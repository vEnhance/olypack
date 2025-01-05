#!/bin/bash

texmfhome=$(kpsewhich -var-value=TEXMFHOME)

if [ -z "$texmfhome" ]; then
  echo "Error: TEXMFHOME directory could not be determined."
  exit 1
fi

fetch_file() {
  local filename="$1"
  local url="$2"

  if [[ "$filename" == *.asy ]]; then
    local asydir="$HOME/.asy"

    local found_files
    found_files=$(find "$asydir" -name "$filename" -print -quit 2>/dev/null)

    if [ -n "$found_files" ]; then
      echo "The file '$filename' was found at '$found_files'."
    else
      echo "'$filename' was not found in '$asydir'. Downloading..."

      mkdir -p "$asydir"

      if curl -fLs "$url" -o "$asydir/$filename"; then
        echo "'$filename' has been successfully downloaded to '$asydir/$filename'."
      else
        echo "Warning: Failed to download '$filename' from $url (HTTP error)."
      fi
    fi

  else
    local found_files
    found_files=$(find "$texmfhome" -name "$filename" -print -quit 2>/dev/null)

    if [ -n "$found_files" ]; then
      echo "The file '$filename' was found at '$found_files'."
    else
      local default_path="$texmfhome/tex/latex/$filename"

      echo "'$filename' was not found in '$texmfhome'. Downloading to '$default_path'..."

      mkdir -p "$(dirname "$default_path")"

      if curl -fLs "$url" -o "$default_path"; then
        echo "'$filename' has been successfully downloaded to '$default_path'."
      else
        echo "Warning: Failed to download '$filename' from $url (HTTP error)."
      fi
    fi
  fi
}

fetch_file "evan.sty" "https://raw.githubusercontent.com/vEnhance/dotfiles/main/texmf/tex/latex/evan/evan.sty"
fetch_file "TST.sty" "https://raw.githubusercontent.com/vEnhance/dotfiles/main/texmf/tex/latex/TST/TST.sty"
fetch_file "natoly.sty" "https://raw.githubusercontent.com/vEnhance/dotfiles/main/texmf/tex/latex/TST/natoly.sty"
fetch_file "von.sty" "https://raw.githubusercontent.com/vEnhance/dotfiles/main/texmf/tex/latex/von/von.sty"
fetch_file "olympiad.asy" "https://raw.githubusercontent.com/vEnhance/dotfiles/main/asy/olympiad.asy"

mktexlsr "$texmfhome"
