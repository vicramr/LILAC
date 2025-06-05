"""
Given the text file with raw logs (one log per line), produce
the structured CSV. NOTE: because the ground truth logs are not
assumed to be available, the EventTemplate field is just a
copy of the Content field.
"""
import sys
import csv

if __name__ == '__main__':
    logfile = sys.argv[1]
    print('Loading logs from', logfile)

    fieldnames = ['LineId', 'Content', 'EventTemplate']  # Omitting EventId
    csvfile = logfile + '_structured.csv'
    with open(csvfile, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        with open(logfile) as f_read:
            for i, log in enumerate(f_read):
                log = log.rstrip()
                line_id = i + 1
                writer.writerow({
                    'LineId': line_id,
                    'Content': log,
                    'EventTemplate': log,
                })
