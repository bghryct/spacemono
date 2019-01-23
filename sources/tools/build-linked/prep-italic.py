import sys
import os
import re
import time
import copy
from glyphsLib import GSFont
from glyphsLib import GSGlyph
from glyphsLib import GSLayer

filename = sys.argv[-1]
font = GSFont(filename)

delMasters = []
delInstances = []
delAxes = []

i = 0
for master in font.masters:
    if re.match('.*Oblique.*', master.name) == None:
        for glyph in font.glyphs:
            delLayers = []
            for layer in glyph.layers:
                if layer.layerId == master.id or layer.associatedMasterId == master.id:
                    delLayers.append(layer.layerId)
            for layerId in delLayers:
                del glyph.layers[layerId]
        delMasters.append(i)
        i = i - 1
    else:
        for glyph in font.glyphs:
            delLayers = []
            for layer in glyph.layers:
                if re.match("^RO2 B.*", layer.name) != None or re.match("^BO2 B.*", layer.name) != None:
                    glyph.layers[layer.associatedMasterId].layerId, layer.layerId = layer.layerId, glyph.layers[layer.associatedMasterId].layerId
                elif layer.layerId != layer.associatedMasterId:
                    delLayers.append(layer.layerId)
            for layerId in delLayers:
                del glyph.layers[layerId]
    i = i + 1

# k = 0
# for instance in font.instances:
#     if instance.isItalic == 0:
#         delInstances.append(k)
#         k = k - 1
#     k = k + 1

for masterIndex in delMasters:
    del font.masters[masterIndex]

# for instanceIndex in delInstances:
#     del font.instances[instanceIndex]

for parameter in font.customParameters:
    if parameter.name == "Axes":
        j = 0
        for axis in parameter.value:
            if axis["Tag"] != "wght":
                delAxes.append(j)
                j = j - 1
            j = j + 1

        for axisIndex in delAxes:
            parameter.value.pop(axisIndex)

print "Built Space Mono Italic source"

font.save(filename)
