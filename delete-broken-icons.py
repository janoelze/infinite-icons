import subprocess
import datetime
import os, glob

def delete_broken_icons():
    icons = glob.glob('icons/*.svg')
    for icon in icons:
        if '*' in icon:
            os.remove(icon)

def main():
    delete_broken_icons()

if __name__ == '__main__':
    main()
