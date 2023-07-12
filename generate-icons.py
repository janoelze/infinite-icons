import os, sys, random
import subprocess, threading

def clean_svg_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    with open(file_path, 'w') as file:
        for line in lines:
            if not line.startswith('```'):
                file.write(line)

def generate_icon_ids():
    output = subprocess.check_output(['llm', 'Output 15 icons potentially included in a large web icon set. The names should contain descriptive IDs. Make them non-obvious. Output each line starting with a "*" star. The filname should only contain the desceriptive icon ID. For example: icon-home.svg, icon-pencil.svg and so forth. NEVER respond with prose. NEVER respond with markdown. NEVER respond with comments, NEVER respond with notes.'], text=True)
    with open('icons.txt', 'a+') as file:
        file.write(output)

def generate_icon(icon):
    print(f"Generating icon '{icon}'...")
    prompt = f"The icon you are creating is called '{icon}.svg'. The SVG element should have the class 'icon icon-{icon}'."
    output = subprocess.check_output(['llm', '--system', f"You are an icon creation engine. Only output valid SVG code. NEVER respond with prose. NEVER respond with markdown. NEVER respond with comments, NEVER respond with notes. Only output valid SVG.", '-m', 'gpt-4', prompt], text=True)
    with open(f"icons/{icon}.svg", 'w') as file:
        file.write(output)
    clean_svg_file(f"icons/{icon}.svg")

def get_missing_icon():
    with open("icons.txt", 'r') as file:
        lines = file.readlines()
        line = random.choice(lines).strip()
        if line.startswith('*'):
            line = line[1:].strip()
        basename = os.path.basename(line)
        icon = os.path.splitext(basename)[0]
        if 'icon' not in icon:
            icon = f"icon-{icon}"
        return icon

def generate_icons(amount):
    for icon in range(amount):
        threading.Thread(target=generate_icon, args=(get_missing_icon(),)).start()

def main():
    try:
        count = int(sys.argv[1] if len(sys.argv) > 1 else None)
        generate_icon_ids()
        generate_icons(count)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except FileNotFoundError:
        print("Error: 'llm' command not found")

if __name__ == '__main__':
    main()
