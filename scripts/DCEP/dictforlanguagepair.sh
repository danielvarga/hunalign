#!/bin/bash

mkdir -p langpairs/autodict
mkdir -p langpairs/autodict.log

l1=$1
l2=$2

bi=langpairs/biqf/$l1-$l2

cat $bi | cut -f1 > tmp.l1
cat $bi | cut -f2 > tmp.l2

./acquisScripts/scripts/coocc.forAcquis -mc20 -ms40 tmp.l1 tmp.l2 2> langpairs/autodict.log/$l1-$l2 > langpairs/autodict/$l1-$l2.dic
