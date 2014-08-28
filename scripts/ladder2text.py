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
The output file is tab-delimited, with three columns. The first is a probability score.
The second and third columns are the chunks corresponding to each other.
" ~~~ " is the sentence delimiter inside chunks.
'''
def main() :
	if len(sys.argv) == 4:
		ladderlines = readfile(sys.argv[1])
		hulines = readfile(sys.argv[2])
		enlines = readfile(sys.argv[3])
		def parseLadderLine(l) :
		    a = l.split()
		    assert len(a)==3
		    return ( int(a[0]), int(a[1]), a[2] ) # The score we leave as a string, to avoid small diffs caused by different numerical representations.
		ladder = map( parseLadderLine, ladderlines )

		# the next map() does all the work, so here are some comments...
		# the map() iterates over the holes of the ladder. 
		# a hole is supposed to be two consecutive items in the array holding the lines of the ladder. /an array of holes is returned by pairwise(ladder)/
		# the following segment returns an interval of sentences corresponding to a hole:
		# hulines[int(hole[0][0]):int(hole[1][0])]
		outputlines = map( lambda hole:
		    hole[0][2] + "\t" +
		    " ~~~ ".join(hulines[int(hole[0][0]):int(hole[1][0])]) 
		    + "\t" + 
		    " ~~~ ".join(enlines[int(hole[0][1]):int(hole[1][1])])
		,
		    pairwise(ladder)
		)
		
		for l in outputlines :
		    print l
	else:
		print 'usage: ladder2text.py <aligned.ladder> <hu.raw> <en.raw> > aligned.txt'
		sys.exit(-1)


if __name__ == "__main__" :
	main()
