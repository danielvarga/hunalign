#!/bin/bash

mkdir -p langpairs/batch

awk 'BEGIN {
langnum=0
while ( getline < "langs.txt" )
{
    lang[langnum]=$0
    ++langnum;
}

for (i=0; i<langnum-1; ++i )
{
for (j=i+1; j<langnum; ++j )
{
    l1=lang[i];
    l2=lang[j];
    print l1,l2
    system("cat langpairs/aligninfo/" l1 "-" l2 ".aligninfo | cut -f4,5,6 | sed s/ladder/ladder2/ > langpairs/batch/" l1 "-" l2 ".batch")
}
}

}'
