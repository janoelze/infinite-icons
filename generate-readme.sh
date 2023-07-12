#!/bin/bash

create_readme() {
  echo "# Icons" > README.md
  echo "" >> README.md
  echo "| <img width=\"100px\"/> | <img width=\"100px\"/> | <img width=\"100px\"/> | <img width=\"100px\"/> |" >> README.md
  echo "| ---- | ---- | ---- | ---- |" >> README.md
  row=""
  titles=""
  for icon in icons/*.svg; do
    iconname=$(basename "$icon")
    iconname=${iconname%.*}
    row="$row| <img src=\"$icon\" alt=\"$iconname\" width=\"100px\"/> "
    titles="$titles| $iconname "
    if [ $(echo "$row" | wc -w) -eq 8 ]; then
      echo "$row" >> README.md
      echo "$titles" >> README.md
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