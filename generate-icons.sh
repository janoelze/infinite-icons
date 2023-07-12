#!/bin/bash

clean_yaml(){
  sed -i '' '/^```/d' "$1"
}

unlink_icons(){
  rm -rf icons
  mkdir icons
}

generate_icon_ids(){
  llm "Output 20 icons potentially included in a large web icon set. The names should contain descriptive IDs. Output each line starting with a "*" star. The filname should only contain the desceriptive icon ID. Make the icons non-obvious. For example: icon-home.svg, icon-pencil.svg and so forth. NEVER respond with prose. NEVER respond with markdown. NEVER respond with comments, NEVER respond with notes." >> icons.txt
}

generate_icon(){
  icon=$1
  echo "Generating icon '$icon'..."
  echo "The icon you are creating is called '$icon.svg'. The SVG element should have the class 'icon icon-$icon'." | llm --system "You are an icon creation engine. Only output valid SVG code. NEVER respond with prose. NEVER respond with markdown. NEVER respond with comments, NEVER respond with notes. Only output valid SVG." -m gpt-4 > "icons/$icon.svg"
  clean_yaml "icons/$icon.svg"
}

generate_icons(){
  i=0
  icons_index="icons.txt"
  while read line; do
    if [[ $line == \** ]]; then
      raw_icon=${line:1}
      basename=$(basename $raw_icon)
      icon=${basename%.*}
      path="icons/$icon.svg"
      if [ ! -f $path ] && [ $i -lt 3 ]; then
        generate_icon $icon
        i=$((i+1))
      fi
    fi
  done < $icons_index
}

trap "exit" INT
generate_icon_ids
# unlink_icons
generate_icons
