#!/bin/bash

awk 'BEGIN { for (i=1;i<100;++i) { if (i%20==0) { print "Working on number",i > "/dev/stderr" } ; s += i ; print s } }'
