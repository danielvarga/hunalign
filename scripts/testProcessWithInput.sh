awk '{ if (NR%100==0) { print "Working on line",NR > "/dev/stderr" } ; s += $0 ; print s }'
