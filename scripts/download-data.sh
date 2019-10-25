#!/usr/bin/env bash

filenames=(data.csv)
fileids=(1ay53rIluB334-RUqn28GR-QI6HxutJ6H)
unzip_paths=(core/data)

for i in $(seq 0);
do
  cd "${unzip_paths[i]}" || return 1
  echo "Download ${filenames[i]}"
  # Download
  curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileids[i]}" > /dev/null
  curl -Lb ./cookie \
      "https://drive.google.com/uc?export=download&confirm=$(awk '/download/ {print $NF}' ./cookie)&id=${fileids[i]}" \
      -o "${filenames[i]}"
  rm cookie
  # Unzip
  tar xvzf "${filenames[i]}" 2> /dev/null
  rm -f "${filenames[i]}"
  # Go back
  cd - || return 1
done
