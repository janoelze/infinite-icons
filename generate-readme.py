import datetime
import os

def create_readme():
    icons_per_run = 5
    avg_run_duration = 1
    cost_per_run = 0.008
    runs_per_hour = 6
    avg_cost_per_icon = 0.36585
    icons_per_hour = icons_per_run * runs_per_hour
    icons_per_day = icons_per_hour * 24
    icons_per_week = icons_per_day * 7
    icons_per_month = icons_per_week * 4
    icons_per_year = icons_per_month * 12
    days_to_one_million_icons = round(1000000 / icons_per_day)
    days_to_one_billion_icons = round(1000000000 / icons_per_day)
    years_to_one_billion_icons = round(days_to_one_billion_icons / 365)
    date_one_million_icons = datetime.datetime.now() + datetime.timedelta(days=days_to_one_million_icons)
    date_one_billion_icons = datetime.datetime.now() + datetime.timedelta(days=days_to_one_billion_icons)
    cost_per_one_billion_icons = round(avg_cost_per_icon * 1000000000)
    cost_per_one_billion_icons = f"${cost_per_one_billion_icons:,}"
    run_cost_per_hour = round(cost_per_run * runs_per_hour, 2)
    run_cost_per_day = round(run_cost_per_hour * 24)
    run_cost_to_one_million = days_to_one_million_icons * run_cost_per_day
    run_cost_to_one_billion_icons = days_to_one_billion_icons * run_cost_per_day
    run_cost_to_one_billion_icons_formatted = f"${run_cost_to_one_billion_icons:,}"
    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    # Create a readme.md file containing a markdown table of all icons, four per row
    with open('README.md', 'w') as file:
        file.write("# infinite icons\n\n")
        file.write("here we're generating the biggest svg icon set on this planet using openai's gpt-4 llm. current velocity is %s i/ph (icons per hour). we'll reach 1M icons in %s days (%s) and 1B in %s years (%s). Reaching 1B icons will rack up an OpenAI bill of about %s not including the %s required for the GitHub Actions credits. *we're desperately seeking funding.*\n\n" % (
            icons_per_hour,
            days_to_one_million_icons,
            datetime.datetime.strftime(date_one_million_icons, '%Y-%m-%d'),
            years_to_one_billion_icons,
            datetime.datetime.strftime(date_one_billion_icons, '%Y-%m-%d'),
            cost_per_one_billion_icons,
            run_cost_to_one_billion_icons_formatted
            ))
        file.write("last update: %s\n\n" % current_date)
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
