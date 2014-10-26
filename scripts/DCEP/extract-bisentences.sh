#!/bin/bash

mkdir langpairs
mkdir langpairs/raw
cat total.aligninfo.shuffled.limitin1000 | while read did l1 l2 tok1 tok2 ladder
do
    hunalign/scripts/ladder2text.py $ladder $tok1 $tok2 >> langpairs/raw/$l1-$l2 2>> cerr.ladder2text
done

mkdir langpairs/biqf
cat total.aligninfo.shuffled.limitin1000 | while read did l1 l2 tok1 tok2 ladder
do
    hunalign/scripts/ladder2text.py $ladder $tok1 $tok2 | hunalign/scripts/DCEP/filteralign.sh >> langpairs/biqf/$l1-$l2 2> /dev/null
done
