#!/bin/bash

# With an uncomfortable tie-in, it does several things:
# 1. creates the final directory structure.
# 2. restructures the flatly structured ladder files into a language-pair based structure.
# 3. gets rid of the unreliable quality values in the ladder files. (cut -f1,2)
# 4. makes the final filenames as simple as possible,
#    from flat/ladder/89/033089.ES.LT.ladder to final/aligns/ES-LT/033089

p=$1
if [ ${#p} -ne 5 ]
then
    echo "Usage: flatladdertolangpair.sh L1-L2"
    exit -1
fi

pdot=`echo $p | sed "s/-/./"`

targ=final/aligns
mkdir -p $targ/$p

sub=ladder2
find flat/$sub -type f | grep "$pdot" | sed "s/^flat\/$sub\///" | sed "s/\.ladder$//" | tr '/.' ' ' |\
while read dig id l1 l2
do
    cat flat/$sub/$dig/$id.$l1.$l2.ladder 2>> tmp/cerr.$p | cut -f1,2 > $targ/$l1-$l2/$id
done
