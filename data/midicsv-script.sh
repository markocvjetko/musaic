#/bin/bash
for i in $(find . -name '*.mid');
do
    midicsv $i ${i%.mid}'.csv'
done;
