import sys
import zlib
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

def getUnzipFilename(did,lang,unzipDir) :
    return unzipDir+"/"+did[-2:]+"/"+did+"."+lang

def unzip(did,docs,langs,sentenceRootDir,unzipDir) :
    for doc,lang in zip(docs,langs) :
	data = file(sentenceRootDir+"/"+doc).read()
	data = zlib.decompress(data)
	unzipFilename = getUnzipFilename(did,lang,unzipDir)
	try :
	    with open(unzipFilename,"w") as f :
		f.write(data)
	except :
	    raise

def removeUnzips(did,langs,unzipDir) :
    # Don't now.
    return

def alignOnePair(l1,l2,did) :
    pass

def setupUnzipDir(unzipDir) :
    for i in range(10) :
	for j in range(10) :
	    mkdir_p(unzipDir+"/"+str(i)+str(j))
    logg("unzipDir was set up.")

# indexLine is coming from named-cross-lingual-index.txt
def doOneDocForAllLangPairs(indexLine, sentenceRootDir, unzipDir, ladderDir) :
    a = indexLine.strip("\n").split()
    did = a[0]
    docs = a[1:]
    langs = [ lang4doc(doc) for doc in docs ]
    unzip(did,docs,langs)
    for i1,l1 in enumerate(langs) :
	for i2 in range(i1+1,len(langs)) :
	    alignOnePair(l1,l2,did)
    removeUnzips(did,langs,unzipDir)
	    
sentenceRootDir = "./ssplit"
unzipDir = "./tmp"
ladderDir = "./ladder"

setupUnzipDir(unzipDir)

doOneDocForAllLangPairs(sys.stdin.readline(), sentenceRootDir, unzipDir, ladderDir)

