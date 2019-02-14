import csv
import os
import argparse

def get_args():
    example_text = '''
    examples:

    python opendiffit/%(identify_diffs)s --old="old-report.csv" --new="new-report.csv" --diff="diff-report.csv"

    ''' % {'identify_diffs': os.path.basename(__file__)}

    parser = argparse.ArgumentParser(epilog=example_text, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-o', '--old', help='original csv')
    parser.add_argument('-n', '--new', help='new csv')
    parser.add_argument('-d', '--diff', help='output csv')
    return parser.parse_args()

def identify_diffs(old, new, diff):
    """identify rows with changed cells"""
    with open(old, 'r', encoding='utf-8-sig') as r_csv_old, \
        open(new, 'r', encoding='utf-8-sig') as r_csv_new, \
        open(diff, 'w', encoding='utf-8-sig') as w_csv_diff:

        reader_old = csv.DictReader(r_csv_old)
        reader_new = csv.DictReader(r_csv_new)
        fieldnames = reader_new.fieldnames + ['diff']
        writer = csv.DictWriter(w_csv_diff, fieldnames=fieldnames)
        writer.writeheader()

        row_index = {r['url']: r for r in reader_old}

        for row in reader_new:
            if row['url'] in row_index:
                if row['hash'] == row_index[row['url']]['hash']:
                    message = 'SAME'
                else:
                    message = 'UPDATED'
            else:
                message = 'NEW'
            row['diff'] = message
            writer.writerow(row)


def check_headers(old,new,diff):
    """Check if required column headers exist"""
    with open(old, 'r', encoding='utf-8-sig') as old_csv, \
        open(new, 'r', encoding='utf-8-sig') as new_csv:
        reader_old = csv.DictReader(old_csv, dialect='excel')
        reader_new = csv.DictReader(new_csv, dialect='excel')

        if ('url' in reader_old.fieldnames) and ('url' in reader_new.fieldnames):
            # print("CSVs are both valid and have 'url' headers.")
            return True
        else:
            # print("One or more CSVs are invalid or have no 'url' headers. utf-8-sig")
            return False

def main():
    """pass in arguments"""
    args = get_args()
    new = args.new
    old = args.old
    diff = args.diff

    if check_headers(old, new, diff):
        identify_diffs(old, new, diff)
    else:
        print("Check contents of csv.")

if __name__ == '__main__':
    main()