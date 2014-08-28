#!/bin/bash

echo -n "Working... " > /dev/stderr
for (( i=1 ; i<10 ; ++i )) ; do
    sleep 1
    echo -n "$i " > /dev/stderr
done

echo "Done." > /dev/stderr
echo "End result 1"
echo "End result 2"
echo "End result 3"
