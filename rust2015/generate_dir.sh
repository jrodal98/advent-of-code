#!/bin/bash

rs_template_file=$(realpath template.rs)
solutions='solutions'
day_dir_base='day'

mkdir -p "$solutions"

# compute number of "day" directories that already exist
num_directories_created=$(fd $day_dir_base $solutions | wc -w)
# compute the number for the next day director
day_num=$((num_directories_created + 1))
# we are going to pad day_num with 0s
zeros="00"
day_num_zero_padded="${zeros:${#day_num}:${#zeros}}${day_num}"
# construct directory name
directory_name="${solutions}/${day_dir_base}$day_num_zero_padded"

mkdir "$directory_name"
cd "$directory_name" || exit
cargo init
cargo add anyhow
mkdir data

sample_file="data/sample.txt"
echo "Paste sample input here (and delete this line!)" >"$sample_file"
${VISUAL:-${EDITOR:-vi}} "$sample_file"

read -rp 'Sample solution: ' sample_solution

input_file="data/input.txt"
if [ -z "$AOC_SESSION" ]; then
  echo "Paste problem input here (and delete this line!)" >"$input_file"
  ${VISUAL:-${EDITOR:-vi}} "$input_file"
else
  curl --cookie "session=${AOC_SESSION}" "https://adventofcode.com/2015/day/$day_num/input" >"$input_file"
fi

rust_main_file="src/main.rs"

sed "s/PART1_SAMPLE_SOLUTION/$sample_solution/" "$rs_template_file" >"$rust_main_file"

${VISUAL:-${EDITOR:-vi}} "$rust_main_file" "$sample_file" "$input_file"
