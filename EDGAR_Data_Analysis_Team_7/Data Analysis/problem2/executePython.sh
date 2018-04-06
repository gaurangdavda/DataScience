#!/bin/bash

python3.5 /src/hw1_part2/problem2.py $YEAR

mv /src/*zip /src/hw1_part2/generatedFiles
mv /src/Edgar*.txt /src/hw1_part2/generatedFiles

if [ $? -eq 0 ]
then
  echo "Successfully created file"
  sh /src/hw1_part2/awsS3.sh $1 $2 $3
else
  echo "Could not create file" >&2
fi
