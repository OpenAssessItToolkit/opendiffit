import csv
import os
import argparse
import logging
from utils import initialize_logger
import xlsxwriter
import xlrd
import sys
import configargparse


def get_args():
    example_text = '''
    examples:

    python opendiffit/%(convert_spreadsheet)s --spreadsheet="some file"

    python opendiffit/%(convert_spreadsheet)s --config="my-config-file.yml"


    ''' % {'convert_spreadsheet': os.path.basename(__file__)}

    # parser = argparse.ArgumentParser(epilog=example_text, formatter_class=argparse.RawTextHelpFormatter)
    parser = configargparse.get_argument_parser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add('--config', is_config_file=True, help='config file path')
    parser.add_argument('--spreadsheet', help='spreadsheet file')
    return parser.parse_args()

def convert_spreadsheet(spreadsheet):
    if spreadsheet.lower().endswith('.xlsx'):
        xlsx_to_csv(spreadsheet)
    elif spreadsheet.lower().endswith('.csv'):
        csv_to_xlsx(spreadsheet)
    else:
        logging.error(spreadsheet.lower() + 'That is not a spreadsheet extention.')

def csv_to_xlsx(csv_file):
    """ Convert csv to xlsx with formating """
    # if we read f.csv we will write f.xlsx
    wb = xlsxwriter.Workbook(csv_file[:-4] + '.xlsx')
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

    # TODO: Do something with goofy character issues other than ignore errors
    with open(csv_file,'r', encoding='utf-8', errors='ignore') as csvfile:
        """ Convert csv to xlsx with formating """
        table = csv.reader(csvfile)
        i = 0
        # write each row from the csv file as text into the excel file
        # this may be adjusted to use 'excel types' explicitly (see xlsxwriter doc)
        for row in table:
            ws.write_row(i, 0, row)
            i += 1
        ws.conditional_format('A1:XFD1048576', {'type':'formula',
                      'criteria':'=INDIRECT("d"&ROW())="UNKNOWN"',
                      'format':formatyellow})
        ws.conditional_format('A1:XFD1048576', {'type':'formula',
                      'criteria':'=INDIRECT("d"&ROW())="MAYBE"',
                      'format':formatyellow})
        ws.conditional_format('A1:XFD1048576', {'type':'formula',
                      'criteria':'=INDIRECT("d"&ROW())="ALMOST"',
                      'format':formatyellow})
        ws.conditional_format('A1:XFD1048576', {'type':'formula',
                      'criteria':'=INDIRECT("d"&ROW())="NO"',
                      'format':formatpink})
        ws.conditional_format('A1:XFD1048576', {'type':'formula',
                      'criteria':'=INDIRECT("d"&ROW())="YES"',
                      'format':formatgreen})
        ws.conditional_format('A1:XFD1048576', {'type':'formula',
                      'criteria':'=INDIRECT("d"&ROW())="SKIP"',
                      'format':formatgreen})

        ws.set_column(0, 0, 75)
        ws.set_column(1, 1, 25)
        ws.freeze_panes(1, 0)
    logging.info('Converted csv to pretty xlsx')
    wb.close()

def xlsx_to_csv(xlsx_file):
    """ Convert xlsx to plain csv """
    csv_file = xlsx_file[:-5] + '.csv'
    with xlrd.open_workbook(xlsx_file) as wb:
        sh = wb.sheet_by_index(0)
        with open(csv_file, 'w') as r_csv_new:
            writer = csv.writer(r_csv_new)
            for r in range(sh.nrows):
                writer.writerow(sh.row_values(r))
    logging.info('Converted pretty xlsx to plain csv')


def main():
    """ Pass in arguments """
    args = get_args()
    spreadsheet = args.spreadsheet
    # output_dir = os.path.dirname(args.spreadsheet)
    initialize_logger('convert_spreadsheet')

    try:
        convert_spreadsheet(spreadsheet)

    except Exception as ex:
        logging.error(ex)


if __name__ == '__main__':
    main()