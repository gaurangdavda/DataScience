#!/bin/bash

python3.5 /src/hw1_part1/problem1.py $CIK  $ACCESSION

mv /src/hw1_part1/*zip /src/hw1_part1/generatedFiles
mv /src/hw1_part1/Edgar*.txt /src/hw1_part1/generatedFiles

if [ $? -eq 0 ]
then
  echo "Successfully created file"
  sh /src/hw1_part1/awsS3.sh $1 $2 $3
else
  echo "Could not create file" >&2
fi
