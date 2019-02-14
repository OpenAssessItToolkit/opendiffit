import csv
import optparse
from remote_sha import get_remote_sha_sum


def add_hash(input_file):
    """Add new column with hash"""
    output_file = input_file + '_hashed.csv'
    with open(input_file, 'r', encoding='utf-8-sig') as r_csvfile, open(output_file, 'w', encoding='utf-8-sig') as w_csvfile:
        reader = csv.DictReader(r_csvfile)
        fieldnames = reader.fieldnames + ['hash']
        writer = csv.DictWriter(w_csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            row['hash'] = get_remote_sha_sum(row['url'])
            writer.writerow(row)
            print('Hashed')


def check_header(input_file):
    """Check if required column headers exist"""
    with open(input_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        if 'url' in reader.fieldnames:
            return True
        else:
            print("This csv is invalid or has no 'url'.")
            return False


def main():
    """Pass arguments, check csv validity, and add hash"""
    opt = optparse.OptionParser()
    opt.add_option('--input-file', '-i', default='foo_r.csv')
    opt.add_option('--output_-ile', '-o', default='foo_w.csv')
    options, args = opt.parse_args()

    if check_header(options.input_file):
        add_hash(options.input_file)
    else:
        print("Check contents of csv.")

    print('Done adding hashes.')

if __name__ == '__main__':
    main()