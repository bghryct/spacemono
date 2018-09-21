font = Glyphs.font
import math
import re

# Sync everything to the HOI layer

## Modify these variables to suit your naming conventions ##
############################################################

nameA = "Regular$"
nameB = "B"
nameC1 = "C1"
nameC2 = "C2"
nameC3 = "C3"
nameD1 = "D1"
nameD2 = "D2"
nameD3 = "D3"
nameHOI = "HOI"

nodeOffset = (11)

############################################################
############################################################

for select in font.selectedLayers:
	for layer in select.parent.layers:
		if re.match(nameA, layer.name) != None:
			idA = layer.layerId
		elif re.match(nameB, layer.name) != None:
			idB = layer.layerId
		elif re.match(nameC1, layer.name) != None:
			idC1 = layer.layerId
		elif re.match(nameC2, layer.name) != None:
			idC2 = layer.layerId
		elif re.match(nameC3, layer.name) != None:
			idC3 = layer.layerId
		elif re.match(nameD1, layer.name) != None:
			idD1 = layer.layerId
		elif re.match(nameD2, layer.name) != None:
			idD2 = layer.layerId
		elif re.match(nameD3, layer.name) != None:
			idD3 = layer.layerId
		elif re.match(nameHOI, layer.name) != None:
			idHOI = layer.layerId

def updateA(glyph, i):
	glyph.layers[idA].paths[0].nodes[i+nodeOffset].x = glyph.layers[idHOI].paths[i].nodes[0].x
	glyph.layers[idA].paths[0].nodes[i+nodeOffset].y = glyph.layers[idHOI].paths[i].nodes[0].y
		
def	updateC(glyph, i):
		glyph.layers[idC1].paths[0].nodes[i+nodeOffset].x = glyph.layers[idHOI].paths[i].nodes[1].x
		glyph.layers[idC1].paths[0].nodes[i+nodeOffset].y = glyph.layers[idHOI].paths[i].nodes[1].y
		
		glyph.layers[idC2].paths[0].nodes[i+nodeOffset].x = glyph.layers[idHOI].paths[i].nodes[1].x
		glyph.layers[idC2].paths[0].nodes[i+nodeOffset].y = glyph.layers[idHOI].paths[i].nodes[1].y
		
		glyph.layers[idC3].paths[0].nodes[i+nodeOffset].x = glyph.layers[idHOI].paths[i].nodes[1].x
		glyph.layers[idC3].paths[0].nodes[i+nodeOffset].y = glyph.layers[idHOI].paths[i].nodes[1].y
	
def updateD(glyph, i):
		glyph.layers[idD1].paths[0].nodes[i+nodeOffset].x = glyph.layers[idHOI].paths[i].nodes[2].x
		glyph.layers[idD1].paths[0].nodes[i+nodeOffset].y = glyph.layers[idHOI].paths[i].nodes[2].y
		
		glyph.layers[idD2].paths[0].nodes[i+nodeOffset].x = glyph.layers[idHOI].paths[i].nodes[2].x
		glyph.layers[idD2].paths[0].nodes[i+nodeOffset].y = glyph.layers[idHOI].paths[i].nodes[2].y
		
		glyph.layers[idD3].paths[0].nodes[i+nodeOffset].x = glyph.layers[idHOI].paths[i].nodes[2].x
		glyph.layers[idD3].paths[0].nodes[i+nodeOffset].y = glyph.layers[idHOI].paths[i].nodes[2].y
	
def updateB(glyph, i):
	glyph.layers[idB].paths[0].nodes[i+nodeOffset].x = glyph.layers[idHOI].paths[i].nodes[3].x
	glyph.layers[idB].paths[0].nodes[i+nodeOffset].y = glyph.layers[idHOI].paths[i].nodes[3].y

for select in font.selectedLayers:
	for i in range(len(select.parent.layers[idHOI].paths)):
		updateA(select.parent, i)	
		updateC(select.parent, i)
		updateD(select.parent, i)
		updateB(select.parent, i)