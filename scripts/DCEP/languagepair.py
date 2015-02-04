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
    defaultDelimiter = " ~~~ "
    parser.add_option("--no-merge", action="store_true", dest="noMerge", help="Keep the output bidocuments in separate files under bitext/L1-L2/, instead of merging them and writing them to the standard output.")
    parser.add_option("--not-just-bisentences", action="store_false", dest="justBisen", default=True, help="Save all alignment units, not just 1-to-1 correspondences.")
    parser.add_option("--delimiter", dest="delimiter", type="string", default=defaultDelimiter, help="String for delimiting sentences within alignment units. Only meaningful when combined with --not-just-bisentences. Default value: '"+defaultDelimiter+"'.")

# TODO Commented out, hardly finished.
#    parser.add_option("--topo-filter-level", action="store", type="int", dest="topoFilterLevel", metavar="TOPO_FILTER_LEVEL",
#	help="Agressiveness of context-based bisentence filtering. Between 0 and 100. By default it is not employed. Cannot be combined with --not-just-bisentences.")

    parser.add_option("--length-filter-level", action="store", type="int", dest="lengthFilterLevel", metavar="LENGTH_FILTER_LEVEL",
	help="Agressiveness of sentence character length based bisentence filtering. Between 0 and 100. By default it is not employed. Cannot be combined with --not-just-bisentences.")
    parser.add_option("--numbering-filter", action="store_true", dest="sentenceDetector", default=False,
	help="A crude heuristic that drops numberings and short titles from the output. Cannot be combined with --not-just-bisentences.")

    parser.add_option("--index-file", action="store", type="string", dest="indexFilename", metavar="INDEX_FILE",
	help="Use this file to decide which documents to process, instead of the default indices/L1-L2. Tab-separated file with rows containing document-id L1-sentence-segmented-file L2-sentence-segmented-file. When combined with --no-merge, the bitext/L1-L2 directory is deduced from the sentence file paths, assuming DCEP directory structure.")

    parser.usage = "%prog [options] L1-L2\nwhere L1-L2 is a language pair, and L1 and L2 are in alphabetical order. E.g. DE-EN.\n"
    parser.usage += "or\n%prog [options] --index-file INDEX_FILE."

    try :
	assert len(sys.argv)>1
	(options, args) = parser.parse_args(sys.argv[1:])
    except :
	parser.print_help()
	sys.exit(-1)

    if options.indexFilename :
	if len(args)>0 :
	    error("Should not give a language pair when the --index-file argument is used.")
	l1 = None
	l2 = None
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


    if options.topoFilterLevel is not None and not(0<=options.topoFilterLevel<=100) :
	error("TOPO_FILTER_LEVEL should be between 0 and 100 inclusive.")
    if options.lengthFilterLevel is not None and not(0<=options.lengthFilterLevel<=100) :
	error("LENGTH_FILTER_LEVEL should be between 0 and 100 inclusive.")

    if options.indexFilename :
	indexFilename = options.indexFilename
    else :
	indexFilename = "indices/"+lp

    # TODO This part has not really been figured out yet.
    if options.noMerge and not options.indexFilename :
	mkdir_p("bitext/"+lp)

    if options.indexFilename :
	languagePairsEncountered = set()
    else :
	languagePairsEncountered = set((lp,))

    prefix = "DCEP/sentence/" # TODO Should be generalized to tokenized text.

    docCounter = 0
    errorCounter = 0
    try :
	f = open(indexFilename)
    except :
	error("Missing index file "+indexFilename)
    for line in f :
	docid,doc1,doc2 = line.strip().split()

	heuristicL1 = doc1.split("/")[1]
	heuristicL2 = doc2.split("/")[1]
	if l1 is not None :
	    assert heuristicL1==l1
	    assert l2 is not None
	    assert heuristicL2==l2
	else :
	    lp = heuristicL1+"-"+heuristicL2
	    if options.noMerge and (lp not in languagePairsEncountered) :
		mkdir_p("bitext/"+lp)
		languagePairsEncountered.add(lp)

	print docid,
	ladder = "aligns/"+lp+"/"+docid
	doc1 = prefix+doc1
	doc2 = prefix+doc2

	# See explanation of this 'if' at the 'else' path.
	if os.path.isfile(ladder) :
	    outputBytes = ladder2text.process(ladder, doc1, doc2,
	    justBisen=options.justBisen, delimiter=options.delimiter,
	    topoFilterLevel=options.topoFilterLevel, lengthFilterLevel=options.lengthFilterLevel,
	    sentenceDetector=options.sentenceDetector)

	    if options.noMerge :
		resultFilename = "bitext/"+lp+"/"+docid
		try :
		    resultFile = open(resultFilename, "w")
		    resultFile.write(outputBytes)
		    resultFile.close()
		except :
		    error("Failed to write to file %s" % resultFilename)
	    else :
		sys.stdout.write(outputBytes)

	    docCounter += 1
	    print "done"
	else :
	    # Ugly special case code.
	    # Sometimes hunalign rejects a task (e.g. when sentence counts differ too much)
	    # Due to some sloppiness in the postprocessing, these become empty ladder files.
	    # Normally this happens rarely, so if it is common, we take it as a sign that the
	    # directory structure was not set up properly.
	    print "skipped"
	    errorCounter += 1
	    if errorCounter>docCounter+100 :
		error("Too many align/"+lp+" files missing, the directory structure was probably not set up properly.")

main()
