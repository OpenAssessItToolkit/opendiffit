import csv
import optparse

def identify_diffs(old, new, diff):
    """identify new files"""
    with open(old, 'r') as old:
        old_indices = dict((r[1], i) for i, r in enumerate(csv.reader(old)))

    with open(new, 'r') as new:
        with open(diff, 'w') as diffs:
            reader = csv.reader(new)
            writer = csv.writer(diffs)

            writer.writerow(next(reader, []) + ['DIFFs'])

            for row in reader:
                index = old_indices.get(row[3])
                if index is not None:
                    message = 'FOUND in old list (row {})'.format(index)
                else:
                    message = 'NOT FOUND in old list'
                writer.writerow(row + [message])


def main():
    """pass in arguments"""
    opt = optparse.OptionParser()
    opt.add_option('--old', '-o', default='old.csv')
    opt.add_option('--new', '-n', default='new.csv')
    opt.add_option('--diff', '-r', default='diff.csv')

    options, args = opt.parse_args()
    identify_diffs(options.old, options.new, options.diff)

if __name__ == '__main__':
    main()