#!/bin/bash

grep -v "~~~" | grep -v "<p>" | awk 'BEGIN {FS="\t"} { ra = ( length($2)>length($3) ? (length($2)+10)/(length($3)+10) : (length($3)+10)/(length($2)+10) ) ; if ((ra<1.5)&&($2!=$3)) print $2 "\t" $3 }'
