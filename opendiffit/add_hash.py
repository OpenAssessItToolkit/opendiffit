import csv
import optparse
from remote_sha import *


def add_hash(in_file):
    """Add new column with hash"""
    out_file = in_file + '_hashed.csv'
    with open(in_file, 'r') as r_csvfile, open(out_file, 'w') as w_csvfile:
        reader = csv.DictReader(r_csvfile)
        fieldnames = reader.fieldnames + ['hash']
        writer = csv.DictWriter(w_csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            row['hash'] = get_remote_sha_sum(row['url'])
            writer.writerow(row)


def check_header(in_file):
    """Check if required column headers exist"""
    with open(in_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        if 'url' in reader.fieldnames:
            return True
        else:
            print("This csv is invalid or has no 'href'.")
            return False


def main():
    """Pass arguments, check csv validity, and add hash"""
    opt = optparse.OptionParser()
    opt.add_option('--in_file', '-i', default='foo_r.csv')
    opt.add_option('--out_file', '-o', default='foo_w.csv')
    options, args = opt.parse_args()

    if check_header(options.in_file):
        add_hash(options.in_file)
    else:
        print("Check contents of csv.")

if __name__ == '__main__':
    main()