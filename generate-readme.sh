#!/bin/bash

create_readme(){
  # create a readme.md file
  # containing a markdown table of all icons, four per row
  # with the icon name and the icon itself
  
  output="| Icon | Name |"
  output="$output\n| --- | --- |"
  for icon in icons/*.svg; do
    iconname=$(basename $icon)
    iconname=${iconname%.*}
    output="$output\n| ![$iconname](icons/$iconname.svg) | $iconname |"
  done
  echo -e "$output" > README.md
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