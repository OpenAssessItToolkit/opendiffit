import csv
import optparse

def identify_diffs(old, new, diff):
    """identify rows with changed cells"""
    w_csv_diff = new + '_diff.csv'
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
                print('url in here')
                if row['hash'] != row_index[row['url']['hash']]
                    print('hash in here')


        # writer.writerow(next(reader, []) + ['DIFFs'])

        # for row in reader:
        #     index = old_indices.get(row[3])
        #     if index is not None:
        #         message = 'FOUND in old list (row {})'.format(index)
        #     else:
        #         message = 'NOT FOUND in old list'
        #     writer.writerow(row + [message])

        # for row_old in reader_old:

        #     for row_new in reader_new:
        #         if row_old['url'] in row_new['url']:
        #             print(str(row_old['url']) + ' equal ' + str(row_new['url']))
        #         else:
        #             print(str(row_old['url']) + ' not equal ' + str(row_new['url']))



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