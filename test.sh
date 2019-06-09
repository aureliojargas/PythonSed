#!/bin/bash

mkdir -p test-aurelio/scripts-{sedsed,pysed}
mkdir -p test-aurelio/parsing-{sedsed,pysed}

for f in ../sedsed/test/scripts/*.sed
do
    echo $f
    python3 ../sedsed/sedsed.py --indent -f $f \
        > test-aurelio/scripts-sedsed/$(basename $f)

    python3 aurelio.py $f | grep -v '^\[.*: .*\]$' \
        > test-aurelio/scripts-pysed/$(basename $f)
done

for f in ../sedsed/test/parsing/*.sed
do
    echo $f
    python3 ../sedsed/sedsed.py --indent -f $f \
        > test-aurelio/parsing-sedsed/$(basename $f)

    python3 aurelio.py $f | grep -v '^\[.*: .*\]$' \
        > test-aurelio/parsing-pysed/$(basename $f)
done

rm w.out[12]

diff -ur test-aurelio/parsing-{sedsed,pysed}
diff -ur test-aurelio/scripts-{sedsed,pysed}
