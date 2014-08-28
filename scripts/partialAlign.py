#!/usr/bin/python

import sys
import itertools

def log(s) :
    sys.stderr.write(s+"\n")

def tokenFreq(corpus) :
    freq = {}
    for l in corpus :
        for t in l :
            if t in freq :
                freq[t] += 1
            else :
                freq[t] = 1
    return freq

# kis gyengeseg: elengedjuk azokat az anchor-szavakat,
# amik ketszer de egy sorban szerepelnek. na bumm.
def hapaxes(freq) :
    hapaxes = set()
    for token,cnt in freq.iteritems() :
        if cnt==1 :
            hapaxes.add(token)
    return hapaxes

def hapaxPositions( hapaxes, corpus ) :
    hapaxPos = {}
    for ind,l in enumerate(corpus) :
        for t in l :
            if t in hapaxes :
                hapaxPos[t] = ind
    return hapaxPos

def uniqSort(l) :
    return [ p for p,g in itertools.groupby(sorted(l)) ]

def less(a,b) :
    return a[0]<b[0] and a[1]<b[1]

# feltetelezi, hogy uniqSort meg volt hivva a bemenetre!
def maximalChain(pairs) :
    lattice = {}
    for p in pairs :
        bestLength = 0
        bestPredessor = None
        for q in pairs :
            if less(q,p) :
                length,dummy = lattice[q]
                if bestLength<length+1 :
                    bestLength = length+1
                    bestPredessor = q
        lattice[p] = (bestLength,bestPredessor)
        # print bestLength,p,bestPredessor
    bestLength,p = max( [ (lattice[p][0],p) for p in pairs ] )
    chain = []
    while p :
        chain.append(p)
        length,p = lattice[p]
    chain.reverse()
    return chain 

# Greedy algorithm
# Its second return value is True if maximalChunkSize could not be obeyed somewhere.
def selectFromChain( chain, maximalChunkSize ) :
    forced = False
    filteredChain = []
    for ind,p in enumerate(chain) :
        if ind==0 :
            assert p==(0,0)
            filteredChain.append(p)
            cursor = p
            continue
        if p[0]-cursor[0]>maximalChunkSize or p[1]-cursor[1]>maximalChunkSize :
            lastPos = chain[ind-1] if ind!=0 else (0,0)
            if lastPos!=cursor :
                filteredChain.append(lastPos)
            else :
                # we were forced to move more than maximalChunkSize
                filteredChain.append(p)
                forced = True
            cursor = filteredChain[-1]
            
    # we include the last element regardless, because
    # by convention it marks the end of the corpora.
    if filteredChain[-1]!=chain[-1] :
        filteredChain.append(chain[-1])
    return filteredChain,forced


def posetDump(chain, pairs, huLines, enLines, outputFilename) :
    log("Writing status of poset elements into file "+outputFilename+".poset")
    dropFile = file(outputFilename+".poset","w")
    chainSet = set(chain)
    for p in pairs :
        status = "used" if p in chainSet else "dropped"
        huDrop,enDrop = p
        if huDrop<len(huLines) and enDrop<len(enLines) and huDrop+enDrop>0 :
            dropFile.write( "%s\t%d\t%d\t%s\t%s\n" %
                ( status, huDrop, enDrop, huLines[huDrop], enLines[enDrop] )
            )
    dropFile.close()


# Returns a thinned chain: a list of pairs of indices.
# It also returns the unthinned version, for future reference (posetDump).
def partialAlign(huLines,enLines,maximalChunkSize) :
    huCorpus = map( lambda l : l.strip().split() , huLines )
    enCorpus = map( lambda l : l.strip().split() , enLines )

    huFreq = tokenFreq(huCorpus)
    enFreq = tokenFreq(enCorpus)
    huHap = hapaxes(huFreq)
    enHap = hapaxes(enFreq)
    commonHap = huHap & enHap
    huPositions = hapaxPositions(huHap,huCorpus)
    enPositions = hapaxPositions(enHap,enCorpus)

    pairs = []
    for t in commonHap :
#       print "%d\t%d\t%s" % (huPositions[t],enPositions[t],t)
        pairs.append( (huPositions[t],enPositions[t]) )

    pairs.append((0,0))
    # by convention, we include this to mark the end of the corpora
    # luckily it is always < comparable to every other element,
    # so maximalChain never forgets to include it.
    # this is not true for (0,0)!
    corpusSizes = (len(huCorpus),len(enCorpus))
    pairs.append(corpusSizes)

    pairs = uniqSort(pairs)

    log("Computing maximal chain in poset...")
    chain = maximalChain(pairs)
    log("Done.")
    log("%d long chain found in %d sized poset." % (len(chain),len(pairs)) )

    if maximalChunkSize>0 :
        log( "Selecting at most %d sized chunks..." % maximalChunkSize )
        chain,forced = selectFromChain( chain, maximalChunkSize )
        log( "%d chunks selected." % len(chain) )
        log("Done.")
        if forced :
            log("WARNING: maximalChunkSize could not be obeyed.")

    return chain,pairs

def strInterval( corpus, start, end ) :
    return "\n".join(corpus[start:end]) + "\n"

def writeSubcorpora(chain, outputFilename, huLangName, enLangName, huLines, enLines) :
    lastPos = (0,0)
    ind = 1
    for pos in chain :
        if pos==lastPos :
            continue
        baseFilename = outputFilename + "_" + str(ind)
        huSubCorpus = strInterval( huLines, lastPos[0], pos[0] )
        enSubCorpus = strInterval( enLines, lastPos[1], pos[1] )

        huFilename = baseFilename + "." + huLangName
        huFile = file( huFilename, "w" )
        huFile.write(huSubCorpus)
        huFile.close()

        enFilename = baseFilename + "." + enLangName
        enFile = file( enFilename, "w" )
        enFile.write(enSubCorpus)
        enFile.close()

        print huFilename +"\t"+ enFilename +"\t"+ baseFilename+".align"

        lastPos = pos
        ind += 1


def main() :
    if len(sys.argv) not in (6,7) :
        log("A preprocessor for hunalign.")
        log("Cuts a very large sentence-segmented unaligned bicorpus into smaller parts manageable by hunalign.")
        log("")
        log("Usage: partialAlign.py huge_text_in_one_language huge_text_in_other_language output_filename name_of_first_lang name_of_second_lang [ maximal_size_of_chunks=5000 ] > hunalign_batch")
        log("")
        log("The two input files must have one line per sentence. Whitespace-delimited tokenization is preferred.")
        log("The output is a set of files named output_filename_[123..].name_of_lang")
        log("The standard output is a batch job description for hunalign, so this can and should be followed by:")
        log("hunalign dictionary.dic -batch hunalign_batch")
        sys.exit(-1)

    if len(sys.argv)==7 :
        maximalChunkSize = int(sys.argv[6])
    else :
        maximalChunkSize = 5000
    
    huFilename,enFilename,outputFilename,huLangName,enLangName = sys.argv[1:6]

    log("Reading corpora...")
    huLines = map( lambda l : l.strip("\n") , file(huFilename).readlines() )
    enLines = map( lambda l : l.strip("\n") , file(enFilename).readlines() )
    log("Done.")

    chain,pairs = partialAlign(huLines,enLines,maximalChunkSize)

    posetDump(chain, pairs, huLines, enLines, outputFilename)

    debug = False
    if debug :
        justResult = True
        if justResult :
            chainToPrint = chain[:-1]
        else :
            chainToPrint = pairs[:-1]
        for huPos,enPos in chainToPrint :
            s = huLines[huPos] + "\t" + enLines[enPos]
            if justResult :
                print s
            else :
                if (huPos,enPos) in chain :
                    s += "\t<<<<<<<<"
                print s
                print
    else :
        justPrintChain = False
        if justPrintChain :
            for p in chain :
                print p[0],p[1]
        else :
            log("Writing subcorpora to files...")
            writeSubcorpora(chain, outputFilename, huLangName, enLangName, huLines, enLines)
            log("Done.")

if __name__ == '__main__': 
    main()
