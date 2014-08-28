#!/bin/bash

ladderDir=../regtest/handaligns/1984.ro.utf8
../src/hunalign/hunalign -utf -hand=$ladderDir/hand.ladder ../data/null.dic $ladderDir/hu.pre $ladderDir/en.pre -bisent
