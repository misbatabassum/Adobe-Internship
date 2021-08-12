from fontTools.ttLib import TTFont

import os
import re


def change_font_version(directory, font_name):
    font_path = os.getcwd() + '/' + directory + '/' + str(font_name)
    font = TTFont(str(font_path))
    head_var = font['head']  # getting head table
    name_var = font['name']  # getting name table

    # Grabbing the version number from name table
    name_table = name_var.getName(5, 3, 1, 1033)
    version_num = (str(name_table).lstrip("Version "))

    # checking if name table version (correct) is in head table (incorrect)
    if name_table == head_var:
        print(font + 'correct version')  # no change needed
    elif re.search('\d+\.\d+\.\d+', version_num):  # version number in name table has 2 decimal points
        string = 'Version ' + str(head_var.fontRevision)[0:5]  # trimming string to 5 characters
        name_var.setName(string, 5, 1, 0, 0)  # setting for WDHS field
        name_var.setName(string, 5, 3, 1, 1033)  # setting for MAC field
    else:  # store name table version number into head table
        head_var.fontRevision = float(version_num)

    # re-saving glyph table, so it updates to correct numbers
    font['glyf'].data = font['glyf'].compile(font)

    # saving changes
    font.save(font_path)


# traverses through different fields in order to remove line break
def fix_line_breaks(directory, font_name):
    font_path = os.getcwd() + '/' + directory + '/' + str(font_name)
    font = TTFont(str(font_path))
    name_table = font['name']

    my_dict = {
        'copyright_MAC': [0, 1, 0, 0],
        'trademark_MAC': [7, 1, 0, 0],
        'designer_MAC': [9, 1, 0, 0],
        'desc_MAC': [10, 1, 0, 0],
        'liscense_desc_MAC': [13, 1, 0, 0],
        'copyright_WDHS': [0, 3, 1, 1033],
        'trademark_WDHS': [7, 3, 1, 1033],
        'designer_WDHS': [9, 3, 1, 1033],
        'desc_WDHS': [10, 3, 1, 1033],
        'liscense_desc_WDHS': [13, 3, 1, 1033]
    }

    # traversing dictionary to remove \n accordingly from specified field
    for name in my_dict.items():
        fix(name[1], name_table)

    font.save(font_path)


# searches and removes the line break
def fix(lst, name_table):
    string = str(name_table.getName(lst[0], lst[1], lst[2], lst[3]))

    if lst[3] == 1033:
        if not string:  # try: if string == null
            string = str(name_table.getName(13, 3, 1, 1041))
            lst[3] = 1041

    if '\n' in string:
        new_string = string.replace("\n", " ")
        name_table.setName(new_string, lst[0], lst[1], lst[2], lst[3])  # making substitution dynamic


def fix_monospace(directory, font_name):
    font_path = os.getcwd() + '/' + directory + '/' + str(font_name)
    font = TTFont(str(font_path))
    post_table = font['post']
    os2_table = font['OS/2']

    # for monospaced fonts only
    if post_table.isFixedPitch != 1:
        post_table.isFixedPitch = 1
    if os2_table.panose.bProportion != 9:
        os2_table.panose.bProportion = 9

    font.save(font_path)


def fix_whitespace(directory, font_name):
    font_path = os.getcwd() + '/' + directory + '/' + str(font_name)
    font = TTFont(str(font_path))
    cmap = font.getBestCmap()
    sp_glyph_name = cmap[0x0020]  # 0x0020 - whitespace value taken from cmap
    nbsp_glyph_name = cmap[0x00A0]  # 0x00A0 - non-breaking space value taken from cmap
    hmtx = font['hmtx']  # horizontal metrics table
    hmtx[nbsp_glyph_name] = hmtx[sp_glyph_name]  # correcting non-breaking space value

    font.save(font_path)


# renaming the glyphs with '#' to have '_' instead so fonttools doesn’t try to convert them back to the original name
def fix_unique_glyph(directory, font_name):
    font_path = os.getcwd() + '/' + directory + '/' + str(font_name)
    font = TTFont(str(font_path))

    glyph_order = font.getGlyphOrder()
    for i, glyph_name in enumerate(glyph_order):
        if '#' in glyph_name:
            glyph_order[i] = glyph_name.replace('#', '_')

    font.save(font_path)


def main():
    path = '/Users/mtabassu/Desktop/Fixing'
    for root, directories, files in os.walk(path):
        for directory in directories:
            for root, directories, files in os.walk(directory):
                print("directory: " + directory)
                for file in files:
                    print("file: " + file)
                    if file.endswith('.ttf') or file.endswith('.otf'):
                        change_font_version(directory, file)
                        fix_line_breaks(directory, file)
                        fix_monospace(directory, file)
                        fix_whitespace(directory, file)
                        fix_unique_glyph(directory, file)


if __name__ == '__main__':
    main()
