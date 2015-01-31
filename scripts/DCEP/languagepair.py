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
    parser.add_option("--no-merge", action="store_true", dest="noMerge", help="Keep the output bidocuments in separate files under bitext/L1-L2/, instead merging them and writing them to the standard output.")
    parser.add_option("--not-just-bisentences", action="store_false", dest="justBisens", help="Save all alignment units, not just 1-to-1 correspondences.")
    parser.add_option("--delimiter", dest="delimiter", type="string", help="String for delimiting sentences within alignment units.")
    parser.add_option("--topo-filter-level", action="store", type="int", default=50, dest="topoFilterLevel", metavar="TOPO_FILTER_LEVEL",
	help="Agressiveness of context-based bisentence filtering. Between 0 and 100. Default is 50.")
    parser.add_option("--length-filter-level", action="store", type="int", default=50, dest="lengthFilterLevel", metavar="LENGTH_FILTER_LEVEL",
	help="Agressiveness of sentence character length based bisentence filtering. Between 0 and 100. Default is 50.")
    parser.add_option("--index-file", action="store", type="string", dest="indexFilename", metavar="INDEX_FILE",
	help="Tab-separated file with rows containing align L1-sentence-segmented L2-sentence-segmented filenames.")
    parser.usage = "%prog [options] L1-L2\nwhere L1-L2 is a language pair, and L1 and L2 are in alphabetical order. E.g. DE-EN.\n"
    parser.usage += "or\n%prog [options] --index-file INDEX_FILE."

    try :
	(options, args) = parser.parse_args(sys.argv[1:])
    except :
	parser.print_help()
	sys.exit(-1)

    if options.indexFilename :
	if len(args)>0 :
	    error("Should not give a language pair when the --index-file argument is used.")
    else :
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


    if not(0<=options.optTopoFilterLevel<=100) :
	error("TOPO_FILTER_LEVEL should be between 0 and 100 inclusive.")
    if not(0<=options.optLengthFilterLevel<=100) :
	error("LENGTH_FILTER_LEVEL should be between 0 and 100 inclusive.")


    if options.indexFilename :
	indexFilename = options.indexFilename
    else :
	indexFilename = "indices/"+lp

    if not os.path.isfile(indexFilename) :
	error("Missing index "+indexFilename+" file.")

    # TODO This part has not really been figured out yet.
    if options.noMerge :
	mkdir_p("bitext/"+lp)

    prefix = "DCEP/sentence/" # Should be generalized to tokenized text.

    docCounter = 0
    errorCounter = 0
    f = open(indexFilename)
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

	    if options.noMerge :
		resultFilename = "bitext/"+lp+"/"+docid
		try :
		    resultFile = open(resultFilename, "w")
		    for outputLine in outputLines :
			resultFile.write(outputLine+"\n")
		except :
		    error("Failed to write to file %s" % resultFilename)
	    else :
		for outputLine in outputLines :
		    sys.stdout.write(outputLine+"\n")

	    docCounter += 1
	    print "done"
	else :
	    print "skipped"
	    errorCounter += 1
	    if errorCounter>docCounter+100 :
		error("Too many align/"+lp+" files missing, the directory structure was probably not set up properly.")

main()
