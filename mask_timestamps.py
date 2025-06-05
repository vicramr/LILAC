import sys

if __name__ == '__main__':
    infile = sys.argv[1]
    outfile = sys.argv[2]

    with open(infile) as f_in, open(outfile, mode='w') as f_out:
        for line in f_in:
            line = line.rstrip()

            if line.startswith('202'):
                word, rest = line.split(maxsplit=1)
                assert word.startswith('2024') or word.startswith('2025')
                line = '[TIMESTAMP] ' + rest
            f_out.write(line)
            f_out.write('\n')
