#!/usr/bin/python
import os, re, sys, shutil
import math, time
from ROOT import *

c1 = TCanvas( 'c1', 'Dynamic Filling Example', 200, 10, 700, 500 )
c1.GetFrame().SetFillColor( 21 )
c1.GetFrame().SetBorderSize( 6 )
c1.GetFrame().SetBorderMode( -1 )
c1.Divide(1,2)

ltemp0 = TLine()
ltemp0.SetY1(0)
ltemp0.SetY2(0)
ltemp0.SetLineColor(2)
lhumi0 = TLine()
lhumi0.SetY1(10)
lhumi0.SetY2(10)
lhumi0.SetLineColor(2)

ltempX = TLine()
ltempY = TLine()
lhumiX = TLine()
lhumiY = TLine()

ltempX.SetLineStyle(7)
ltempY.SetLineStyle(7)
lhumiX.SetLineStyle(7)
lhumiY.SetLineStyle(7)

ltempX.SetLineWidth(1)
ltempY.SetLineWidth(1)
lhumiX.SetLineWidth(1)
lhumiY.SetLineWidth(1)

sh = TSignalHandler( kSigInterrupt, False )
sh.Add()
sh.Connect( "Notified()", "TROOT", gROOT, "SetInterrupt()" )

inputf = 'logfiles/temperature.log'
inputf2 = 'logfiles/humidity.log'
timeUnit=60
print '>> [INFO] Reading %s...'%inputf

while (1):
	global count
	gh = TGraph(inputf)
	gh2 = TGraph(inputf2)

        # Temperature
	x0, y0= Double(0), Double(0)
	gh.GetPoint(0, x0, y0)
	count=0
	up=0
	down=0
        endT=0.
        xmax=0.
        xmin=0.
        ymax=0.
        ymin=0.
        for i in xrange(0, gh.GetN()):
		x, y= Double(0), Double(0)
		gh.GetPoint(i,x,y)
		gh.SetPoint(i,(x-x0)/timeUnit, y)
                if i == 0:
                    xmax=(x-x0)/timeUnit
                    xmin=(x-x0)/timeUnit
                    ymax=y
                    ymin=y
                if i == gh.GetN()-1:
                    endT = y
                    ltempX.SetY1(y)
                    ltempX.SetY2(y)
                    ltempY.SetX1((x-x0)/timeUnit)
                    ltempY.SetX2((x-x0)/timeUnit)
                if xmax < (x-x0)/timeUnit:
                    xmax = (x-x0)/timeUnit
                if xmin > (x-x0)/timeUnit:
                    xmin = (x-x0)/timeUnit
                if ymax < y:
                    ymax = y
                if ymin > y:
                    ymin = y

                # Calcaulate cycle
		inc=y-y0
		if inc<0 and y<-23.5:
                    down=1
                    y0=y
		if inc>0 and down and y>18.5:
                    up=1
                    y0=y
		if up and down and inc<0:
                    count=count+1
                    up=0
                    down=0
        ltemp0.SetX1(int(xmin))
        ltemp0.SetX2(int(xmax)+5)
        ltempX.SetX1(int(xmin))
        ltempX.SetX2(int(xmax)+5)
        ltempY.SetY1(int(ymin)-5)
        ltempY.SetY2(int(ymax)+5)
        gh.GetXaxis().SetRangeUser(int(xmin), int(xmax)+5)
        #gh.GetXaxis().SetRangeUser(int(xmin), xmax*1.25)
        gh.GetYaxis().SetRangeUser(int(ymin)-5, int(ymax)+5)
        titleT="Time: %.1f hrs, T: %+.2f #circC ( Cycles %d done )"%( xmax/60, endT, count)

        # humidity 
        endH=0.
        xmax=0.
        xmin=0.
        ymax=0.
        ymin=0.
	gh2.GetPoint(0, x0, y0)
	for i in xrange(0, gh2.GetN()):
		x, y= Double(0), Double(0)
		gh2.GetPoint(i,x,y)
		gh2.SetPoint(i,(x-x0)/timeUnit, y)
                if i == 0:
                    xmax=(x-x0)/timeUnit
                    xmin=(x-x0)/timeUnit
                    ymax=y
                    ymin=y
                if i == gh2.GetN()-1:
                    endH = y
                    lhumiX.SetY1(y)
                    lhumiX.SetY2(y)
                    lhumiY.SetX1((x-x0)/timeUnit)
                    lhumiY.SetX2((x-x0)/timeUnit)
                if xmax < (x-x0)/timeUnit:
                    xmax = (x-x0)/timeUnit
                if xmin > (x-x0)/timeUnit:
                    xmin = (x-x0)/timeUnit
                if ymax < y:
                    ymax = y
                if ymin > y:
                    ymin = y
        lhumi0.SetX1(int(xmin))
        lhumi0.SetX2(int(xmax)+5)
        lhumiX.SetX1(int(xmin))
        lhumiX.SetX2(int(xmax)+5)
        lhumiY.SetY1(int(ymin)-1)
        lhumiY.SetY2(int(ymax)+3)
        gh2.GetXaxis().SetRangeUser(int(xmin), int(xmax)+5)
        gh2.GetYaxis().SetRangeUser(int(ymin)-1, int(ymax)+3)
        titleH="Time: %.1f hrs, H: %.2f %s"%( xmax/60, endH, '%')

        # Draw()
	gh.SetMarkerStyle(22)
	gh.SetMarkerSize(1)
	gh.SetMarkerColor(kBlue-2)
	gh.SetLineWidth(2)
	gh.SetLineColor(kRed)
	gh.SetTitle(titleT)
	gh.GetXaxis().SetTitle("Time [min]")
	gh.GetXaxis().SetLabelFont(42);
	gh.GetXaxis().SetLabelSize(0.04);
	#gh.GetXaxis().SetTitleSize(0.06);
	gh.GetXaxis().SetTitleFont(42);
	gh.GetYaxis().SetTitle("Temperature [#circC]");
	gh.GetYaxis().SetLabelFont(42);
	gh.GetYaxis().SetLabelSize(0.09);
	gh.GetYaxis().SetTitleSize(0.08);
	gh.GetYaxis().SetTitleOffset(0.55);

	gh2.SetMarkerStyle(22)
	gh2.SetMarkerSize(1)
	gh2.SetMarkerColor(kBlue-2)
	gh2.SetLineWidth(2)
	gh2.SetLineColor(kRed)
	gh2.SetTitle(titleH)
	gh2.GetXaxis().SetTitle("Time [min]")
	gh2.GetXaxis().SetLabelFont(42);
	gh2.GetXaxis().SetLabelSize(0.04);
	#gh2.GetXaxis().SetTitleSize(0.06);
	gh2.GetXaxis().SetTitleFont(42);
	gh2.GetYaxis().SetTitle("RH [%]")
	gh2.GetYaxis().SetLabelFont(42);
	gh2.GetYaxis().SetLabelSize(0.09);
	gh2.GetYaxis().SetTitleSize(0.08);
	gh2.GetYaxis().SetTitleOffset(0.55);

        # Draw on c1
	c1.cd(1)
	gh.Draw("APL")
        ltemp0.Draw()
        ltempY.Draw()
        ltempX.Draw()
	gh.Draw("PLSAME")

	c1.cd(2)
	gh2.Draw("APL")
        lhumi0.Draw()
        lhumiX.Draw()
        lhumiY.Draw()
	gh2.Draw("PLSAME")

        c1.RedrawAxis();

	c1.Modified()
	c1.Update()
	time.sleep(2)
	if gROOT.IsInterrupted():      # allow user interrupt
		c1.SaveAs('temperature.pdf')
		break


