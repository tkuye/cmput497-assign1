import argparse
import pathlib
import re
import os
import csv
from tqdm import tqdm
argparser = argparse.ArgumentParser(description='CMPT 497 Assignment 1')

argparser.add_argument('data', type=pathlib.Path, help='Path to data directory')
argparser.add_argument('output', type=pathlib.Path, help='Path to output file')



months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
months_abbrev = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
days_abbrev = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def list_to_string(list_p):
    return to_raw("(" + '|'.join(list_p) + ")")

def parse_list_to_regex(list_p):
    words_str = '|'.join(list_p)
    return re.compile(r'\b(' + words_str + r')\b')

def preprocess_text(text):
    text = text.replace('\n', ' ')
    text = text.replace('\t', ' ')
    text = text.replace('\r', ' ')
    return text

def to_raw(string):
    return fr"{string}"


def parse_matches(matches):
    
    match_str_set = list(set([match[2].group(0) for match in matches]))
    for match in matches:
        small = False
        for match_str in match_str_set:
            if match[2].group(0) != match_str and match[2].group(0) in match_str:
                small = True
                break
        if not small:
            yield (match[0], match[1], match[2].group(0), match[3])


def main():
    args = argparser.parse_args()
    data = args.data
    output = args.output
    files = os.listdir(data)
    matches = []
    for file in tqdm(files):
        file_matches = []
        with open(data.resolve() / file, 'r') as f:
            file_data = f.read()
           
            month_pattern = parse_list_to_regex(months + months_abbrev)
            day_pattern = parse_list_to_regex(days + days_abbrev)
            year_pattern = re.compile(r'\b\d{4}\b')
            months_str = list_to_string(months + months_abbrev)
            day_month_pattern = re.compile(r'\b\d{2}\s(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b')
            month_year_pattern = re.compile(r'\b(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s(?:\d{4}|\d{2})\b')
            day_month_year_pattern = re.compile(r'\b\d{2}\s' + months_str + r'\s(?:\d{4}|\d{2})\b')
            decade_pattern = re.compile(r'\bthe\s(?:\d{4}|\d{2})s\b')
            part_of_decade_pattern = re.compile(r'\bthe(?:\s+\w+\s+)(?:\d{4}|\d{2})s\b')
            relative_pattern = re.compile(r'\b\w+\s(month|year|weekend)s?\b')
            part_relative_pattern = re.compile(r'\b\w+\s\w+\s(month|year|weekend)s?\b')
            expr_types = {
            'month': month_pattern,
            'dayofweek': day_pattern,
            'year': year_pattern,
            'day-month': day_month_pattern,
            'month-year': month_year_pattern,
            'day-month-year': day_month_year_pattern,
            'decade': decade_pattern,
            'part-of-decade': part_of_decade_pattern,
            'relative-year/month/week': relative_pattern,
            'part-relative-year/month/week': part_relative_pattern
        }
            for expr_type, expr in expr_types.items():
                file_matches += [(file, expr_type,  match, match.start()) for match in expr.finditer(file_data)]
            matches += parse_matches(file_matches)

    with open(output, 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['article_id', 'expr_type', 'value', 'offset'])
        writer.writerows(matches)

    print("All done!")
            
        

        


if __name__ == '__main__':
    main()