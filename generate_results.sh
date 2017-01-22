#!/bin/sh
SAMPLES=8

mkdir -p out/results
cd src

for i in `seq $SAMPLES`
do
	echo
	echo "###### SAMPLE $i ######"
	echo

	python -m bblr.Main --out ../out/results/$i.json --seed $i ../config/pattern/patterns.json ../config/model/models.json ../config/input/inputs.json &
done

