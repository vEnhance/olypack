#!/bin/bash

# Get the directory of this script
# https://stackoverflow.com/questions/59895/getting-the-source-directory-of-a-bash-script-from-within
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR" || exit
cp -r template/* ..
mv ../gitignore ../.gitignore

mkdir -p ../notes ../output ../source

cp .pre-commit-config.yaml ..
