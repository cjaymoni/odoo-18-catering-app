
import csv
import re

def md_table_to_csv(md_file, csv_file):
    with open(md_file, 'r') as f:
        lines = f.readlines()

    table_lines = [line.strip() for line in lines if line.strip().startswith('|')]
    if not table_lines:
        print("No markdown table found.")
        return

    # Remove separator line (---)
    table_lines = [line for line in table_lines if not re.match(r'^\|[-| ]+\|$', line)]

    rows = [line.strip('|').split('|') for line in table_lines]
    rows = [[cell.strip() for cell in row] for row in rows]

    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

md_table_to_csv('../../../Downloads/migration_analysis(1).md', 'godady-migration1.csv')