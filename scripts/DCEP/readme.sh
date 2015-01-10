#####
# Live documentation slash script collection for the creation of the DCEP parallel corpus.
#####


cat cross-lingual-index.txt | awk '{ print NF,NF*(NF-1)/2 }' | sort -n | uniq -c | awk '{ print $1,$2,$3,$1*$3 }' | tr ' ' '\t' | sort -n -k 3 | awk '{ s+=$4 ; print }  END { print s }'

22581	1	0	0
40480	2	1	40480
2090	3	3	6270
990	4	6	5940
627	5	10	6270
393	6	15	5895
248	7	21	5208
223	8	28	6244
329	9	36	11844
1876	10	45	84420
76234	11	55	4192870
5269	12	66	347754
258	13	78	20124
164	14	91	14924
225	15	105	23625
285	16	120	34200
374	17	136	50864
567	18	153	86751
2504	19	171	428184
2816	20	190	535040
912	21	210	191520
12321	22	231	2846151
18	23	253	4554
8949132


cd sentences
wget -r l2 http://optima.jrc.it/Resources/DCEP-2013/sentences/list.html

tar xjvf optima.jrc.it/Resources/DCEP-2013/sentences/DCEP-strip-CS-pub.tar.bz2 > cout 2> cerr
tar xjvf optima.jrc.it/Resources/DCEP-2013/sentences/DCEP-strip-CS-pub.tar.bz2 > cout2 2> cerr2
tar xjvf optima.jrc.it/Resources/DCEP-2013/sentences/DCEP-sentence-DA-pub.tar.bz2 > cout 2> cerr
tar xjvf optima.jrc.it/Resources/DCEP-2013/sentences/DCEP-sentence-CS-pub.tar.bz2 > cout2 2> cerr2

cat DCEP/strip/sgml/CS/QT/8369873__QT__H-2004-0355__CS.txt
cat DCEP/sentence/sgml/CS/QT/8369873__QT__H-2004-0355__CS.txt

# OMG stupid sentence segmenter fucks all dates.

cd DCEP/sentence # Now at ~/big/experiments/DCEP/sentences/DCEP/sentence
cat ../../../cross-lingual-index.txt | awk '{ s="" ; c=0 ; for (i=1;i<=NF;++i) { a=$i ; if ((a~/\/CS\//)||(a~/\/DA\//)) { s = s a " " ; ++c } } ; if (c==2) { print s } }' | sed "s/ $//" | sed "s/\.[a-z]*\.gz/.txt/g" | head -5 | while read a b ; do ls $a $b ; done

####

# The last effort was under ~/big/experiments/AcquisExtended2/raw
# , that's where all the nice scripts are. This is the hierarchy:

- alignallpairsforalldocs.sh
  - alignallpairs.sh
    - alignonepair.sh
      - hunalign
- bisentsforalllanguagepairs.sh
  - bisentsforlanguagepair.sh
    - ladder2text.sh
    - filteralign.sh
- dictsforalllanguagepairs.sh
  - dictforlanguagepair.sh
    - coocc
- alignallpairsforalldocs.withdic.sh
  - as to be expected
- convert to some output that everyone likes, originally ladder2jrc.allpairsforalldocs.sh and ladder2jrc.awk

####

# What's gonna be the document id? The cross-lingual-index.txt
# doesn't have this notion, per se.

cd ~/big/experiments/DCEP/sentences/DCEP/sentence
cat cross-lingual-index.txt | awk 'BEGIN { FS="/" }  { split($0,a,"__") ; s = $1 "." a[2] "." a[3] ; print s }' | sort > /tmp/x
diff /tmp/x <(uniq /tmp/x) | grep "^<" | wc -l
5945
cat cross-lingual-index.txt | awk 'BEGIN { FS="/" }  { split($0,a,"__") ; s = a[2] "." a[3] ; print s }' | sort > /tmp/y
diff /tmp/y <(uniq /tmp/y) | grep "^<" | wc -l
5945

# -> Oops, that's not a uniq id.

cat cross-lingual-index.txt | awk '{ printf("%06d\t%s\n", NR, $0) }' | less 


# Okay, let's unpack all of 'em.

cd DCEP/sentences # Now at ~/big/experiments/DCEP/sentences
ls optima.jrc.it/Resources/DCEP-2013/sentences/DCEP-sentence-* | cut -f4 -d'-' > langs.txt
# unzip does a tar jxvf for all strip and sentence files:
nohup bash unzip.sh > cout 2> cerr &

cd ~/big/experiments/DCEP/
cat cross-lingual-index.txt | awk '{ printf("%06d\t%s\n", NR, $0) }' > named-cross-lingual-index.txt 

# Moved ~/big/experiments/DCEP/ssplit and ssplit-DCEP.tar into ~/big/experiments/DCEP/Attic , they
# are obsoleted by Jaakko's versions.
# Moved Jaakko's versions from ~/big/experiments/DCEP/sentences/DCEP/ to ~/big/experiments/DCEP/tree
# Here tree refers to the original directory structure (sgml/OT/whatever), and flat will refer to my
# numerical id (did) based structure.
# The zipped ones stayed at ~/big/experiments/DCEP/sentences
mv sentences/DCEP/sentence tree 
mv sentences/DCEP/strip tree

# Let's do the tokenization still on the tree struct.
find tree/sentence -type d > struct-of-tree.txt # Takes 4 minutes even on kruso.
cat struct-of-tree.txt | sed "s/^tree\/sentence/tree\/tok/" | while read d ; do mkdir -p "$d" ; done
nohup bash hunalign/scripts/DCEP/tokenizeAll.sh > cout.tokenizeAll 2> cerr.tokenizeAll &
# Actually, I forgot the nohup but dropping the conn still didn't kill it somehow.
# I wonder if it will eventually realize it. Estimated to take 13 hours.

# Parallelly (having two strings to my bow) I unpacked it on my laptop,
# under ~/experiments/DCEP/DCEP. Will rename it to DCEP/tree and run the tokenizer. Seems to be OS X compatible.

# Both finished, the kruso one and the macbook one.
# macbook needed 5.5 hours for tok, and 3.5 hours to verify line counts.
# kruso needed 43.1 hours for tok, and randomly failed (produced 0 byte output) on 49 files,
# documented in cout.tokenizeAll. Also, it seems like the verification did not finish,
# the final "Done." line and date is missing from the output.
# I see no good reason to use kruso at this point.


cat named-cross-lingual-index.txt | sed "s/sgml\.gz/txt/g" | sed "s/xml\.gz/txt/g" > unzipped-named-cross-lingual-index.txt

# I create an augmented hunalign batch file.
cat unzipped-named-cross-lingual-index.txt | python hunalign/scripts/DCEP/reorg.py > total.aligninfo
# A line looks like this:
000001	DA	IT	./tree/tok/sgml/DA/REPORT/511814__REPORT__A5-2000-0003__DA.txt	./tree/tok/sgml/IT/REPORT/511822__REPORT__A5-2000-0003__IT.txt	./flat/ladder/01/000001.DA.IT.ladder
# reorg.py additionally creates the ./flat/ladder/${last two digits of did} subdirs.

wc -l total.aligninfo
8949132

# Looking at
cat total.aligninfo | cut -f1 | sed "s/^....//" | sort | uniq -c
# we can see that every flat subdir will have to keep about 90000 files. A bit too much.

cat total.aligninfo | cut -f2,3 | sort | uniq -c | sort -nr | less
# -> There are basically two or three waves of countries depending on EU join times.
# GA and TR are jokes, with 10 or so docs.
# 55 pairs with 100k-110k bidocs.
# 176 pairs with 14k-23k bidocs.
# 44 pairs with less than 15 bidocs.

# Okay, let's roll.
time ./hunalign/src/hunalign/hunalign -batch hunalign/data/null.dic <( head -1000 total.aligninfo | cut -f4- ) 2> cerr.hunalign.batch

cat total.aligninfo | awk '(NR%1000==0)' > sample.aligninfo
wc -l < sample.aligninfo
    8949

time ./hunalign/src/hunalign/hunalign -batch hunalign/data/null.dic <( cat sample.aligninfo | cut -f4- ) 2> cerr2.hunalign.batch

# Takes 3 min 25 sec = 205 sec, 8e6/8949*205/3600=50 hours total time.

# Encountered the loop bug twice.

# Let's do it with a real random sample:
cat total.aligninfo | awk '(rand()<0.001)' > sample2.aligninfo # 9021 elements.
time ./hunalign/src/hunalign/hunalign -batch hunalign/data/null.dic <( cat sample2.aligninfo | cut -f4- ) 2> cerr3.hunalign.batch
# 3m55.518s that is 8e6/9021*236/3600=58 hours, that's okay.

# Encountered the loop bug only once!

# What about the output?:
cat sample2.aligninfo | cut -f4- | head -10 | while read t1 t2 l ; do hunalign/scripts/ladder2text.py $l $t1 $t2 ; done | less
cat sample2.aligninfo | cut -f4- | head -10 | while read t1 t2 l ; do t1=`echo $t1 | sed "s/tok/sentence/"` ; t2=`echo $t2 | sed "s/tok/sentence/"` ; hunalign/scripts/ladder2text.py $l $t1 $t2 ; done | less
# Looks pretty good so far.


# Okay, so I'll try to run it on nessie.nytud.hu, if the guys are fine with it.

# This is how you tar a subset of the tokenized input:
cat sample2.aligninfo | cut -f4,5 | tr '\t' '\n' | sort -u > sample2.fileset
tar czvf sample2.tgz --files-from sample2.fileset 2> cerr
scp sample2.tgz nessie.nytud.hu:./experiments/DCEP/
scp sample2.aligninfo nessie.nytud.hu:./experiments/DCEP/

# on macbook:
scp -r hunalign nessie.nytud.hu:./experiments/DCEP/ > cout 2> cerr
# At this point I can already run hunalign batch on sample2.
# It takes 2 min 56 sec on nessie, faster than macbook's 3 min 55 sec.
# I'll do it all, and I'll start from scratch aka Jaakko's tbz2s.

######
# Moving to nessie

# So let's start from total scratch:
scp -r hunalign nessie.nytud.hu:./experiments/DCEP/ > cout 2> cerr
scp langs.txt nessie.nytud.hu:./experiments/DCEP/
scp named-cross-lingual-index.txt unzipped-named-cross-lingual-index.txt nessie.nytud.hu:./experiments/DCEP/
scp unzip.sh nessie.nytud.hu:./experiments/DCEP/

# on nessie:
scp -r kruso.mokk.bme.hu:./big/experiments/DCEP/sentences/optima.jrc.it/Resources/DCEP-2013/sentences .
nohup bash unzip.sh &
# ...when done:
mv DCEP tree
find tree/sentence -type d > struct-of-tree.txt
cat struct-of-tree.txt | sed "s/^tree\/sentence/tree\/tok/" | while read d ; do mkdir -p "$d" ; done
nohup bash hunalign/scripts/DCEP/tokenizeAll.sh > cout.tokenizeAll 2> cerr.tokenizeAll &


cat unzipped-named-cross-lingual-index.txt | python hunalign/scripts/DCEP/reorg.py > total.aligninfo
cat total.aligninfo | cut -f4- > total.hunalign.batch
nohup ./hunalign/src/hunalign/hunalign -batch hunalign/data/null.dic total.hunalign.batch 2> cerr.total.hunalign.batch &
ps | grep hunalign | cut -f1 -d' ' | xargs renice -n 19


# Running, I look into it time to time, and mostly it's fine. This one's not fine:
python hunalign/scripts/ladder2text.py ./flat/ladder/15/015015.ET.IT.ladder ./tree/tok/xml/ET/IM-PRESS/16476079__IM-PRESS__20060322-BRI-06601__ET.txt ./tree/tok/xml/IT/IM-PRESS/16594256__IM-PRESS__20060322-BRI-06601__IT.txt | less
# Complete bollocks, and it's not really hunalign's fault.

# Wow, hunalign -batch finished all ~9M bidocs, and basically failed only on one.
# More exactly, it failed on 2879 lousy bidocs with the "rare loop bug" thing,
# and failed on 1 with an assertion, because both docs had 0 sentences.
# It never did its "WARNING: Downgrading planned thickness" thing, which is a bit weird.
# Running time was 48 hours 20 minutes.
# The subcorpora have very different running times:
# The middle did is 085891, and that was done just 12 hours before the end.
# The middle element of total.aligninfo is 058390.IT.NL.ladder,
# and that was done just 25 minutes before 085891. What!?

# Based on this chart:
ls -l flat/ladder/00/ | grep DE.EN | awk '{ print $6,$7,$8 "\t" $9 }' | sed "s/\..*//"
# did 45500 to did 162300 was done in just 2.5 hours. Those are some WQ and WQA, at a first glance.


# Random sample of bidocuments:
time cat total.aligninfo | awk '{ print rand() "\t" $0 }' | sort -T . | cut -f2- > total.aligninfo.shuffled 
# -> Was just 2 mins.
# Collecting no more than 10000 bidocs for each language pair:
cat total.aligninfo.shuffled | awk 'BEGIN{FS="\t"; limit=10000}  { lp=$2 $3 ; n=++lc[lp] ; if (n<=limit) { print } }' > total.aligninfo.shuffled.limitin10000
cat total.aligninfo.shuffled | awk 'BEGIN{FS="\t"; limit=1000}  { lp=$2 $3 ; n=++lc[lp] ; if (n<=limit) { print } }' > total.aligninfo.shuffled.limitin1000

# Collecting bisentences from above random sample of bidocuments:
nohup bash hunalign/scripts/DCEP/extract-bisentences.sh &
# -> Output in langpairs/biqf , name biqf is used for historical reasons, meaning quality-filtered bisentences.

# Building the dicts. Took exactly two weeks.
nohup bash hunalign/scripts/DCEP/dictsforalllanguagepairs.sh &


###
Sztaki guys have dicts for millions of language pairs:
nohup wget -r -l 2 http://hlt.sztaki.hu/resources/dict/bylangpair/wiktionary_2013july/ > cout.wget.hlt 2> cerr.wget.hlt
mv hlt.sztaki.hu/resources/dict/bylangpair/wiktionary_2013july hlt.sztaki.dicts

# Copy them to langpairs/sztaki/DA-HU.dic etc. :
bash hunalign/scripts/DCEP/renamesztakidicts.sh 2> cerr.renamesztakidicts
# -> 210 exists, 66 does not, good ratio.

# Merge the autodicts and sztaki dicts, and in the process converting them to the hunalign dic format.
bash hunalign/scripts/DCEP/mergedicts.sh
# -> messes on cerr for the 66 missing dicts, but that's harmless.

# Sort total.aligninfo into packs by language pair.
# This is much slower than it could be, but so what, still just 45 mins.
bash hunalign/scripts/DCEP/packaligninfobylangpair.sh

# Create the flat directory hierarchy with the 00-99 dirs:
cd hunalign/scripts/DCEP/
python
>>> import reorg
>>> reorg.setupLadderDir("../../../flat/ladder2/")
cd ../../..

# Turn the langpair/aligninfo files into proper hunalign batch files, targeting flat/ladder2
bash hunalign/scripts/DCEP/batchfilebylangpair.sh

# Do the realign:
nohup bash hunalign/scripts/DCEP/realignall.sh > realign.log &

# How long would it take? Took 2 hours to finish BG-[A-G]*. This is 132527/8949132 of the whole thing.
# That's 5.6 days. Actually it's worse than that, these BG-* dictionaries are very small (no sztaki), except for BG-EN.
# BG-EN took 21 mins, the rest each took 10-13. That's bad.

###

# Okay, BG-CS is already done, let's check it:
l1=BG ; l2=CS
cat langpairs/batch/$l1-$l2.batch | awk '{ print $3,$1,$2 }' | while read l t1 t2 ; do hunalign/scripts/ladder2text.py $l $t1 $t2 | cut -f2,3 ; done > tmp.$l1-$l2.text
cat total.hunalign.batch | grep "$l1\.$l2" | while read t1 t2 l ; do hunalign/scripts/ladder2text.py $l $t1 $t2 | cut -f2,3 ; done > tmp.$l1-$l2.firstalign.text
diff tmp.$l1-$l2.firstalign.text tmp.$l1-$l2.text | less
# -> Some improvement, not too much. This is a small dict.

# Same with l1=BG ; l2=EN , here we have more text and a pretty large sztaki dict.


