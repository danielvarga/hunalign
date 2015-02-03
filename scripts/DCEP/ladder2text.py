#!/usr/bin/python

# In the code you can see lots of variables named hu* and en*, as
# as in Hungarian and English. This does not mean that the tool
# is not completely language-agnostic. By convention, and
# for obvious historical reasons, hu and en should be interpreted
# as language #1 and language #2.

import sys
import itertools
import re

# An especially crude but quite useful heuristics for
# detecting sentences (as opposed to numberings, separators etc).
# Two alphabetic characters with space between them.
# See http://stackoverflow.com/a/2039476/383313 for an explanation.
TWO_WORDS_REGEX = re.compile(r"""\w \w""", re.UNICODE)
# TWO_WORDS_REGEX = re.compile(r"""[^\W\d_] [^\W\d_]""", re.UNICODE)

def readfile(name):
    # Open the input files and read lines
    infile = file(name, 'r')
    lines = map( lambda s : s.strip("\n"), infile.readlines() )
    return lines

'''s -> (s0,s1), (s1,s2), (s2, s3), ...
see http://docs.python.org/library/itertools.html'''
def pairwise(iterable):
    a, b = itertools.tee(iterable)
    b.next()
    return itertools.izip(a, b)

'''Create aligned text from two sentence files and hunalign's ladder-style output.
Usage: ladder2text.py <aligner.ladder> <hu.sen> <en.sen> > aligned.txt
See http://mokk.bme.hu/resources/hunalign for detailed format specification and more.
The output file is tab-delimited, with two or three columns.
The first and second columns are the chunks corresponding to each other.
" ~~~ " is the sentence delimiter inside chunks.
The third column is a probability score, if the input file had one.
'''

def parseLadderLine(l):
    a = l.split()
    # We allow both scored and score-less input.
    assert 2<=len(a)<=3
    # The score we leave as a string, to avoid small diffs caused by different numerical representations.
    a[0],a[1] = int(a[0]),int(a[1])
    return a

# a hole is supposed to be two consecutive items in the array holding the lines of the ladder. /an array of holes is returned by pairwise(ladder)/
# the following segment returns an interval of sentences corresponding to a hole:
# hulines[int(hole[0][0]):int(hole[1][0])]
def holeToBisegment(hole,hulines,enlines) :
    if len(hole[0])==3 :
	quality = hole[0][2]
    else :
	quality = None

    huSens = hulines[hole[0][0]:hole[1][0]]
    enSens = enlines[hole[0][1]:hole[1][1]]
    return huSens,enSens,quality

    #serializeSens(huSens, enSens, quality, delimiter)

def serializeBisegment(huSens,enSens,quality=None,delimiter=" ~~~ ") :
    huText = delimiter.join(huSens)
    enText = delimiter.join(enSens)
    text = huText+"\t"+enText
    if quality is not None :
	text += "\t"+str(quality)
    return text

def isBisen(hole) :
    return (hole[1][0]-hole[0][0]==1) and (hole[1][1]-hole[0][1]==1)

def isBisenPos(pos,ladder) :
    assert pos+2<=len(ladder)
    hole = ladder[pos:pos+2]
    return isBisen(hole)

def crudeSentenceDetector(huSenUtf,enSenUtf) :
    return TWO_WORDS_REGEX.search(huSenUtf) is not None and TWO_WORDS_REGEX.search(enSenUtf) is not None

def isAcceptableLength(huSenUtf,enSenUtf,lengthFilterLevel) :
    lengthFilterRatio = float(lengthFilterLevel)/100 # TODO Casting in every inner loop, how lame is that.
    if lengthFilterLevel is None :
	return True
    h = len(huSenUtf)+1
    e = len(enSenUtf)+1
    ratio = float(h)/e
    if ratio>1 :
	ratio = 1/ratio
    return ratio>=lengthFilterRatio

def filterTopology(ladder, topoFilterLevel) :
    if topoFilterLevel is None :
	return ladder

    WINDOW = 100
    # the higher the stricter.
    topoFilterRatio = float(topoFilterLevel)/100
    rungsToKill = set()
    trailSize = len(ladder)
    for pos in range(1,trailSize-1-WINDOW) :
	huStart = ladder[pos][0]
	enStart = ladder[pos][1]
	huEnd = ladder[pos+WINDOW][0]
	enEnd = ladder[pos+WINDOW][1]
	deviation = float(huEnd-huStart+1)/(enEnd-enStart+1) # TODO We don't currently use it.
	if deviation>1 :
	    deviation = 1/deviation
	bisenCnt = 0
	for pos2 in range(pos,pos+WINDOW) :
	    if isBisenPos(pos2,ladder) :
		bisenCnt += 1
	ratio = float(bisenCnt)/WINDOW
	# sys.stderr.write("%f %f\n" % (ratio,deviation))
	# TODO That's lame algorithmically, will switch to proper window-sliding when the basic algorithm is validated.
	if ratio<topoFilterRatio :
	    for pos2 in range(pos,pos+WINDOW) :
		rungsToKill.add(pos2)

    newLadder = [ rung for pos,rung in enumerate(ladder) if pos not in rungsToKill ]
    return newLadder

# topoFilter, lengthFilter, and sentenceDetector are only meaningingful for justBisen.
# The former is applied before holeToBisegment, and works by removing rungs.
# The latter two are applied after collecting the bisegments.
def ladderToBisegments(ladderOrig, huSentences, enSentences, justBisen, topoFilterLevel, lengthFilterLevel, sentenceDetector) :
    ladder = ladderOrig[:]

    if topoFilterLevel is not None or lengthFilterLevel is not None :
	assert justBisen

    if topoFilterLevel is not None :
	ladder = filterTopology(ladder, topoFilterLevel)

    bisegments = [ holeToBisegment(hole,huSentences,enSentences) for hole in pairwise(ladder) if ( isBisen(hole) or not justBisen ) ]

    if lengthFilterLevel is not None or sentenceDetector :
	keptBisegments = []
	for bisegment in bisegments :
	    # Lossiness is not an issue, we only use this to filter the raw bisegments.
	    huSenUtf = bisegment[0][0].decode("utf-8","ignore")
	    enSenUtf = bisegment[1][0].decode("utf-8","ignore")
	    if lengthFilterLevel is not None and not isAcceptableLength(huSenUtf, enSenUtf, lengthFilterLevel) :
		continue
	    if sentenceDetector and not crudeSentenceDetector(huSenUtf,enSenUtf) :
		continue
	    keptBisegments.append(bisegment)
	bisegments = keptBisegments

    return bisegments


def process(ladderFile, huFile, enFile, justBisen, delimiter, topoFilterLevel, lengthFilterLevel, sentenceDetector) :
    ladderLines = readfile(ladderFile)
    huSentences = readfile(huFile)
    enSentences = readfile(enFile)
    ladder = map( parseLadderLine, ladderLines )
    bisegments = ladderToBisegments(ladder, huSentences, enSentences, justBisen, topoFilterLevel, lengthFilterLevel, sentenceDetector)
    lines = [ serializeBisegment(huSens,enSens,quality,delimiter) for huSens,enSens,quality in bisegments ]
    return "\n".join(lines)+"\n"


def main() :
    justBisen = False
    if "--bisen" in sys.argv[1:] :
	justBisen = True
	sys.argv.remove("--bisen")
    if len(sys.argv)==4:
	ladderFile,huFile,enFile = sys.argv[1:]
	outputString = process(ladderFile, huFile, enFile, justBisen=justBisen, delimiter=" ~~~ ")
	sys.stdout.write(outputString) # There's a \n at the end of outputString already.
    else:
	sys.stderr.write( 'usage: ladder2text.py [ --bisen ] <aligned.ladder> <hu.raw> <en.raw> > aligned.txt\n' )
	sys.exit(-1)


if __name__ == "__main__" :
    main()
