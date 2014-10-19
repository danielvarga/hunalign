echo "Starting tokenization"
date

find tree/sentence/ -type f | while read f
do
    t=`echo $f | sed "s/^tree\/sentence/tree\/tok/"`
    cat "$f" | bash hunalign/scripts/tok.one.sh > "$t"
done

echo "Starting sentence count verification"
date

find tree/sentence/ -type f | while read f
do
    t=`echo $f | sed "s/^tree\/sentence/tree\/tok/"`
    lSen=`wc -l < $f`
    lStrip=`wc -l < $t`
    if [ "$lSen" -ne "$lStrip" ]
    then
	echo Mismatch: $f $lSen $t $lStrip 
    fi
done

echo "Done."
date
