import csv
import optparse

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
    opt = optparse.OptionParser()
    opt.add_option('--old', '-o', default='old.csv')
    opt.add_option('--new', '-n', default='new.csv')
    opt.add_option('--diff', '-r', default='diff.csv')

    options, args = opt.parse_args()

    if check_headers(options.old, options.new, options.diff):
        identify_diffs(options.old, options.new, options.diff)
    else:
        print("Check contents of csv.")

if __name__ == '__main__':
    main()