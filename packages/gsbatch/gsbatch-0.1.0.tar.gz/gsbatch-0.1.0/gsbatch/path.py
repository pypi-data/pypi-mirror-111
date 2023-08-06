import click
import os

from .rich import String
from .rich import theme

def check_create(
    source,
    dest,
    quiet = False,
    force = False,
    print_details = True,
    print_summary = True,
    print_all = False,
    theme_name = 'none'):
    r'''
Check to create files.

:type source: list of str
:param source: Filenames of source files.

:type dest: list of str
:param dest: Filenames of the destination files.

:param bool quiet: Proceed without printing progress.
:param bool force: Continue without prompt.
:param bool print_details: Print copy details.
:param bool print_summary: Print copy summary.
:param bool print_all: If ``False`` auto-truncation of long output is applied.

:type theme_name: str or None
:param theme_name: The name of the color-theme. See :py:mod:`shelephant.rich.theme`.
    '''

    assert type(source) == list
    assert type(dest) == list
    assert len(source) == len(dest)

    if len(source) == 0:
        if not quiet:
            print('Nothing to do')
        return

    n = len(source)
    overwrite = [os.path.isfile(file) for file in dest]
    create = [not o for o in overwrite]
    color = theme(theme_name.lower())

    l = max([len(file) for file in source])
    ncreate = sum(create)
    noverwrite = sum(overwrite)
    pcreate = not ((noverwrite > 0 and ncreate > 100) or ncreate > 300) or print_all
    pcreate_message = ' (not printed)' if not pcreate else ''

    overview = []
    if ncreate > 0:
        overview += [String('create (->): {0:d}{1:s}'.format(ncreate, pcreate_message), color=color['new']).format()]
    if noverwrite > 0:
        overview += [String('overwrite (=>): {0:d}'.format(noverwrite), color=color['overwrite']).format()]

    if ncreate + noverwrite <= 100 and print_summary:
        print('-----')
        print(', '.join(overview))
        print('-----')

    if print_details:
        for i in range(n):
            if create[i] and pcreate:
                print('{0:s} {1:s} {2:s}'.format(
                    String(source[i], width=l, color=color['bright']).format(),
                    String('->', color=color['bright']).format(),
                    String(dest[i], color=color['new']).format()
                ))
            elif overwrite[i]:
                print('{0:s} {1:s} {2:s}'.format(
                    String(source[i], width=l, color=color['bright']).format(),
                    String('=>', color=color['bright']).format(),
                    String(dest[i], color=color['overwrite']).format()
                ))

    if ncreate + noverwrite > 100 and print_summary:
        print('-----')
        print(', '.join(overview))
        print('-----')

    if not force:
        if not click.confirm('Proceed?'):
            raise IOError('Cancelled')

