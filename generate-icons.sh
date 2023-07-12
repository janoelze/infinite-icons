#!/bin/bash

MAX_PROCESSES=10
SEMAPHORE=0

clean_yaml(){
  sed -i '' '/^```/d' "$1"
}

unlink_icons(){
  rm -rf icons
  mkdir icons
}

generate_icon(){
  iconname=$1
  echo "The icon you are creating is called '$iconname.svg'. The SVG element should have the class 'icon icon-$iconname'." | llm --system "You are an icon creation engine. Only output valid SVG code. NEVER respond with prose. NEVER respond with markdown. NEVER respond with comments, NEVER respond with notes. Only output valid SVG." -m gpt-4 > "icons/$iconname.svg"
  clean_yaml "icons/$iconname.svg"
  # Release the semaphore
  ((SEMAPHORE--))
}

generate_icons(){
  ICONS_FILE_PATH="icons.txt"
  while read line; do
    basename=$(basename $line)
    iconname=${basename%.*}

    # Wait until a slot is available in the semaphore
    while [ $SEMAPHORE -ge $MAX_PROCESSES ]; do
      sleep 1
    done

    # Acquire the semaphore
    ((SEMAPHORE++))

    generate_icon $iconname &
    wait
  done < $ICONS_FILE_PATH

  wait
}

trap "exit" INT
unlink_icons
generate_icons
