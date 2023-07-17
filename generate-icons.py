import os, sys, random
import subprocess, threading
import openai

def run_prompt(system, prompt):
    c = openai.ChatCompletion.create(model="gpt-4", messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": prompt}
    ])
    return c.choices[0].message.content

def clean_svg_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    with open(file_path, 'w') as file:
        for line in lines:
            if not line.startswith('```'):
                file.write(line)

def generate_icon_ids():
    output = run_prompt("", "Output 15 icons potentially included in a large web icon set. The names should contain descriptive IDs. Make them non-obvious. Output each line starting with a '*' star. The filname should only contain the desceriptive icon ID. For example: icon-home.svg, icon-pencil.svg and so forth. NEVER respond with prose. NEVER respond with markdown. NEVER respond with comments, NEVER respond with notes.")
    # output = subprocess.check_output(['llm', 'Output 15 icons potentially included in a large web icon set. The names should contain descriptive IDs. Make them non-obvious. Output each line starting with a "*" star. The filname should only contain the desceriptive icon ID. For example: icon-home.svg, icon-pencil.svg and so forth. NEVER respond with prose. NEVER respond with markdown. NEVER respond with comments, NEVER respond with notes.'], text=True)
    with open('icons.txt', 'a+') as file:
        file.write(output)

def generate_icon(icon_filename):
    icon_id = os.path.splitext(icon_filename)[0]
    print(f"Generating icon '{icon_id}'")
    prompt = f"The icon you are creating is called '{icon_id}'. The SVG element should have the class 'icon {icon_id}'."
    output = run_prompt(
        f"You are an icon creation engine. Only output valid SVG code. NEVER respond with prose. NEVER respond with markdown. NEVER respond with comments, NEVER respond with notes. Only output valid SVG.",
        prompt
    )
    with open(f"icons/{icon_id}.svg", 'w') as file:
        file.write(output)
    clean_svg_file(f"icons/{icon_id}.svg")

def clean_line(line):
    line = line.strip()
    if line.startswith('*'):
        line = line[1:].strip()
    if 'icon' not in line:
        line = f"icon-{line}"
    return line

def get_missing_icon():
    icon_filenames = []
    with open("icons.txt", 'r') as file:
        lines = file.readlines()
        for line in lines:
            icon_filename = clean_line(line)
            icon_filenames.append(icon_filename)
    icon_filenames = random.sample(icon_filenames, len(icon_filenames))
    for icon_filename in icon_filenames:
        if not os.path.exists(f"icons/{icon_filename}") and not "*" in icon_filename:
            return icon_filename

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
