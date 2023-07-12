#!/bin/bash

create_readme(){
  # create a readme.md file
  # containing a markdown table of all icons, four per row

  echo "# Icons" > README.md
  echo "" >> README.md
  echo "|  |  |  |  |" >> README.md
  echo "| ---- | ---- | ---- | ---- |" >> README.md
  # iterate over icons/*.svg in chunks of four
  row=""
  titles=""
  for icon in icons/*.svg; do
    iconname=$(basename $icon)
    iconname=${iconname%.*}
    row="$row| ![$iconname]($icon) "
    titles="$titles| $iconname "
    if [ $(echo $row | wc -w) -eq 8 ]; then
      echo $row >> README.md
      echo $titles >> README.md
      row=""
      titles=""
    fi
  done
  echo "" >> README.md
}

create_overview(){
  for icon in icons/*.svg; do
    iconname=$(basename $icon)
    iconname=${iconname%.*}
    echo "<div class='icon'><div class='icon-name'>$iconname</div><div class='icon-svg'>$(cat $icon)</div></div>" >> icons.html
  done
}

create_readme
create_overview