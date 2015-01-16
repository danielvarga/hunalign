#!/bin/bash

# With an uncomfortable tie-in, it does several things:
# 1. creates the final directory structure.
# 2. restructures the flatly structured ladder files into a language-pair based structure.
# 3. gets rid of the unreliable quality values in the ladder files. (cut -f1,2)
# 4. makes the final filenames as simple as possible,
#    from flat/ladder/89/033089.ES.LT.ladder to final/aligns/ES-LT/033089

targ=final/aligns
mkdir -p $targ
ls langpairs/batch | cut -f1 -d'.' | while read p ; do mkdir $targ/$p ; done

sub=ladder
find flat/$sub -type f | sed "s/^flat\/$sub\///" | sed "s/\.ladder$//" | tr '/.' ' ' |\
while read dig id l1 l2
do
    cat flat/$sub/$dig/$id.$l1.$l2.ladder | cut -f1,2 > $targ/$l1-$l2/$id
done
