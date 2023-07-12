import os

def create_readme():
    # Create a readme.md file containing a markdown table of all icons, four per row
    with open('README.md', 'w') as file:
        file.write("# Icons\n\n")
        file.write("|  |  |  |  |\n")
        file.write("| ---- | ---- | ---- | ---- |\n")

        row = ""
        titles = ""
        icons = sorted(os.listdir('icons'))
        for i, icon in enumerate(icons, start=1):
            if icon.endswith('.svg'):
                iconname = os.path.splitext(icon)[0]
                row += f"| ![{iconname}](icons/{icon}) "
                titles += f"| {iconname} "
                if i % 4 == 0:
                    file.write(row + '\n')
                    file.write(titles + '\n')
                    titles = ""
                    row = ""

        file.write("\n")

def create_overview():
    with open('icons.html', 'w') as file:
        icons = sorted(os.listdir('icons'))
        for icon in icons:
            if icon.endswith('.svg'):
                iconname = os.path.splitext(icon)[0]
                icon_path = os.path.join('icons', icon)
                with open(icon_path, 'r') as svg_file:
                    svg_data = svg_file.read()
                    file.write(f"<div class='icon'><div class='icon-name'>{iconname}</div><div class='icon-svg'>{svg_data}</div></div>\n")

def main():
    create_readme()
    create_overview()

if __name__ == '__main__':
    main()
