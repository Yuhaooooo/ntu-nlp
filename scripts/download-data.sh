#!/usr/bin/env bash

filenames=(data.tar.gz)
fileids=(1pkvBtO7B8suZx-tYttlUNcCoP4WPsWLr)
unzip_paths=(core/)

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
  tar xvzf "${filenames[i]}"
  # Go back
  rm "${filenames[i]}"
  cd - || return 1
done
