#!/usr/bin/python

import sys
import itertools

'''file -> array holding the lines of the file'''
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

def process(ladderFile, huFile, enFile, justBisen, delimiter) :
    ladderLines = readfile(ladderFile)
    huSentences = readfile(huFile)
    enSentences = readfile(enFile)
    ladder = map( parseLadderLine, ladderLines )
    bisegments = ladderToBisegments(ladder, huSentences, enSentences, justBisen)
    lines = [ serializeBisegment(huSens,enSens,quality,delimiter) for huSens,enSens,quality in bisegments ]
    return "\n".join(lines)+"\n"

def ladderToBisegments(ladder, huSentences, enSentences, justBisen) :
    bisegments = [ holeToBisegment(hole,huSentences,enSentences) for hole in pairwise(ladder) if ( isBisen(hole) or not justBisen ) ]
    return bisegments

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
