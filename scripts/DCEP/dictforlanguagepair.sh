#!/bin/bash

mkdir -p langpairs/autodict
mkdir -p langpairs/autodict.log

l1=$1
l2=$2

bi=langpairs/biqf/$l1-$l2

# I forgot to do this filtering step in the biqf creation step.
# I'm lazy and do it with byte length
cat $bi | awk '(length($0)<1000)' > tmp.bi

cat tmp.bi | cut -f1 > tmp.l1
cat tmp.bi | cut -f2 > tmp.l2

./acquisScripts/scripts/coocc.forAcquis -mc10 -ms40 tmp.l1 tmp.l2 2> langpairs/autodict.log/$l1-$l2 > langpairs/autodict/$l1-$l2.dic
