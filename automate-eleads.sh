#!/bin/bash

month="2"
year="18"
for date_item in {1..5}
do
python Eleads-history.py "${month}/0${date_item}/${year}"
done &


for date_item in {6..9}
do
python Eleads-history.py "${month}/0${date_item}/${year}"
done &


for date_item in {10..15}
do
python Eleads-history.py "${month}/${date_item}/${year}"
done &

for date_item in {16..20}
do
python Eleads-history.py "${month}/${date_item}/${year}"
done &

for date_item in {21..25}
do
python Eleads-history.py "${month}/${date_item}/${year}"
done &

for date_item in {26..28}
do
python Eleads-history.py "${month}/${date_item}/${year}"
done &
