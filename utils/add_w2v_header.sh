#!/bin/bash

N=$(wc -l $1 | cut -d " " -f 1)
DIM=$(($(head -n 1 $1 | tr " " "\n" | sed '/^$/d' | wc -l) - 1))

sed -i "1i$N $DIM" $1
