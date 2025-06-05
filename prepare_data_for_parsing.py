"""
Overwrite *_structured.csv and also write *_templates.csv for the LILAC parsing run.
"""
import sys
import csv

if __name__ == '__main__':
    logfile = sys.argv[1]
    print('Loading logs from', logfile)

    fieldnames = ['LineId', 'Content', 'EventId', 'EventTemplate']
    csvfile = logfile + '_structured.csv'

    num_logs = 0

    with open(csvfile, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        with open(logfile) as f_read:
            for i, log in enumerate(f_read):
                log = log.rstrip()
                if log == '':
                    print('Empty log found')
                    log = 'empty'
                line_id = i + 1
                writer.writerow({
                    'LineId': line_id,
                    'Content': log,
                    'EventId': 'E1',
                    'EventTemplate': '<*>',
                })

                num_logs += 1

    templates_file = logfile + '_templates.csv'
    with open(templates_file, 'w') as f:
        f.write('EventId,EventTemplate,Occurrences\n')
        f.write('E1,<*>,')
        f.write(str(num_logs))
        f.write('\n')
