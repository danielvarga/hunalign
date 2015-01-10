#!/bin/bash

# flat/ladder2 already created.

mkdir -p langpairs/realign2.log

awk 'BEGIN {
langnum=0
while ( getline < "langs.txt" )
{
    lang[langnum]=$0
    ++langnum;
}

k=0

for (i=0; i<langnum-1; ++i )
{
for (j=i+1; j<langnum; ++j )
{
    ++k;
    if (k<=170) { continue }
    l1=lang[i];
    l2=lang[j];
    print l1,l2
    p = l1 "-" l2
    system("./hunalign/src/hunalign/hunalign -batch langpairs/fulldict/" p ".dic langpairs/batch2/" p ".batch 2> langpairs/realign2.log/" p )
}
}

}'
