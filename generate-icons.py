import os
import subprocess

def clean_yaml(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    with open(file_path, 'w') as file:
        for line in lines:
            if not line.startswith('```'):
                file.write(line)

def unlink_icons():
    if os.path.exists('icons'):
        shutil.rmtree('icons')
    os.mkdir('icons')

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
    clean_yaml(f"icons/{icon}.svg")

def generate_icons():
    i = 0

    with open("icons.txt", 'r') as file:
        lines = file.readlines()

    for line in lines:
        if line.startswith('*'):
            raw_icon = line[1:].strip()
            basename = os.path.basename(raw_icon)
            icon = os.path.splitext(basename)[0]
            path = f"icons/{icon}.svg"
            if not os.path.isfile(path) and i < 4:
                generate_icon(icon)
                i += 1

def main():
    try:
        generate_icon_ids()
        generate_icons()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except FileNotFoundError:
        print("Error: 'llm' command not found")

if __name__ == '__main__':
    main()
