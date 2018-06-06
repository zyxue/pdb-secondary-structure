import gzip
import logging
import csv
import argparse

logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s|%(levelname)s|%(message)s')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', type=str, default='ss.txt.gz',
        help='input file, e.g. ss.txt.gz downloaded from https://cdn.rcsb.org/etl/kabschSander/ss.txt.gz'
    )
    parser.add_argument(
        '-o', '--output', type=str, default=None,
        help='output filename in csv format'
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    infile = args.input
    if args.output is None:
        outfile = args.input.replace('txt.gz', 'csv')
    else:
        outfile = args.output

    with gzip.open(infile, 'rt') as inf:
        # cannot use SeqIO.parse from Biopython because it cannot handle empty
        # string in DSSP secondary structure properly! Just put here for
        # reference

        # e.g. seqio = SeqIO.parse(inf, format='fasta')

        with open(outfile, 'wt') as opf:
            csv_writer = csv.writer(opf)
            csv_writer.writerow(['pdb_id', 'chain_code', 'seq', 'sst'])

            state = None
            count = 0
            seq_id, seq_chain_id = '', ''
            sst_id, sst_chain_id = '', ''
            seq, sst = '', ''
            log_interval = 30000
            for k, line in enumerate(inf):
                if line.startswith('>'):
                    line = line.replace('>', '')
                    if state is None or state == 'ss':
                        if state == 'ss':
                            assert seq_id == sst_id
                            assert seq_chain_id == sst_chain_id
                            csv_writer.writerow(
                                [seq_id, seq_chain_id, seq, sst]
                            )
                            count += 1
                            if count % log_interval == 0:
                                msg = 'processing {0}th record'.format(count)
                                logging.info(msg)

                        state = 'seq'
                        seq_id = line.split(':')[0]
                        seq_chain_id = line.split(':')[1]
                        seq, sst = '', ''
                    elif state == 'seq':
                        state = 'ss'
                        sst_id = line.split(':')[0]
                        sst_chain_id = line.split(':')[1]
                    else:
                        raise ValueError('unknown state: {0}'.format(state))
                    continue

                if state == 'seq':
                    seq += line.strip()
                else:
                    sst += line.replace(' ', 'C').strip()

            # count last seq
            count += 1
    logging.info('processed {0}th records'.format((count)))
