#!/bin/bash

set -e

# quantifies the difference between align and realign for a given language pair

p=$1
seed=$2
if [ -z "$seed" ]; then seed=0 ; fi

cat langpairs/aligninfo/$p.aligninfo | cut -f6 | awk -v seed=$seed '(NR%100==seed)' > tmp/$p.ladsam
cat tmp/$p.ladsam | xargs cat | cut -f1,2 > tmp/$p.ladcat
cat tmp/$p.ladsam | sed "s/ladder/ladder2/" | xargs cat | cut -f1,2 > tmp/$p.ladcat2
l1=`wc -l < tmp/$p.ladcat`
l2=`wc -l < tmp/$p.ladcat2`
d=`diff tmp/$p.ladcat tmp/$p.ladcat2 | wc -l`
echo $p $l1 $l2 $d
