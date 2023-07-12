import subprocess
import datetime
import os, glob

def calculate_avg_tokens_per_icon():
    icons = glob.glob('icons/*.svg')
    cost = 0.06
    total_tokens = 0
    for icon in icons:
        contents = open(icon, 'r').read()
        output = int(subprocess.check_output(['ttok', contents], text=True).strip())
        total_tokens += output
    avg_tokens = total_tokens / len(icons)
    print(f"Average tokens per icon: {avg_tokens}")


def main():
    calculate_avg_tokens_per_icon()

if __name__ == '__main__':
    main()
