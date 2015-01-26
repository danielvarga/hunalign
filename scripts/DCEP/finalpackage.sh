#!/bin/bash

p=$1

cat langpairs/aligninfo/$p.aligninfo | cut -f1,4,5 | sed "s/\.\/tree\/tok\///g" > final/indices/$p
cd final
tar jcf packages/DCEP-$p.tar.bz2 aligns/$p indices/$p
# scp DCEP-$p.tar.bz2 kruso.mokk.bme.hu:./public_html/DCEP/langpairs/
cd ..
