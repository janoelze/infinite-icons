#!/bin/bash

clean_yaml(){
  sed -i '' '/^```/d' "$1"
}

unlink_icons(){
  rm -rf icons
  mkdir icons
}

generate_icon(){
  icon=$1
  echo "Generating icon '$icon'..."
  echo "The icon you are creating is called '$icon.svg'. The SVG element should have the class 'icon icon-$icon'." | llm --system "You are an icon creation engine. The theme is dystopian. Only output valid SVG code. NEVER respond with prose. NEVER respond with markdown. NEVER respond with comments, NEVER respond with notes. Only output valid SVG." -m gpt-4 > "icons/$icon.svg"
  clean_yaml "icons/$icon.svg"
}

generate_icons(){
  icons_index="icons.txt"
  while read line; do
    basename=$(basename $line)
    icon=${basename%.*}
    generate_icon $icon
  done < $icons_index
}

trap "exit" INT
unlink_icons
generate_icons
