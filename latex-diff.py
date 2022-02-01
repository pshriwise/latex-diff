#!/usr/bin/env python

import argparse
import glob
import os
import shutil
import subprocess


def main():
    # CLI
    descr = "Run latexdiff and generate a pdf"
    parser = argparse.ArgumentParser(description=descr,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    r1 = 'Starting commit/revision/tag.'
    parser.add_argument('r1', help=r1)
    r2 = 'Ending commit/revision/tag. Defaults to HEAD.'
    parser.add_argument('--r2', help=r2, default='HEAD')
    args = parser.parse_args()

    # args from CLI
    r1 = args.r1
    r2 = args.r2

    # save files
    files = glob.glob('*.tex')
    for f in files:
        shutil.copyfile(f, '.' + f)

    # generate diffs
    cmd = "latexdiff-vc -r {} -r {}"
    subprocess.check_call(cmd.format(r1, r2).split() + files)

    # build pdf
    diff_file = lambda f, r1, r2: "{}-diff{}-{}.{}".format(
        f[:-4], r1, r2, f[-3:])
    for f in files:
        shutil.copyfile(diff_file(f, r1, r2), f)
    subprocess.check_call('make')
    shutil.copyfile('paper.pdf', diff_file('paper.pdf', r1, r2))

    # clean up
    for f in files:
        shutil.copyfile('.' + f, f)
    rm = glob.glob(diff_file('*.tex', r1, r2)) + glob.glob('*oldtmp*.tex')
    for f in set(rm):
        os.remove(f)


if __name__ == '__main__':
    main()
