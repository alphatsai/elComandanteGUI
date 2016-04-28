#!/usr/bin/python
#import sys
#import os
##import ROOT
#from ROOT import *
import os, re, sys, shutil
import math, time
from ROOT import *

class gMainFrame(TGMainFrame):

	def __init__(self, parent, width, height):
		TGMainFrame.__init__(self, parent, width, height)

	def CloseWindow(self):
		print "closing"
		gApplication.Terminate(0)

	def doDraw(self):
		print "Yp"

	def __del__(self):
		self.CloseWindow()

class gMainWindow():

	def __init__(self, parent, width, height, app):
		self.Application = app
		self.MainFrame = gMainFrame(parent, width, height)
		#self.MainFrame = TGMainFrame(parent, width, height)
		self.Canvas = TRootEmbeddedCanvas("Canvas", self.MainFrame, 1000, 500)
		self.MainFrame.AddFrame(self.Canvas, TGLayoutHints())
		self.ButtonsFrame = TGHorizontalFrame(self.MainFrame, 200, 40)
		self.DrawButton = TGTextButton(self.ButtonsFrame, '&Draw')
		self.DrawButton.Connect('Clicked()', 'gMainFrame', self.MainFrame, 'CloseWindow(self)')
		self.ButtonsFrame.AddFrame(self.DrawButton, TGLayoutHints())

		# Following line give a seg. fault
		#self.DrawButton.Connect('clicked()', 'gMainWindow', self, 'draw()')
		self.ExitButton = TGTextButton(self.ButtonsFrame, '&Exit')
		self.ExitButton.SetCommand("gApplication.Terminate(0)")
		self.ButtonsFrame.AddFrame(self.ExitButton, TGLayoutHints())
		self.MainFrame.AddFrame(self.ButtonsFrame, TGLayoutHints())
		self.MainFrame.SetWindowName('My first GUI')
		self.MainFrame.MapSubwindows()
		self.MainFrame.Resize(self.MainFrame.GetDefaultSize())
		self.MainFrame.MapWindow()

		#c1 = TCanvas( 'c1', 'Dynamic Filling Example', 200, 10, 700, 500 )

		c1 = self.Canvas.GetCanvas();
		c1.GetFrame().SetFillColor( 21 )
		c1.GetFrame().SetBorderSize( 6 )
		c1.GetFrame().SetBorderMode( -1 )

	#def doDraw(self):		
		sh = TSignalHandler( kSigInterrupt, False )
		sh.Add()
		sh.Connect( "Notified()", "TROOT", gROOT, "SetInterrupt()" )
		
		inputf = '../example/logfiles/temperature.log'
		timeUnit=60
		print '>> [INFO] Reading %s...'%inputf
		while (1):
			gh = TGraph(inputf)
		
			x0, y0= Double(0), Double(0)
			gh.GetPoint(0, x0, y0)
			for i in xrange(0, gh.GetN()):
				x, y= Double(0), Double(0)
				gh.GetPoint(i,x,y)
				gh.SetPoint(i,(x-x0)/timeUnit, y)
		
			gh.SetMarkerStyle(22)
			gh.SetMarkerSize(1)
			gh.SetMarkerColor(kBlue-2)
			gh.SetLineWidth(2)
			gh.SetLineColor(kRed)
			gh.SetTitle("")
			gh.GetXaxis().SetTitle("Time [min]")
			gh.GetYaxis().SetTitle("Temperature [#circC]")
			gh.Draw("APL")
		
			c1.Modified()
			c1.Update()
			#time.sleep(4)
			if gROOT.IsInterrupted():      # allow user interrupt
				c1.SaveAs('temperature.pdf')
				break

	def __del__(self):
		self.MainFrame.CloseWindow()
		self.MainFrame.Cleanup()
		self.Application.Terminate(0)

if __name__ == '__main__':
	#ROOT.gROOT.Reset()
	app = gApplication
	window = gMainWindow(gClient.GetRoot(), 200, 200, app)
	print "Is gApplication running ? %d" % app.IsRunning()
	app.Run()
