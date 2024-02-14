#!/bin/bash

texmfhome=$(kpsewhich -var-value=TEXMFHOME)

if [ -z "$texmfhome" ]; then
  echo "Error: TEXMFHOME directory could not be determined."
  exit 1
fi

fetch_file() {
  local filename="$1"
  local url="$2"
  local found_files=$(find "$texmfhome" -name "$filename" -print -quit)

  if [ ! -z "$found_files" ]; then
    echo "The file $filename was found at $found_files."
  else
    local default_path="$texmfhome/tex/latex/$filename"
    
    echo "$filename was not found. Downloading to $default_path..."
    
    mkdir -p "$(dirname "$default_path")"
    
    curl -Ls "$url" -o "$default_path"
    
    if [ -f "$default_path" ]; then
      echo "$filename has been successfully downloaded to $default_path."
    else
      echo "Error: Failed to download $filename."
      exit 1
    fi
  fi
}

fetch_file "evan.sty" "https://raw.githubusercontent.com/vEnhance/dotfiles/main/texmf/tex/latex/evan/evan.sty"
fetch_file "TST.sty" "https://raw.githubusercontent.com/vEnhance/dotfiles/main/texmf/tex/latex/TST/TST.sty"
fetch_file "natoly.sty" "https://raw.githubusercontent.com/vEnhance/dotfiles/main/texmf/tex/latex/TST/natoly.sty"
fetch_file "von.sty" "https://raw.githubusercontent.com/vEnhance/dotfiles/main/texmf/tex/latex/von/von.sty"

mktexlsr "$texmfhome"