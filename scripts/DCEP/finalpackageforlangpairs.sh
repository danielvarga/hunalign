#!/bin/bash

mkdir -p final/indices
mkdir -p final/packages

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
    p = l1 "-" l2
    system("bash hunalign/scripts/DCEP/finalpackage.sh " p )
}
}

}'
