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
def holeToText(hole,hulines,enlines):
    hutext = " ~~~ ".join(hulines[hole[0][0]:hole[1][0]])
    entext = " ~~~ ".join(enlines[hole[0][1]:hole[1][1]])
    text = hutext+"\t"+entext
    if len(hole[0])==3 :
	text += "\t"+hole[0][2]
    return text

def isBisen(hole) :
    return (hole[1][0]-hole[0][0]==1) and (hole[1][1]-hole[0][1]==1)

def process(ladderFile,huFile,enFile,justBisen=False) :
    ladderLines = readfile(ladderFile)
    huLines = readfile(huFile)
    enLines = readfile(enFile)
    ladder = map( parseLadderLine, ladderLines )

    outputLines = [ holeToText(hole,huLines,enLines) for hole in pairwise(ladder) if ( isBisen(hole) or not justBisen ) ]
    return outputLines


def main() :
    justBisen = False
    if "--bisen" in sys.argv[1:] :
	justBisen = True
	sys.argv.remove("--bisen")
    if len(sys.argv)==4:
	ladderFile,huFile,enFile = sys.argv[1:]
	outputlines = process(ladderFile,huFile,enFile,justBisen)
	for l in outputlines :
	    print l
    else:
	sys.stderr.write( 'usage: ladder2text.py [ --bisen ] <aligned.ladder> <hu.raw> <en.raw> > aligned.txt\n' )
	sys.exit(-1)


if __name__ == "__main__" :
    main()
