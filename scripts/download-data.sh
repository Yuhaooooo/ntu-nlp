#!/usr/bin/env bash

filenames=(data.zip)
fileids=(1Xu-BAztca_HduVoU2h-LcQpfI1gcau0Q)
unzip_paths=(core/data)

for i in $(seq 0 0);
do
  cd "${unzip_paths[i]}" || return 1
  echo "Download ${filenames[i]}"
  # Download
  curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileids[i]}" > /dev/null
  curl -Lb ./cookie \
      "https://drive.google.com/uc?export=download&confirm=$(awk '/download/ {print $NF}' ./cookie)&id=${fileids[i]}" \
      -o "${filenames[i]}"
  rm cookie
  unzip "${filenames[i]}"
  # Go back
  rm "${filenames[i]}"
  cd - || return 1
done
