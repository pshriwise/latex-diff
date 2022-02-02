#!/usr/bin/env python

import argparse
import glob
import os
import shutil
import subprocess


def main(args):
    try:
        # args from CLI
        r1 = args.r1
        r2 = args.r2

        # save files
        files = glob.glob('*.tex')
        for f in files:
            shutil.copyfile(f, '.' + f)
        files = list(filter(lambda f: f not in args.ignore, files))

        # generate diffs
        cmd = "latexdiff-vc -t CFONT -r {} -r {}"
        subprocess.check_call(cmd.format(r1, r2).split() + files)

        # build pdf
        diff_file = lambda f, r1, r2: "{}-diff{}-{}.{}".format(
            f[:-4], r1, r2, f[-3:])
        for f in files:
            shutil.copyfile(diff_file(f, r1, r2), f)
        subprocess.check_call('make')
        shutil.copyfile('main.pdf', diff_file('main.pdf', r1, r2))
        if args.output:
            shutil.move('main.pdf', args.output)
    finally:
        # always clean up
        for f in files:
            shutil.copyfile('.' + f, f)
        rm = glob.glob(diff_file('*.tex', r1, r2)) + glob.glob('*oldtmp*.tex')
        for f in set(rm):
            os.remove(f)


if __name__ == '__main__':
    # CLI
    descr = "Run latexdiff and generate a pdf"
    parser = argparse.ArgumentParser(description=descr,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
    r1 = 'Starting commit/revision/tag.'
    parser.add_argument('r1', help=r1)
    r2 = 'Ending commit/revision/tag. Defaults to HEAD.'
    parser.add_argument('-r2', help=r2, default='HEAD')
    ignore = 'List of tex files to ignore'
    parser.add_argument('-i','--ignore', help=ignore, nargs='+', default=[])
    output = 'Name of the resulting PDF diff'
    parser.add_argument('-o','--output', help=output, default='')

    args = parser.parse_args()
    main(args)
