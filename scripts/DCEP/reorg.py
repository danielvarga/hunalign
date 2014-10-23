import sys
import gzip
import os, errno

def logg(s) :
    sys.stderr.write(s+"\n")

def mkdir_p(path) :
    try :
        os.makedirs(path)
    except OSError, exc :
        if exc.errno == errno.EEXIST and os.path.isdir(path) :
            pass
        else :
	    raise

def lang4doc(doc) :
    a = doc.split("/")
    assert a[0] in ('sgml','xml')
    return a[1]

def getFlatFilename(did,lang,flatDir) :
    return "%s/%s/%s.%s.txt" % (flatDir,did[-2:],did,lang)

def rename(did,docs,langs,sentenceRootDir,flatDir) :
    for doc,lang in zip(docs,langs) :
	oldFilename = sentenceRootDir+"/"+doc
	newFilename = getFlatFilename(did,lang,flatDir)
	try :
	    shutil.copyfile(oldFilename,newFilename)
	except :
	    raise

def alignOnePair(doc1,doc2,did,l1,l2,tokRootDir,ladderRootDir) :
    # If you send this through a cut -f4- , that's the input for a hunalign -batch run.
    file1 = tokRootDir+"/"+doc1
    file2 = tokRootDir+"/"+doc2
    ladder = '{ladderRootDir}/{didPrefix}/{did}.{l1}.{l2}.ladder'.format(ladderRootDir=ladderRootDir,didPrefix=did[-2:],did=did,l1=l1,l2=l2)
    print "\t".join((did,l1,l2,file1,file2,ladder))

def setupLadderDir(ladderRootDir) :
    logg("Setting up ladderDir.")
    for i in range(10) :
	for j in range(10) :
	    mkdir_p(ladderRootDir+"/"+str(i)+str(j))
    logg("Done.")

# indexLine is coming from unzipped-named-cross-lingual-index.txt
def doOneDocForAllLangPairs(indexLine, tokRootDir, ladderRootDir) :
    a = indexLine.strip("\n").split()
    did = a[0]
    docs = a[1:]
    langs = [ lang4doc(doc) for doc in docs ]
    if int(did)%1000==0 :
	logg(did)

    # rename(did,docs,langs,tokRootDir,tokFlatDir)

    for i1,l1 in enumerate(langs) :
	doc1 = docs[i1]
	for i2 in range(i1+1,len(langs)) :
	    l2 = langs[i2]
	    doc2 = docs[i2]
	    alignOnePair(doc1,doc2,did,l1,l2,tokRootDir,ladderRootDir)


# A typical tokenized file is under tree/tok/${some field in unzipped-named-cross-lingual-index.txt},
# An example of ${some field} is sgml/DA/REPORT/511814__REPORT__A5-2000-0003__DA.txt

# A ladder file is under flat/ladder/${last two digits of did}/$did.$l1.$l2.ladder

def main() :
    tokRootDir = "./tree/tok"
    ladderRootDir = "./flat/ladder"

    setupLadderDir(ladderRootDir)

    for line in sys.stdin :
	doOneDocForAllLangPairs(line, tokRootDir, ladderRootDir)


main()
