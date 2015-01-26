#!/usr/bin/python

import sys
import os.path
import os, errno
import optparse

import ladder2text


dcepLanguages = [ "BG", "CS", "DA", "DE", "EL", "EN", "ES", "ET", "FI", "FR", "GA", "HU", "IT", "LT", "LV", "MT", "NL", "PL", "PT", "RO", "SK", "SL", "SV", "TR" ]


class InputError(Exception):
    pass

def error(s) :
    sys.stderr.write("ERROR: "+s+"\n")
    sys.exit(-1)

def mkdir_p(path) :
    try :
        os.makedirs(path)
    except OSError, exc :
        if exc.errno == errno.EEXIST and os.path.isdir(path) :
            pass
        else :
            raise

def main():

    parser = optparse.OptionParser()
    # HERE COME THE REAL OPTIONS
    # --no-merge (does not merge them into a giant output file)
    # --not-just-bisentences
    # --delimiter (for --not-just-bisentences, default " ~~~ ".)
    # --topo-filter-level LEVEL
    # --length-filter-level LEVEL
    # --index-file INDEX_FILE (instead of the default indices/L1-L2)

    (options, args) = parser.parse_args(sys.argv[1:])

    try :
	assert len(args)==1
	lp = args[0]
	l1,l2 = lp.split("-")
	assert len(l1)==len(l2)==2
	assert l1<l2
    except :
	error("One and only one language pair should be provided as argument, in L1-L2 format.\nL1 must be lexicographically smaller than L2.")

    for l in (l1,l2) :
	if l not in dcepLanguages :
	    error(l1+" is not the language code of a DCEP language.")

    batchfilename = "indices/"+lp

    if not os.path.isfile(batchfilename) :
	error("Missing "+batchfilename+" file.")

    mkdir_p("bitext/"+lp)

    prefix = "DCEP/sentence/" # Should be generalized to tokenized text.

    docLimit = 1e10 # Will add a --count argument later

    docCounter = 0
    errorCounter = 0
    f = open(batchfilename)
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
	    resultFilename = "bitext/"+lp+"/"+docid
	    try :
		resultFile = open(resultFilename, "w")
		for outputLine in outputLines :
		    resultFile.write(outputLine+"\n")
	    except :
		error("Failed to write file %s" % resultFilename)
	    docCounter += 1
	    if docCounter>=docLimit :
		break
	    print "done"
	else :
	    print "skipped"
	    errorCounter += 1
	    if errorCounter>docCounter+100 :
		error("Too many align/"+lp+" files missing, the directory structure was probably not set up properly.")

try :
    main()
except InputError :
    sys.stderr.write("Usage: languagepair.py L1-L2\n")
    sys.stderr.write("L1 and L2 are two-letter language codes, in alphabetical order.\n")
    sys.exit(-1)
