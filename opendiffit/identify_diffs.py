import csv
import os
import argparse
import logging
import tempfile
from utils import yes_or_no
from utils import initialize_logger
from utils import check_header
import xlsxwriter
import xlrd
import sys


def get_args():
    example_text = '''
    examples:

    python opendiffit/%(identify_diffs)s --old="old-report.csv" --new="new-report.csv" --diff="diff-report.csv"

    python opendiffit/%(identify_diffs)s --old="old-report.csv" --new="new-report.csv" --diff="-"

    ''' % {'identify_diffs': os.path.basename(__file__)}

    parser = argparse.ArgumentParser(epilog=example_text, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-o', '--old', help='original csv')
    parser.add_argument('-n', '--new', help='new csv')
    parser.add_argument('-d', '--diff', help='output csv. use "-" add columns to the existing new csv file (keep a backup).')
    return parser.parse_args()

def identify_diffs(old, new, diff):
    """ Identify rows with changed cells """
    with open(old, 'r', encoding='utf-8-sig') as r_csv_old, \
        open(new, 'r', encoding='utf-8-sig') as r_csv_new, \
        open(diff, 'w', encoding='utf-8-sig') as w_csv_diff:
        reader_old = csv.DictReader(r_csv_old)
        reader_new = csv.DictReader(r_csv_new)
        fieldnames = reader_new.fieldnames
        if 'diff' not in reader_new.fieldnames:
            fieldnames = reader_new.fieldnames + ['diff']
        if 'comply' not in reader_new.fieldnames:
            fieldnames = reader_new.fieldnames + ['comply']

        writer = csv.DictWriter(w_csv_diff, fieldnames=fieldnames)
        writer.writeheader()

        row_index = {r['url']: r for r in reader_old}

        for row in reader_new:
            if row['url'] in row_index:
                row['comply'] = 'UNKNOWN'
                if row['hash'] == row_index[row['url']]['hash']:
                    row['diff'] = 'SAME'
                    row['comply'] = row_index[row['url']]['comply'] # carry over compliance value from prev report

                else:
                    row['diff'] = 'UPDATED'
                    row['comply'] = 'UNKNOWN'
            else:
                row['diff'] = 'NEW'
                row['comply'] = 'UNKNOWN'
            if row['comply'] == '':
                row['comply'] = '.'
            writer.writerow(row)
    # logging.info("Created %s file." % (diff))

def csv_to_xlsx(csv_file):
    """ Convert csv to xlsx with formating """
    # if we read f.csv we will write f.xlsx
    wb = xlsxwriter.Workbook(csv_file[:-3] + '.xlsx')
    ws = wb.add_worksheet("WS1")    # your worksheet title here
    # ws.insert_textbox('B2', 'Edit using Online Excel in Box!', {'width': 256, 'height': 100})
    ws.insert_textbox('G1', 'Only edit using Online Excel in Box!',
                         {'width': 250,
                          'height': 30,
                          'y_offset': 25,
                          'x_offset': 25,
                          'font': {'bold': True,
                                   'color': 'red'
                                    },
                          'align': {'vertical': 'middle',
                                    'horizontal': 'center'
                                    },
                          'line': {'color': 'red',
                                   'width': 1.25,
                                   'dash_type': 'square_dot'}
                                   })

    formatyellow = wb.add_format({'bg_color':'#FFD960'})
    formatpink = wb.add_format({'bg_color':'#ffc0cb'})
    formatgreen = wb.add_format({'bg_color':'#ccff80'})

    with open(csv_file,'r') as csvfile:
        """ Convert csv to xlsx with formating """
        table = csv.reader(csvfile)
        i = 0
        # write each row from the csv file as text into the excel file
        # this may be adjusted to use 'excel types' explicitly (see xlsxwriter doc)
        for row in table:
            ws.write_row(i, 0, row)
            i += 1
        ws.conditional_format('A1:XFD1048576', {'type':'formula',
                      'criteria':'=INDIRECT("e"&ROW())="UNKNOWN"',
                      'format':formatyellow})
        ws.conditional_format('A1:XFD1048576', {'type':'formula',
                      'criteria':'=INDIRECT("e"&ROW())="NO"',
                      'format':formatpink})
        ws.conditional_format('A1:XFD1048576', {'type':'formula',
                      'criteria':'=INDIRECT("e"&ROW())="YES"',
                      'format':formatgreen})
        ws.set_column(0, 0, 75)
        ws.set_column(1, 1, 25)
        ws.freeze_panes(1, 0)
    logging.info('Converted csv to pretty xlsx')
    wb.close()

def xlsx_to_csv(xlsx_file):
    """ Convert xlsx to csv """
    csv_file = xlsx_file[:-4] + '.csv'
    with xlrd.open_workbook(xlsx_file) as wb:
        sh = wb.sheet_by_index(0)
        with open(csv_file, 'w', encoding='utf-8-sig') as r_csv_new:
            writer = csv.writer(r_csv_new)
            for r in range(sh.nrows):
                writer.writerow(sh.row_values(r))
    logging.info('Converted pretty xlsx to plain csv')


def main():
    """ Pass in arguments """
    args = get_args()
    new = args.new
    old = args.old
    diff = args.diff
    output_dir = os.path.dirname(args.new)
    initialize_logger('identify_diffs', output_dir)

    if new.lower().endswith('.xlsx'):
        xlsx_to_csv(new)
        new = new[:-4] + '.csv'
        logging.info('You asked to use an xlsx. We converted it to a csv and are using that newly converted file instead.')

    if check_header(old,['url','hash','comply'],[]) and check_header(new,['url','hash','comply'],['diff']):
        try:
            identify_diffs(old, new, diff)
            if diff == "-":
                # yes_or_no("Are you sure you want to add the data to the existing '%s' file? (keeping a backup is recommended)" % (input_file))
                os.remove(new)
                os.rename(diff, new)
                logging.info("Updated '%s' file with diff" % (new))
                csv_to_xlsx(new)
            else:
                logging.info("Created new '%s' file with diff" % (new))
                csv_to_xlsx(diff)
            logging.info("Made an Excel copy of '%s' file with diff" % (diff))

        except Exception as ex:
            logging.error(ex)


if __name__ == '__main__':
    main()