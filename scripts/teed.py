# http://stackoverflow.com/questions/4984428/python-subprocess-get-childrens-output-to-file-and-terminal/4985080#4985080
# Thanks http://stackoverflow.com/users/4279/j-f-sebastian

import sys
from subprocess import Popen, PIPE
from threading  import Thread

def tee(infile, *files):
    """Print `infile` to `files` in a separate thread."""
    def fanout(infile, *files):
        for line in iter(infile.readline, ''):
            for f in files:
                f.write(line)
        infile.close()
    t = Thread(target=fanout, args=(infile,)+files)
    t.daemon = True
    t.start()
    return t

def teed_call(cmd_args, **kwargs):    
    stdout, stderr = [kwargs.pop(s, None) for s in 'stdout', 'stderr']
    p = Popen(cmd_args,
              stdout=PIPE if stdout is not None else None,
              stderr=PIPE if stderr is not None else None,
              **kwargs)
    threads = []
    # Here I changed Sebastian's original version, because I don't want to tee stdout, just stderr:
    # ORIGINAL:
    # if stdout is not None: threads.append(tee(p.stdout, stdout, sys.stdout))
    # MINE:
    if stdout is not None: threads.append(tee(p.stdout, stdout))

    if stderr is not None: threads.append(tee(p.stderr, stderr, sys.stderr))
    for t in threads: t.join() # wait for IO completion
    return p.wait()


if __name__ == '__main__':
    outf, errf = open('out.txt', 'w'), open('err.txt', 'w')
    assert not teed_call(["cat", __file__], stdout=None, stderr=errf)
    assert not teed_call(["echo", "abc"], stdout=outf, stderr=errf, bufsize=0)
    assert teed_call(["gcc", "a b"], close_fds=True, stdout=outf, stderr=errf)

