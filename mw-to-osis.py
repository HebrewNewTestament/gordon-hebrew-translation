# mw-to-osis.py
# Hack to convert extremely specific mediawiki source to OSIS.

import re

from hebrew_numbers import gematria_to_int
from hebrew_numbers import int_to_gematria

# E.g.:
# ==[[דניאל ב|פרק ב]]==
chapter_re = re.compile(
    f'^==\[\['
    f'(?P<heb_book_name>[^\s]*) .*'
    f'פרק (?P<heb_chapter_name>[א-ת]*).*=='
)

# E.g.:
# (יג) וְהַדָּת יָצְאָה, וְהַחֲכָמִים נֶהֱרָגִים, וְעָמְדוּ דָּנִיֵּאל וַחֲבֵרָיו לְהֵהָרֵג.
verse_re = re.compile(
    '^\((?P<heb_verse_name>[^\)]*)\) (?P<verse_content>.*)'
)

def heb_to_osis_bookname(heb_book_name):
    known_names = {
        'דניאל': 'Dan',
        'עזרא': 'Ezra',
    }
    if heb_book_name in known_names:
        return known_names[heb_book_name]
    raise RuntimeError(f'Unknown book name {heb_book_name}')

book_indent_level = 1
chapter_indent_level = book_indent_level + 1
verse_indent_level = chapter_indent_level + 1
book_indent = '\t' * book_indent_level
chapter_indent = '\t' * chapter_indent_level
verse_indent = '\t' * verse_indent_level

def osis_chapter_header(heb_book_name, heb_chapter_name):
    osis_bookname = heb_to_osis_bookname(heb_book_name)
    chapter_number = gematria_to_int(heb_chapter_name)
    id = f'{osis_bookname}.{chapter_number}'
    return (
        f'{chapter_indent}'
        f'<chapter osisID="{id}" sID="{id}" n="{heb_chapter_name}"/>'
    )

def osis_chapter_footer(heb_book_name, heb_chapter_name):
    osis_bookname = heb_to_osis_bookname(heb_book_name)
    chapter_number = gematria_to_int(heb_chapter_name)
    id = f'{osis_bookname}.{chapter_number}'
    return (
        f'{chapter_indent}'
        f'<chapter eID="{id}"/>'
    )

def osis_verse(
    heb_book_name,
    heb_chapter_name,
    heb_verse_name,
    verse_content,
):
    osis_bookname = heb_to_osis_bookname(heb_book_name)
    chapter_number = gematria_to_int(heb_chapter_name)
    verse_number = gematria_to_int(heb_verse_name)
    id = f'{osis_bookname}.{chapter_number}.{verse_number}'
    return (
        f'{verse_indent}'
        f'<verse osisID="{id}" sID="{id}" n="{heb_verse_name}"/> '
        f'{verse_content}'
        f'<verse eID="{id}"/>'
    )

def osis_book_header(heb_book_name):
    osis_bookname = heb_to_osis_bookname(heb_book_name)
    return [
        (
            f'{book_indent}'
            f'<div type="book" osisID="{osis_bookname}">'
        ),
        (
            f'{chapter_indent}'
            f'<title>{heb_book_name}</title>'
        )
    ]

def osis_book_footer(heb_book_name):
    return [
        (
            f'{book_indent}'
            f'</div>'
        ),
    ]

def mw_content_to_osis(content):
    res = []
    on_start = True
    for line in content.splitlines():
        if chapter_re.match(line):
            match = chapter_re.match(line)
            heb_book_name = match.group('heb_book_name')
            heb_chapter_name = match.group('heb_chapter_name')
            if on_start:
                on_start = False
                res.extend(
                    osis_book_header(heb_book_name)
                )
            else:
                res.append(
                    osis_chapter_footer(
                        heb_book_name,
                        heb_chapter_name
                    )
                )
            res.append(osis_chapter_header(heb_book_name, heb_chapter_name))
        elif verse_re.match(line):
            match = verse_re.match(line)
            heb_verse_name = match.group('heb_verse_name')
            verse_content = match.group('verse_content')
            res.append(
                osis_verse(
                    heb_book_name,
                    heb_chapter_name,
                    heb_verse_name,
                    verse_content,
                )
            )
    res.append(osis_chapter_footer(heb_book_name, heb_chapter_name))
    res.extend(osis_book_footer(heb_book_name))
    return '\n'.join(res) + '\n'

with open('header.osis', 'r') as f:
    osis_header = f.read()

with open('daniel.mw', 'r') as f:
    danmw = f.read()

with open('ezra.mw', 'r') as f:
    ezramw = f.read()

with open('footer.osis', 'r') as f:
    osis_footer = f.read()

with open('SLGH.osis', 'w') as f:
    f.write(
        osis_header +
        mw_content_to_osis(danmw) +
        mw_content_to_osis(ezramw) +
        osis_footer
    )
