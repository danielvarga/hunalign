#!/bin/bash

cut -f1,2 | grep -v "@" | awk '{ print $2,"@",$1 }'
