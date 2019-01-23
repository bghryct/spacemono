import sys
import os
import re
import copy
import time
from glyphsLib import GSFont
from glyphsLib import GSGlyph

start = time.time()

filename = sys.argv[-1]

font = GSFont(filename)

nonExportGlyphs = []
baseIndex = 0
for glyph in font.glyphs:
    if glyph.export == False:
        nonExportGlyphs.append(baseIndex)
        baseIndex -= 1
    baseIndex += 1

for baseIndex in nonExportGlyphs:
    del font._glyphs[baseIndex]

font.save(filename)