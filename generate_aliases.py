import os
import unicodedata

# print each svg file in the current directory
svgs = [filename for filename in os.listdir(os.curdir) if filename.endswith('.svg')]

skin_tone_modifiers = [
    '1f3fb',
    '1f3fc',
    '1f3fd',
    '1f3fe',
    '1f3ff'
]

# dictionary to store glyphs
baseGlyphs = {}

for svg in svgs:
    filename, extension = os.path.splitext(svg)  # separate file into filename and extension
    codepoints = filename.split('_')  # create list of codepoints sequence
    if set(codepoints) & set(skin_tone_modifiers):  # checking if the set of codepoints is overlapping with set of
        # skintone modifiers
        basic_sequence = [codepoint for codepoint in codepoints if codepoint not in skin_tone_modifiers]
        base_filename = '_'.join(basic_sequence)  # join codepoint sequence to create base filename
        baseGlyphs.setdefault(base_filename, []).append(filename)  # making dictionary with base filename as key,
        # and aliases as values in a list

# Formatting Output File
exclude = ['JOINER', 'FITZPATRICK']  # excluding zero width joiners and skin tone variations (Fitzpatrick)
f = open("aliasOutput.txt", "w")


# Formatting comments
def getComment(firstLine):
    f.write(firstLine + ' ')
    emojiFrom, emojiTo = firstLine.split(';')
    elements = emojiFrom.split('_')
    f.write(" # " + ' ')
    for hexCodepoint in elements:
        deCodepoint = int(hexCodepoint.lstrip('uU'), 16)
        character = chr(deCodepoint)
        uniName = unicodedata.name(character)
        if not set(uniName.split()) & set(exclude):
            f.write(uniName.lower() + ' ')
    f.write('\n')


for key in baseGlyphs.keys():
    firstLine = "{};{}".format(key, baseGlyphs[key][0])
    getComment(firstLine)
    for i in baseGlyphs.get(key)[1:]:
        f.write("{};{}".format(key,i))
        f.write('\n')
