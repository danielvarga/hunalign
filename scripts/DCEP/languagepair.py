#!/usr/bin/python

import sys
import os.path
import os, errno
import ladder2text

class InputError(Exception):
    pass

def mkdir_p(path) :
    try :
        os.makedirs(path)
    except OSError, exc :
        if exc.errno == errno.EEXIST and os.path.isdir(path) :
            pass
        else :
            raise

def main():
    try:
	assert len(sys.argv)==2
	lp = sys.argv[1]
	l1,l2 = lp.split("-")
	assert len(l1)==len(l2)==2
	assert l1<l2
    except:
	raise InputError

    batchfilename = "indices/"+lp

    if not os.path.isfile(batchfilename) :
	sys.stderr.write("Missing "+batchfilename+" file.\n")
	sys.exit(-1)

    mkdir_p("bitext/"+lp)

    prefix = "DCEP/sentence/" # Should be generalized to tokenized text.

    docLimit = 1e10 # Will add a --count argument later

    docCounter = 0
    errorCounter = 0
    with open(batchfilename) as f :
	for line in f :
	    docid,doc1,doc2 = line.strip().split()
	    print docid,
	    ladder = "aligns/"+lp+"/"+docid
	    doc1 = prefix+doc1
	    doc2 = prefix+doc2
	    
	    # Ugly special case code:
	    # Sometimes hunalign rejects a task (e.g. when sentence counts differ too much)
	    # Due to some sloppiness in the postprocessing, these become empty ladder files.
	    # Normally this happens rarely, so if it is common, we take it as a sign that the
	    # directory structure was not set up properly.
	    if os.path.isfile(ladder) :
		outputLines = ladder2text.process(ladder,doc1,doc2,justBisen=False) # Will add --bisen flag later
		with open("bitext/"+lp+"/"+docid, "w") as g :
		    for outputLine in outputLines :
			g.write(outputLine+"\n")
		docCounter += 1
		if docCounter>=docLimit :
		    break
		print "done"
	    else :
		print "skipped"
		errorCounter += 1
		if errorCounter>docCounter+100 :
		    sys.stderr.write("Too many align/"+lp+" files missing, the directory structure was probably not set up properly.\n")
		    sys.exit(-1)

try :
    main()
except InputError :
    sys.stderr.write("Usage: languagepair.py L1-L2\n")
    sys.stderr.write("L1 and L2 are two-letter language codes, in alphabetical order.\n")
    sys.exit(-1)
