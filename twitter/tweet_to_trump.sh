#!/bin/bash 
t update "@realDonaldTrump This is a tweet sent from a script as a test #ICHack17 bant/10?"
t timeline --number=1 -l > test.txt
i="0"
touch test.txt
while [ $i -le 0 ]
do
    i=$(cat test.txt | awk '{print $1;}' | xargs t status | awk 'NR > 5 { print }' | awk 'NR < 2 { print}' | awk '{print $2;}')
done
echo "This is where a sicccck webhook would go"
# Here is where I do things
#echo $tweets
