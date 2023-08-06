'''Convert files to PNG files.

:usage:

    gsbatch_topng [options] <file>...

:arguments:

    Files to convert.

:options:

    --colors=arg
        Select color scheme from: none, dark. [default: dark]

    -s, --summary
        Print summary (and no details unless specified).

    -d, --details
        Print details (and no summary unless specified).

    -f, --force
        Force overwrite of all existing (but not matching) files.

    --verbose
        Verbose all commands.

    -q, --quiet
        Do not print progress.

    -h, --help
        Show help.

    --version
        Show version.

(c - MIT) T.W.J. de Geus | tom@geus.me | www.geus.me | github.com/tdegeus/gsbatch_topng
'''

import argparse
import os
import subprocess
import tqdm

from .. import version
from .. import path
from .. import external

def main():

    try:

        class Parser(argparse.ArgumentParser):
            def print_help(self):
                print(__doc__)

        parser = Parser()
        parser.add_argument(      '--colors', required=False, default='dark')
        parser.add_argument('-s', '--summary', required=False, action='store_true')
        parser.add_argument('-d', '--details', required=False, action='store_true')
        parser.add_argument('-f', '--force', required=False, action='store_true')
        parser.add_argument(      '--verbose', required=False, action='store_true')
        parser.add_argument('-q', '--quiet', required=False, action='store_true')
        parser.add_argument('-v', '--version', action='version', version=version)
        parser.add_argument('files', nargs='+')
        args = parser.parse_args()

        output = [os.path.splitext(file)[0] + ".png" for file in args.files]
        path.check_create(
            source = args.files,
            dest = output,
            quiet = args.quiet,
            force = args.force,
            print_details = not (args.force or args.summary) or args.details,
            print_summary = not (args.force or args.details) or args.summary,
            print_all = args.details,
            theme_name = args.colors.lower())

        for i, o in zip(tqdm.tqdm(args.files, disable=args.quiet), output):
            command = [
                'gs',
                '-dBATCH',
                '-dNOPAUSE',
                '-dQUIET',
                '-sDEVICE=png16m',
                '-r300',
                '-dUseCropBox',
                '-sOutputFile="{0:s}"'.format(o),
                '"{0:s}"'.format(i)]
            external.exec_cmd(' '.join(command), verbose=args.verbose)

    except Exception as e:

        print(e)
        return 1


if __name__ == '__main__':

    main()
