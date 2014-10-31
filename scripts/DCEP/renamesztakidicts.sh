#!/bin/bash

mkdir -p langpairs/sztaki

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
    ll1 = tolower(l1)
    ll2 = tolower(l2)
    print l1,l2
    system("cp hlt.sztaki.dicts/" ll1 "_" ll2 " langpairs/sztaki/" l1 "-" l2 ".dic" )
}
}

}'
