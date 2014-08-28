#!/bin/bash

bindir=../src/hunalign


fscorer() {
    prec=`cat $1 | grep "^Precision" | tr -d ',' | cut -f2 -d' '`
    recall=`cat $1 | grep "^Precision" | tr -d ',' | cut -f4 -d' '`
    fscore=`echo "2/(1/$prec+1/$recall)" | bc -l | awk '{ print $0+0 }'`
    echo "F-score: $fscore"
    echo
}

evaluator() {
    echo "=================================="
    echo "Expected:"
    cat $1 | tail -3
    fscorer $1
    targetfscore=$fscore
    echo "Achieved:"
    cat $2 | tail -3
    fscorer $2
    targetfscore=$targetfscore fscore=$fscore awk '
    BEGIN{
	print "Expected F-score:", ENVIRON["targetfscore"], " Achieved F-score:",ENVIRON["fscore"]
        if (ENVIRON["targetfscore"]>ENVIRON["fscore"])
	{
	    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> REGRESSION in F-score <<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
	}
	else
	{
	    print "No regression found"
        }
    }'
    echo
}

name=1984.ro.utf8.realign
echo "Testing $name ..."
target=targets/$name.cerr
file=results/$name.cerr
ofile=results/$name.cout
$bindir/hunalign -utf -realign -hand=handaligns/1984.ro.utf8/hand.ladder ../data/null.dic handaligns/1984.ro.utf8/hu.pre handaligns/1984.ro.utf8/en.pre -bisent > $ofile 2> $file
evaluator $target $file

name=1984.hu
echo "Testing $name ..."
target=targets/$name.cerr
file=results/$name.cerr
ofile=results/$name.cout
$bindir/hunalign -hand=handaligns/1984.hu/hand.ladder ../data/hu-en.dic handaligns/1984.hu.handstem/hu.pre handaligns/1984.hu.handstem/en.pre -bisent > $ofile 2> $file
evaluator $target $file

name=1984.hu.handstem.realign
echo "Testing $name ..."
target=targets/$name.cerr
file=results/$name.cerr
ofile=results/$name.cout
$bindir/hunalign -realign -hand=handaligns/1984.hu/hand.ladder ../data/hu-en.dic handaligns/1984.hu.handstem/hu.pre handaligns/1984.hu.handstem/en.pre -bisent > $ofile 2> $file
evaluator $target $file

name=steinbeck.huntoken.nopara
echo "Testing $name ..."
target=targets/$name.cerr
file=results/$name.cerr
ofile=results/$name.cout
$bindir/hunalign -hand=handaligns/steinbeck.huntoken.nopara/hand.ladder ../data/hu-en.dic handaligns/steinbeck.huntoken.nopara/hu.pre handaligns/steinbeck.huntoken.nopara/en.pre > $ofile 2> $file
evaluator $target $file

name=1984.ro.realign
echo "Testing $name ..."
target=targets/$name.cerr
file=results/$name.cerr
ofile=results/$name.cout
$bindir/hunalign -realign -hand=handaligns/1984.ro/hand.ladder ../data/null.dic handaligns/1984.ro/hu.pre handaligns/1984.ro/en.pre -bisent > $ofile 2> $file
evaluator $target $file

name=dtm.realign
echo "Testing $name ..."
target=targets/$name.cerr
file=results/$name.cerr
ofile=results/$name.cout
$bindir/hunalign -hand=handaligns/dtm/hand.ladder ../data/hu-en.dic handaligns/dtm/hu.pre handaligns/dtm/en.pre > $ofile 2> $file
evaluator $target $file
