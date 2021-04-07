from datetime import datetime
from pathlib import Path
import fileinput
import locale
locale.setlocale(locale.LC_TIME, "pt_PT.UTF-8")
import sys


def update_readme(date_now):
    path = Path(__file__).resolve().parents[2]
    filepath = path / 'README.md'
    search_string = "📅️ **Última actualização**:"
    new_string = "📅️ **Última actualização**: {} de {} de {}, {}\n".format(date_now.day, date_now.strftime('%B').capitalize(), date_now.year, date_now.strftime('%H:%M'))

    for line in fileinput.input([filepath], inplace=True):
        if line.strip().startswith(search_string):
            line = new_string
        sys.stdout.write(line)

if __name__ == '__main__':
    
    update_readme(datetime.now())
