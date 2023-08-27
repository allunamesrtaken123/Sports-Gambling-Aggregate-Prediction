#!/usr/bin/env bash

COUNT=0

while [ $COUNT -lt 5 ]
do
    python3 /Users/aaronfoote/Documents/GitHub/Sports-Gambling-Aggregate-Prediction/tennisScraper.py
    sleep 1200
    ((COUNT++))
done

echo "while loop finished"
exit 0