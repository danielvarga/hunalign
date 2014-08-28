from StringIO import StringIO

from teed import *

cmd = ["./testProcess.sh"]
cmd = ["./testProcess-RealHunalign.sh"]

ladderDir = '../regtest/handaligns/1984.ro.utf8/'

cmd = ['../src/hunalign/hunalign', '-utf',
'-hand='+ladderDir+'hand.ladder', '../data/null.dic', ladderDir+'/hu.pre', ladderDir+'/en.pre', '-bisent', '-realign']

fout, ferr = StringIO(), StringIO()
exitcode = teed_call(cmd, stdout=fout, stderr=ferr)
stdout = fout.getvalue()
stderr = ferr.getvalue()

# print len(stdout),len(stderr)

print stderr
