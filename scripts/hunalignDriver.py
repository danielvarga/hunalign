from StringIO import StringIO

from teed import *

from partialAlign import *


OUTPUT_FILENAME="tmp/tmp_chunk"
BATCH_JOB_FILENAME = "tmp/tmp_batch"
MAXIMAL_CHUNK_SIZE = 1000


def parseLadderData(fileContent) :
    ls = fileContent.split("\n")
    if ls[-1]=="" :
        del ls[-1]

    result = []
    for l in ls :
        a = l.split()
        if len(a)!=3 :
            raise Exception("hunalign should return 3-column data.")
        result.append((int(a[0]),int(a[1]),float(a[2])))

    return result

def serializeLadderData(ladder) :
    def serializeLine(l) :
        return "\t".join(map(str,l))
    return "\n".join( map(serializeLine, ladder) ) + "\n"

def hunalignDriver(hunalignExecutablePath, hunalignArgs) :

    cmd = [ hunalignExecutablePath ] + hunalignArgs

    fout, ferr = StringIO(), StringIO()
    exitcode = teed_call(cmd, stdout=fout, stderr=ferr)
    stdout = fout.getvalue()
    stderr = ferr.getvalue()

    if exitcode!=0 :
        raise Exception("hunalign returned with exit code "+str(exitcode))

    result = parseLadderData(stdout)

    return result, stderr


def batchHunalignDriver(hunalignExecutablePath, hunalignArgs) :
    cmd = [ hunalignExecutablePath, "-batch" ] + hunalignArgs

    fout, ferr = StringIO(), StringIO()
    exitcode = teed_call(cmd, stdout=fout, stderr=ferr)
    stdout = fout.getvalue()
    stderr = ferr.getvalue()

    if exitcode!=0 :
        raise Exception("hunalign returned with exit code "+str(exitcode))

    assert len(stdout)==0


def partialAlignDriver(huFilename, enFilename) :
    chain,stdout = partialAlignWithIO(huFilename, enFilename, outputFilename=OUTPUT_FILENAME, huLangName="a", enLangName="b", maximalChunkSize=MAXIMAL_CHUNK_SIZE)
    return chain,stdout

def fullStack(hunalignExecutablePath, huFilename, enFilename, dictFilename) :
    chain,stdout = partialAlignDriver(huFilename, enFilename)

    with open(BATCH_JOB_FILENAME,'w') as f :
        f.write(stdout)

    extraCareful = True
    if extraCareful :
        # Output should arrive in files named OUTPUT_FILENAME +"_"+ str(number) +"."+ ("a" if hu else "b")
        chunkNumber = len(chain)-1
        huSenCnt = 0
        enSenCnt = 0
        for chunkId in range(1,chunkNumber+1) :
            chunkFilename = "%s_%d." % (OUTPUT_FILENAME, chunkId)
            huChunkFilename = chunkFilename+"a"
            enChunkFilename = chunkFilename+"b"
            with open(huChunkFilename) as huChunkFile :
                huSenCnt += len(huChunkFile.readlines())
            with open(enChunkFilename) as enChunkFile :
                enSenCnt += len(enChunkFile.readlines())
            assert chain[chunkId] == (huSenCnt,enSenCnt)

    hunalignArgs = [ dictFilename, BATCH_JOB_FILENAME ]
    batchHunalignDriver(hunalignExecutablePath, hunalignArgs)

    # Output should now arrive in files named OUTPUT_FILENAME +"_"+ str(number) + ".align"

    totalLadder = []
    for chunkId in range(1,chunkNumber+1) :
        alignChunkFilename = "%s_%d.align" % (OUTPUT_FILENAME, chunkId)
        chunkStarts = chain[chunkId-1]
        huStart,enStart = chunkStarts
        if len(totalLadder)>0 :
            if totalLadder[-1][:2] != chunkStarts :
                log( "ERROR: In %s rung %s should match with %s" % (alignChunkFilename, str(totalLadder[-1]), chunkStarts) )
                raise Exception("chunk aligns inconsistent with chunking data")

            # The last element of the ladder is only there to mark the size of the who bidocument.
            # Supposedly it's quality value is always 0.3 (We don't check this.)
            del totalLadder[-1]
        try :
            with open(alignChunkFilename) as f :
                chunkLadder = parseLadderData(f.read())
                assert chunkLadder[0][:2] == (0,0)
                for rung in chunkLadder :
                    huStep,enStep,quality = rung
                    totalLadder.append( (huStart+huStep, enStart+enStep, quality) )
        except IOError :
            log( "ERROR: %s missing, hunalign probably gave up on input" % alignChunkFilename)
            raise Exception("chunk align missing")

    sys.stdout.write(serializeLadderData(totalLadder))

def testBatchHunalign() :
    hunalignExecutablePath = '../src/hunalign/hunalign'
    hunalignArgs = ['../data/null.dic', 'batch.job']
    batchHunalignDriver(hunalignExecutablePath, hunalignArgs)


def testHunalign() :
    hunalignExecutablePath = '../src/hunalign/hunalign'
    ladderDir = '../regtest/handaligns/1984.ro.utf8/'
    hunalignArgs = [ '-hand='+ladderDir+'hand.ladder', '../data/null.dic', ladderDir+'/hu.pre', ladderDir+'/en.pre' ]

    result,stderr = hunalignDriver(hunalignExecutablePath, hunalignArgs)

    print "\n".join(map(str,result))


def testFullStack() :
    hunalignExecutablePath = '../src/hunalign/hunalign'
    ladderDir = '../regtest/handaligns/1984.ro.utf8/'
    huFilename, enFilename, dictFilename = ( ladderDir+'/hu.pre', ladderDir+'/en.pre', '../data/null.dic' )

    fullStack(hunalignExecutablePath, huFilename, enFilename, dictFilename)

def main() :
    # testHunalign()
    # testBatchHunalign()
    testFullStack()

if __name__=='__main__' :
    main()
