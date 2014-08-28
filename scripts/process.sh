#!/bin/bash

lang=Hungarian ; slang=hu ; cat $CATALOG | tr '\t' '\n' | while read au ; read ind ; do mkdir $lang/$au/sen 2>/dev/null ; echo $lang/$au/sen/${au}_$ind.$slang.sen ; $BINDIR/hu.sen.one.sh < $lang/$au/raw/${au}_$ind.$slang.raw > $lang/$au/sen/${au}_$ind.$slang.sen ; done

lang=English ; slang=en ; cat $CATALOG | tr '\t' '\n' | while read au ; read ind ; do mkdir $lang/$au/sen 2>/dev/null ; echo $lang/$au/sen/${au}_$ind.$slang.sen ; $BINDIR/en.sen.one.sh < $lang/$au/raw/${au}_$ind.$slang.raw > $lang/$au/sen/${au}_$ind.$slang.sen ; done


lang=Hungarian ; slang=hu ; cat $CATALOG | tr '\t' '\n' | while read au ; read ind ; do mkdir $lang/$au/sen.tok 2>/dev/null ; echo $lang/$au/sen.tok/${au}_$ind.$slang.sen.tok ; $BINDIR/tok.one.sh < $lang/$au/sen/${au}_$ind.$slang.sen > $lang/$au/sen.tok/${au}_$ind.$slang.sen.tok ; done

lang=English ; slang=en ; cat $CATALOG | tr '\t' '\n' | while read au ; read ind ; do mkdir $lang/$au/sen.tok 2>/dev/null ; echo $lang/$au/sen.tok/${au}_$ind.$slang.sen.tok ; $BINDIR/tok.one.sh < $lang/$au/sen/${au}_$ind.$slang.sen > $lang/$au/sen.tok/${au}_$ind.$slang.sen.tok ; done


lang=Hungarian ; slang=hu ; cat $CATALOG | tr '\t' '\n' | while read au ; read ind ; do mkdir $lang/$au/sen.tok.stem 2>/dev/null ; echo $lang/$au/sen.tok.stem/${au}_$ind.$slang.sen.tok.stem ; $BINDIR/$slang.stem.one.sh < $lang/$au/sen.tok/${au}_$ind.$slang.sen.tok > $lang/$au/sen.tok.stem/${au}_$ind.$slang.sen.tok.stem ; done

lang=English ; slang=en   ; cat $CATALOG | tr '\t' '\n' | while read au ; read ind ; do mkdir $lang/$au/sen.tok.stem 2>/dev/null ; echo $lang/$au/sen.tok.stem/${au}_$ind.$slang.sen.tok.stem ; $BINDIR/$slang.stem.one.sh < $lang/$au/sen.tok/${au}_$ind.$slang.sen.tok > $lang/$au/sen.tok.stem/${au}_$ind.$slang.sen.tok.stem ; done

# /////////////////////////////////////////////////
# VEGRE ALIGN, POSZTPROCESSZOROKKAL:

mkdir $BICDIR/Align

cat $CATALOG | cut -f1 | sort -u | while read d ; do mkdir $BICDIR/Align/$d ; mkdir $BICDIR/Align/$d/ladder ; done


cat $CATALOG | awk '{ print "Hungarian/"$1"/sen.tok.stem/"$1"_"$2".hu.sen.tok.stem" "\t" "English/"$1"/sen.tok.stem/"$1"_"$2".en.sen.tok.stem" "\t" "Align/"$1"/ladder/"$1"_"$2".ladder" }' > align.batch

$BINDIR/alignerTool -batch -headerthresh=100 -ppthresh=30 $BINDIR/vonyo7.nojoker.stemmed align.batch > align.cout 2> align.cerr

cat $CATALOG | cut -f1 | sort -u | while read d ; do mkdir $BICDIR/Align/$d/text ; done

cat $CATALOG | tr '\t' '\n' | while read au ; read ind ; do lang=Hungarian ; slang=hu ; $BINDIR/ladder2text.sh $BICDIR/Align/$au/ladder/${au}_$ind.ladder $BICDIR/Hungarian/$au/sen/${au}_$ind.hu.sen $BICDIR/English/$au/sen/${au}_$ind.en.sen > $BICDIR/Align/$au/text/${au}_$ind.text ; done


cat $CATALOG | cut -f1 | sort -u | while read d ; do mkdir $BICDIR/Align/$d/text.qf ; done

cat $CATALOG | tr '\t' '\n' | while read au ; read ind ; do echo Align/$au/text.qf/${au}_$ind.text.qf ; cat Align/$au/text/${au}_$ind.text | grep -v "~~~" | grep -v "<p>" | awk 'BEGIN {FS="\t"} { ra = ( length($2)>length($3) ? (length($2)+10)/(length($3)+10) : (length($3)+10)/(length($2)+10) ) ; if (ra<1.5) print $0}' > Align/$au/text.qf/${au}_$ind.text.qf ; done


cat $CATALOG | cut -f1 | sort -u | while read d ; do mkdir $BICDIR/Align/$d/shuffled ; done

cat $CATALOG | tr '\t' '\n' | while read au ; read ind ; do echo Align/$au/shuffled/${au}_$ind.shuffled ; cat Align/$au/text.qf/${au}_$ind.text.qf | cut -f2,3 | sort > $BICDIR/Align/$au/shuffled/${au}_$ind.shuffled ; done


mkdir measure

cat $CATALOG | tr '\t' '\n' | while read au ; read ind ; do lang=Hungarian ; slang=hu ; hu=`cat $lang/$au/sen/${au}_$ind.$slang.sen | grep -v "<p>" | wc -l` ; lang=English ; slang=en ; en=`cat $lang/$au/sen/${au}_$ind.$slang.sen | grep -v "<p>" | wc -l` ; echo ${au}_$ind $hu $en ; done | awk '{ h=$2+1; e=$3+1; print (h<e ? h/e : e/h) "\t" $1 "\t" h "\t" e "\t" h/e }' | sort -n | cut -f2- > measure/senratio.txt

cat $CATALOG | tr '\t' '\n' | while read au ; read ind ; do i=$BICDIR/Align/$au/ladder/${au}_$ind.ladder ; echo -n "$i" ; cat $i | awk '{ if (($1-one==1)&&($2-two==1)) { ++bis } ; one=$1; two=$2 } END { print "\t" 0+bis "\t" 0+one "\t" 0+two "\t" bis/(1+(one<two?one:two))}' ; done | sort -n +4 > measure/otor.txt
