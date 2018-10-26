import sys
import re
import uuid
import copy
from glyphsLib import GSFont
from glyphsLib import GSGlyph
from glyphsLib import GSLayer
from glyphsLib import GSFontMaster
import objc

filename = sys.argv[-1]
font = GSFont(filename)

# Code for converting HOI glyphs file with virtual masters to something compatible with fontmake

locations = []
masterMapping = {}
deleteLayers = []
deleteGlyphs = []

glyphIndex = 0
for glyph in font.glyphs:
	if glyph.export == True:
		stopIter = len(glyph.layers)
		layerIndex = 0
		for layer in glyph.layers:
			print glyph.name, layer.name
			if layerIndex == stopIter - 1:
				break
			layerIndex = layerIndex + 1
			if re.match(".*\{.*\}", layer.name) != None:
				location = re.sub("\}", "", re.sub(".*\{", "", layer.name))
				location = [int(i) if i.isdigit() else int(i) for i in location.split(',')]
				if location in locations:
					pass
				else:
					# for master in font.masters:
					# 	print master, master.id
					# print font.masters[-1]
					# print "\n"
					# print "Before Location",  font.masters[1].name

					locations.append(location)
					newMaster = GSFontMaster()
					newMaster.id = None # str(uuid.uuid4()).upper()
					newMaster.name = str(location)
					font.masters.append(newMaster)

					attrIndex = 0
					for item in dir(font.masters[layer.associatedMasterId]):
						# print item, attrIndex
						if attrIndex > 27 and attrIndex != 44 and attrIndex != 46 and attrIndex != 38 and attrIndex != 48 and attrIndex != 47 and attrIndex != 31 and attrIndex != 54 and attrIndex != 52 and attrIndex != 32:
							# print str(item), getattr(font.masters[layer.associatedMasterId], str(item))
							setattr(font.masters[-1], str(item), getattr(font.masters[layer.associatedMasterId], str(item)))
						else:
							pass # print "NOT ADDED:", str(item), getattr(font.masters[layer.associatedMasterId], str(item))
						attrIndex = attrIndex + 1

					
					font.masters[-1].weightValue = location[0]
					font.masters[-1].widthValue = location[1]
					font.masters[-1].customValue = location[2]
					font.masters[-1].customValue1 = location[3]
					font.masters[-1].customValue2 = location[4]
					font.masters[-1].customValue3 = location[5]

		
					print "New Master Location added at %s" % str(location), glyph.name
					# for master in font.masters:
					# 	print master.name, font.masters[1].name
					# 	# print master.id, font.masters[1].id
					# 	# print font.masters[-1].name
					# print "\n\n"

					masterMapping.update({str(location): (font.masters[-1].id, layer.associatedMasterId)})
					# for key in masterMapping.keys():
					# 	print key
	else: 
		deleteGlyphs.append([glyph.name, glyphIndex])
	glyphIndex = glyphIndex + 1

before = len(font.glyphs)

# CLEAN THIS UP, don't need a tuple
for i in range(len(deleteGlyphs)):
	index = deleteGlyphs[i][1]
	del font._glyphs[index]
	for j in range(len(deleteGlyphs)):
		if deleteGlyphs[j][1] > index:
			deleteGlyphs[j][1] = (deleteGlyphs[j][1] - 1)

after = len(font.glyphs)

print "Removed %d glyph(s)" % (before - after)


	
for glyph in font.glyphs:
	for layer in glyph.layers:
		if re.match(".*\{.*\}", layer.name) != None:
			location = re.sub("\}", "", re.sub(".*\{", "", layer.name))
			location = [int(i) if i.isdigit() else int(i) for i in location.split(',')]
			deleteLayers.append([glyph.name, layer.layerId])
			glyph.layers[masterMapping[str(location)][0]].paths = []
			for path in layer.paths:
				glyph.layers[masterMapping[str(location)][0]].paths.append(copy.copy(path))
			glyph.layers[masterMapping[str(location)][0]].width = layer.width
		elif re.match("\[.*\]", layer.name) !=None:
			layerKey = re.sub(" Italic", "", layer.name)
			glyph.layers[masterMapping[layerKey][0]].paths = []
			for path in glyph.layers[masterMapping[layerKey][1]].paths:
				glyph.layers[masterMapping[layerKey][0]].paths.append(copy.copy(path))
			glyph.layers[masterMapping[layerKey][0]].width = glyph.layers[masterMapping[layerKey][1]].width
				
for i in range(len(deleteLayers)):
	print "Deleted Layer:", font.glyphs[deleteLayers[i][0]].layers[deleteLayers[i][1]]
	del font.glyphs[deleteLayers[i][0]].layers[deleteLayers[i][1]]

font.save(filename)