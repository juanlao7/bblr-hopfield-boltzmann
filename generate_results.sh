#!/bin/sh
SAMPLES=2

mkdir -p out/results
cd src

for i in `seq $SAMPLES`
do
	echo
	echo "###### SAMPLE $i ######"
	echo

	python -m bblr.Main --out ../out/results/$i.json --seed $i ../config/pattern/final.json ../config/model/final.json ../config/input/final.json
done

