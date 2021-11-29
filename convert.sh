#!/usr/bin/env bash


cd CoNLL2SSF/
cp -r ../Input_data/ data/
mkdir data/SSF/

echo "#1 ----> CoNLL to SSF conversion in progress"
python3 main.py

cp -r data/ ../SSF2PS/
rm -r data/

cd ../SSF2PS/
mkdir data/PS

echo "#2 ----> SSF to PS conversion in progress"
python conversion.py 

cp -r data/ ../TC/
rm -r data/

cd ../TC/
mkdir data/PS-Braces
mkdir data/TC

echo "#3 ----> PS Tree fixing in progress"
python3 tree_from_ssf.py

echo "#4 ----> Evaluation is in progress"
./generate-sent.sh

echo "#5 ----> Congratulations! All trees have been successfuly converted. Check Result folder"
mkdir ../Output
mkdir ../Output/DS
mkdir ../Output/SSF
mkdir ../Output/PS
mkdir ../Output/TC
mkdir ../Output/DS-sentences
mkdir ../Output/PS-sentences

cp -r data/DS/* ../Output/DS
cp -r data/SSF/* ../Output/SSF
cp -r data/PS/* ../Output/PS
cp -r data/TC/* ../Output/TC
cp -r data/DS-sentences/* ../Output/DS-sentences
cp -r data/PS-sentences/* ../Output/PS-sentences
mv diff-result.txt ../Output/
rm -r data/
