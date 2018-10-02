# encoding: utf-8

###########################################################################################################
#
#
#	Reporter Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################

import objc
import GlyphsApp
from GlyphsApp import *
from GlyphsApp.plugins import *
# from Cocoa import NSBezierPath
import math

class viewHOI(ReporterPlugin):
	sliderView = objc.IBOutlet()  # the dialog view (e.g., panel or window)
	slider1 = objc.IBOutlet()
	slider2 = objc.IBOutlet() 
	slider3 = objc.IBOutlet() 
	slider4 = objc.IBOutlet()       # the slider placed inside the view
	button = objc.IBOutlet()

	weightValue = 84.0
	slantValue = 0.0
	italicValue = 0.0
	monoValue = 1000.0
	selection = []
	nodeType = []
	angleTolerance = 5.0

	def settings(self):
		# Load .nib file next to plugin.py
		self.loadNib("sliderView", __file__)
		self.menuName = Glyphs.localize({'en': u'HOI Viewer', 'de': u'Mein Plugin'})
		self.generalContextMenus = [{'name': 'HOI Viewer', 'view': self.sliderView}]
		self.slider1.setMinValue_(84.0)
		self.slider1.setMaxValue_(132.0)
		self.slider2.setMinValue_(0.0)
		self.slider2.setMaxValue_(1000.0)
		self.slider3.setMinValue_(0.0)
		self.slider3.setMaxValue_(1000.0)
		self.slider4.setMinValue_(0.0)
		self.slider4.setMaxValue_(1000.0)

	def sliderUpdate(self):
		self.weightValue = self.slider1.floatValue()
		self.slantValue = self.slider2.floatValue()
		self.italicValue = self.slider3.floatValue()
		self.monoValue = self.slider4.floatValue()

		layer = Glyphs.font.selectedLayers[0]
		currentGlyph = layer.parent.name

		tempInstance = layer.parent.parent.instances[0].copy()
		tempInstance.name = "tempInstance"
		tempInstance.weightValue = self.weightValue
		tempInstance.widthValue = self.slantValue
		tempInstance.customValue = self.italicValue
		tempInstance.setInterpolationCustom1_(self.italicValue)
		tempInstance.setInterpolationCustom2_(self.italicValue)
		tempInstance.setInterpolationCustom3_(self.monoValue)
		self.tempInstance = tempInstance
		
		Glyphs.redraw()

	@objc.IBAction
	def slider1_(self, sender):
		self.sliderUpdate()

	@objc.IBAction
	def slider2_(self, sender):
		self.sliderUpdate()

	@objc.IBAction
	def slider3_(self, sender):
		self.sliderUpdate()

	@objc.IBAction
	def slider4_(self, sender):
		self.sliderUpdate()

	@objc.IBAction
	def button_(self, sender):
		self.selection = []
		self.nodeType = []
		Glyphs.redraw()

	def roundDotForPoint( self, thisPoint, markerWidth ):
		"""
		from Show Angled Handles by MekkaBlue
		Returns a circle with thisRadius around thisPoint.
		"""
		myRect = NSRect( ( thisPoint.x - markerWidth * 0.5, thisPoint.y - markerWidth * 0.5 ), ( markerWidth, markerWidth ) )
		return NSBezierPath.bezierPathWithOvalInRect_(myRect)

	# (1) Adding code for showing nodes and changing color based on angle
	def nodeColor(self, nodePrev, node, nodeNext):

		dx1 = node.x - nodePrev.x
		dy1 = node.y - nodePrev.y
		angle1 = math.degrees(math.atan2(dy1, dx1))

		dx2 = nodeNext.x - node.x 
		dy2 = nodeNext.y - node.y
		angle2 = math.degrees(math.atan2(dy2, dx2))

		diff = abs(angle2 - angle1)

		if diff > 180:
			diff = 360 - diff

		if diff >= (self.angleTolerance * 2):
			redValue = 1.0
			greenValue = 0.0
		elif diff < self.angleTolerance:
			redValue = (diff % self.angleTolerance) / self.angleTolerance
			greenValue = 1.0
		else:
			redValue = 1.0
			greenValue = 1.0 - ((diff % self.angleTolerance) / self.angleTolerance)

		return (redValue, greenValue)

		
	def foreground(self, layer):
		self.italicValue = self.slider3.floatValue()

		tempInstance = layer.parent.parent.instances[0].copy()
		tempInstance.name = "tempInstance"
		tempInstance.weightValue = self.weightValue
		tempInstance.widthValue = self.slantValue
		tempInstance.customValue = self.italicValue
		tempInstance.setInterpolationCustom1_(self.italicValue)
		tempInstance.setInterpolationCustom2_(self.italicValue)
		tempInstance.setInterpolationCustom3_(self.monoValue)

		currentGlyph = layer.parent.name

		t = NSBezierPath.bezierPath()

		cx1 = None
		cy1 = None
		cx2 = None
		cy2 = None

		tempFont = tempInstance.interpolatedFontProxy.glyphs[currentGlyph].layers[0].paths[0]
		tx1 = tempFont.nodes[0].x
		ty1 = tempFont.nodes[0].y
		t.moveToPoint_(NSMakePoint(tx1, ty1))

		# VF preview as fill
		for node in layer.paths[0].nodes:
			if node.type != "offcurve":
				tx2 = tempFont.nodes[node.index].x
				ty2 = tempFont.nodes[node.index].y

			if node.type == "line":
				t.lineToPoint_(NSMakePoint(tx2, ty2))
			elif node.type == "offcurve":
				if cx1 == None:
					cx1 = tempFont.nodes[node.index].x
					cy1 = tempFont.nodes[node.index].y
				else:
					cx2 = tempFont.nodes[node.index].x
					cy2 = tempFont.nodes[node.index].y
			else:
				t.curveToPoint_controlPoint1_controlPoint2_(NSMakePoint(tx2, ty2), NSMakePoint(cx1, cy1), NSMakePoint(cx2, cy2))
				cx1 = None
				cy1 = None
				cx2 = None
				cy2 = None

			tx0 = tx2
			ty0 = ty2

		t.closePath()
		NSColor.colorWithCalibratedRed_green_blue_alpha_(0.0, 0.0, 0.0, 0.2).set()
		t.fill()

		# ——————————————————————————————————————————————————————————————————————————————————————————————————————————
		# ——————————————————————————————————————————————————————————————————————————————————————————————————————————

		scale = layer.parent.parent.currentTab.scale


		p = NSBezierPath.bezierPath()
		lineScale = 0.2 / scale
		nodeScale = 8.0 / scale
		# (1) Adding code for showing nodes and changing color based on angle

		# VF preview selection
		if self.selection == []:
			for node in layer.paths[0].nodes:
				if node.selected:
					interpolatedIndex = node.index
					self.selection.append(interpolatedIndex)
					self.nodeType.append(node.type)

					try:
						x1 = x0
						y1 = y0
					except:
						x1 = tempFont.nodes[interpolatedIndex].x
						y1 = tempFont.nodes[interpolatedIndex].y

					x2 = tempFont.nodes[interpolatedIndex].x
					y2 = tempFont.nodes[interpolatedIndex].y

					x0 = x2
					y0 = y2

					ThisPoint = NSMakePoint(x2, y2)

					p.moveToPoint_(NSMakePoint(x1, y1))
					p.lineToPoint_(NSMakePoint(x2, y2))
					NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.0, 0.0, 1.0, 1.0).set()
					p.setLineWidth_(lineScale)
					p.stroke()
					# NSGraphicsContext.setShouldAntialias_(True)

					pNode = NSBezierPath.bezierPath()

					# (1) Adding code for showing nodes and changing color based on angle
					pNode.appendBezierPath_( self.roundDotForPoint( ThisPoint, nodeScale ) )

					# Changes node color based on angle
					NSColor.colorWithCalibratedRed_green_blue_alpha_(
						self.nodeColor(tempFont.nodes[interpolatedIndex - 1],  tempFont.nodes[interpolatedIndex],  tempFont.nodes[interpolatedIndex + 1])[0] ,
						self.nodeColor(tempFont.nodes[interpolatedIndex - 1],  tempFont.nodes[interpolatedIndex],  tempFont.nodes[interpolatedIndex + 1])[1] ,
						0.0,
						1.0).set()
					# NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.0, 0.0, 1.0, 1.0).set()
					pNode.fill()

					if node.type != "offcurve":
						NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.0, 0.0, 1.0, 1.0).set()
						pNode.setLineWidth_(lineScale * 4)
						pNode.stroke()

		else:
			i = 0
			for nodeIndex in self.selection:
				interpolatedIndex = nodeIndex
				try:
					x1 = x0
					y1 = y0
				except:
					x1 = tempInstance.interpolatedFontProxy.glyphs[currentGlyph].layers[0].paths[0].nodes[interpolatedIndex].x
					y1 = tempInstance.interpolatedFontProxy.glyphs[currentGlyph].layers[0].paths[0].nodes[interpolatedIndex].y

				x2 = tempInstance.interpolatedFontProxy.glyphs[currentGlyph].layers[0].paths[0].nodes[interpolatedIndex].x
				y2 = tempInstance.interpolatedFontProxy.glyphs[currentGlyph].layers[0].paths[0].nodes[interpolatedIndex].y

				x0 = x2
				y0 = y2

				ThisPoint = NSMakePoint(x2, y2)

				p.moveToPoint_(NSMakePoint(x1, y1))
				p.lineToPoint_(NSMakePoint(x2, y2))
				NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.0, 0.0, 1.0, 1.0).set()
				p.setLineWidth_(lineScale)
				p.stroke()

				pNode = NSBezierPath.bezierPath()

				# (1) Adding code for showing nodes and changing color based on angle
				pNode.appendBezierPath_( self.roundDotForPoint( ThisPoint, nodeScale ) )

				# Changes node color based on angle
				NSColor.colorWithCalibratedRed_green_blue_alpha_(
					self.nodeColor(tempFont.nodes[interpolatedIndex - 1],  tempFont.nodes[interpolatedIndex],  tempFont.nodes[interpolatedIndex + 1])[0] ,
					self.nodeColor(tempFont.nodes[interpolatedIndex - 1],  tempFont.nodes[interpolatedIndex],  tempFont.nodes[interpolatedIndex + 1])[1] ,
					0.0,
					1.0).set()
				pNode.fill()

				if self.nodeType[i] != "offcurve":
					NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.0, 0.0, 1.0, 1.0).set()
					pNode.setLineWidth_(lineScale * 4)
					pNode.stroke()

				i = i + 1

	# def inactiveLayer(self, layer):
	# 	NSColor.redColor().set()
	# 	if layer.paths:
	# 		layer.bezierPath.fill()
	# 	if layer.components:
	# 		for component in layer.components:
	# 			component.bezierPath.fill()

	# def preview(self, layer):
	# 	NSColor.blueColor().set()
	# 	if layer.paths:
	# 		layer.bezierPath.fill()
	# 	if layer.components:
	# 		for component in layer.components:
	# 			component.bezierPath.fill()
	
	def doSomething(self):
		print 'Just did something'
		
	def conditionalContextMenus(self):

		# Empty list of context menu items
		contextMenus = []

		# Execute only if layers are actually selected
		if Glyphs.font.selectedLayers:
			layer = Glyphs.font.selectedLayers[0]
			
			# Exactly one object is selected and it’s an anchor
			if len(layer.selection) == 1 and type(layer.selection[0]) == GSAnchor:
					
				# Add context menu item
				contextMenus.append({'name': '2nd View', 'view': self.sliderView})
				contextMenus.append({'name': '2nd View', 'view': self.slider})

		# Return list of context menu items
		return contextMenus

	def doSomethingElse(self):
		print 'Just did something else'

	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__