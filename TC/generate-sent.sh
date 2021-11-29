#!/usr/bin/env bash

mkdir data/PS_sentences/
mkdir data/PS_sentences/data
mkdir data/PS_sentences/data/TC

mkdir data/DS_sentences/
mkdir data/DS_sentences/data
mkdir data/DS_sentences/data/DS


echo "####4.1 ----> Generate sentences from DS trees"

#for i in {1..1953}; do cat data/DS/s$i.txt | cut -f2 | sed 's/^$/EOL/g' | paste -sd ' ' | sed 's/ EOL /\n/g' | sed 's/ EOL$//g' > data/DS-sentences/s$i.txt ; done

for file in data/DS/* ; do cat $file | cut -f2 | sed 's/^$/EOL/g' | paste -sd ' ' | sed 's/ EOL /\n/g' | sed 's/ EOL$//g' > data/DS_sentences/$file ; done


echo "####4.2 ----> Generate sentences from PS trees"

#for i in {1..1953}; do cat data/TC/tree_ps_s$i.txt | sed "s/\[./(/g" | sed 's/\]/)/g' | sed 's/(-NONE-[^)]*)//g'  |  sed 's/([^ ]* //g;s/)//g'  |  sed 's/  */ /g;s/^ *//;s/ *$//;'  |  sed 's/!unf! *//g' | sed 's/\r$//g' | awk '{$1=$1};1' | sed '/^$/d' | sed 's/HYP/-/g' | sed 's/RB/)/g' | sed 's/LB/(/g' > data/PS-sentences/s$i.txt ; done

for file in data/TC/*; do cat $file | sed "s/\[./(/g" | sed 's/\]/)/g' | sed 's/(-NONE-[^)]*)//g'  |  sed 's/([^ ]* //g;s/)//g'  |  sed 's/  */ /g;s/^ *//;s/ *$//;'  |  sed 's/!unf! *//g' | sed 's/\r$//g' | awk '{$1=$1};1' | sed '/^$/d' | sed 's/HYP/-/g' | sed 's/RB/)/g' | sed 's/LB/(/g' > data/PS_sentences/$file ; done



echo "####4.3 ----> Comparing sentences DS vs PS"

mkdir data/PS-sentences
mkdir data/DS-sentences
mv data/DS_sentences/data/DS/* data/DS-sentences/
mv data/PS_sentences/data/TC/* data/PS-sentences/
rm -r data/DS_sentences
rm -r data/PS_sentences

cd data/PS-sentences/
rename "s/.*_//" *
cd ../../

#for i in {1..1953}; do echo "s"$i; diff data/DS-sentences/s$i.txt data/PS-sentences/tree_ps_s$i.txt ; done > diff-result.txt
diff data/DS-sentences/ data/PS-sentences/ > diff-result.txt
