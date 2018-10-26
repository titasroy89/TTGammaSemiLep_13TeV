from ROOT import TFile, TPad, gROOT, gStyle, TCanvas, SetOwnership, TLegend, kBlack, kRed, kBlue, TF1,TH1F
import math
import os
import sys
from array import array
import CMS_lumi
from Style import *
from optparse import OptionParser
from Quiet import Quiet

gROOT.SetBatch(True)

parser = OptionParser()
    
parser.add_option("-c", "--channel", dest="channel", default="mu",type='str',
                  help="Specify which channel mu or ele? default is mu" )
parser.add_option("--Tight","--tight", dest="isTightSelection", default=False,action="store_true",
                     help="Use 4j2t selection" )
parser.add_option("--bins","--bins", dest="isbinsCR", default=False,action="store_true",
                     help="Use Fit regions" )


(options, args) = parser.parse_args()

TightSelection = options.isTightSelection
isbinsCR = options.isbinsCR

if TightSelection:
	dir_="_tight"
elif isbinsCR:
	dir_="_binned"
else:
	dir_=""
finalState = options.channel
thestyle = Style()

thestyle.SetStyle()

ROOT.gROOT.ForceStyle()
# gStyle.SetOptTitle(0)
# gStyle.SetOptStat(0)
gStyle.SetMarkerStyle(1)


process_signal = {"TTGamma_Prompt":["t#bar{t}+#gamma Prompt"],
		  "TTGamma_NonPrompt":["t#bar{t}+#gamma Nonprompt"],
		  "TTbar_Prompt": ["t#bar{t} Prompt"],
		  "TTbar_NonPrompt": ["t#bar{t} Nonprompt"],
		  "VGamma_Prompt":["V+#gamma Prompt"],
		  "VGamma_NonPrompt":["V+#gamma Nonprompt"],
#		  "SingleTop_Prompt":["SingleTop Prompt"],
 #                 "SingleTop_NonPrompt":["SingleTop Nonprompt"],
#		  "VJets_Prompt":["V+jets Prompt"],
#		  "VJets_NonPrompt":["V+jets Nonprompt"],
		  "Other_Prompt":["Other Prompt"],
		  "Other_NonPrompt":["Other Nonprompt"],
		  "Other":["Other"],
#		  "SingleTop":["SingleTop"],
#		  "VJets":["V+jets"],
		  "VGamma":["V+#gamma"],
		 # "ZGamma":["Z+#gamma"],
		  "TTbar":["t#bar{t}"],
		  "TTGamma":["t#bar{t}+#gamma"],
		  #"TTbar_DD":["t#bar{t} DataDriven"],
		  }

import CMS_lumi
H = 600;
W = 800;


# references for T, B, L, R                                                                                                             
T = 0.08*H
B = 0.12*H
L = 0.12*W
R = 0.1*W
observe_={"M3":["M3 GeV"],
	"ChHad":["Photon Charge Hadron Isolation (GeV)"],
	"M3_control":["M3 (GeV)"],
	}
if isbinsCR:
	observe_={"M3":["M3 GeV"],
        "ChHad":["Photon Charge Hadron Isolation (GeV)"],
        "M3_control":["Events in 0 photon CR"],
	"Njet":["Events in 0 btag CR"],
	}


c1 = TCanvas('c1','c1',W,H)
c1.SetFillColor(0)
c1.SetBorderMode(0)
c1.SetFrameFillStyle(0)
c1.SetFrameBorderMode(0)
c1.SetLeftMargin( L/W )
c1.SetRightMargin( R/W )
c1.SetTopMargin( T/H )
c1.SetBottomMargin( B/H )
c1.SetTickx(0)
c1.cd()
c1.ResetDrawn()
c2 = TCanvas('c2','c2',W,H)
c2.SetFillColor(0)
c2.SetBorderMode(0)
c2.SetFrameFillStyle(0)
c2.SetFrameBorderMode(0)
c2.SetLeftMargin( L/W )
c2.SetRightMargin( R/W )
c2.SetTopMargin( T/H )
c2.SetBottomMargin( B/H )
c2.SetTickx(0)
c2.SetTicky(0)
c2.Draw()
c2.cd()
padRatio = 0.25
padOverlap = 0.15

padGap = 0.01
pad1 = TPad("zxc_p1","zxc_p1",0,padRatio-padOverlap,1,1)
pad2 = TPad("qwe_p2","qwe_p2",0,0,1,padRatio+padOverlap)
pad1.SetLeftMargin( L/W )
pad1.SetRightMargin( R/W )
pad1.SetTopMargin( T/H/(1-padRatio+padOverlap) )
pad1.SetBottomMargin( (padOverlap+padGap)/(1-padRatio+padOverlap) )
pad2.SetLeftMargin( L/W )
pad2.SetRightMargin( R/W )
pad2.SetTopMargin( (padOverlap)/(padRatio+padOverlap) )
pad2.SetBottomMargin( B/H/(padRatio+padOverlap) )

pad1.SetFillColor(0)
pad1.SetBorderMode(0)
pad1.SetFrameFillStyle(0)
pad1.SetFrameBorderMode(0)
pad1.SetTickx(0)
pad1.SetTicky(0)

pad2.SetFillColor(0)
pad2.SetFillStyle(4000)
pad2.SetBorderMode(0)
pad2.SetFrameFillStyle(0)
pad2.SetFrameBorderMode(0)
pad2.SetTickx(0)
pad2.SetTicky(0)

c2.cd()
pad1.Draw()
pad2.Draw()

SetOwnership(pad1,False)
SetOwnership(pad2,False)

if finalState=="ele":
	_file = TFile("Combine_withDDTemplateData_v6_ele_binned.root","read")
        if TightSelection :
		_file = TFile("Combine_withDDTemplateData_v6_ele_tight_binned_PDF.root","read")
else:
	_file = TFile("Combine_withDDTemplateData_v6_mu_binned.root","read")
	if TightSelection :
                _file = TFile("Combine_withDDTemplateData_v6_mu_tight_binned_PDF.root","read")
MC_signal = ["TTbar_Prompt","TTbar_NonPrompt","TTGamma_Prompt","TTGamma_NonPrompt","VGamma_Prompt","VGamma_NonPrompt","Other_Prompt","Other_NonPrompt"]
MC_control=["TTGamma","TTbar","VGamma","Other"]

process = MC_signal
if finalState=="mu":
	systematics = {"JER"     :["JER"],
		       "phosmear":["Photon scale"],
		       "phoscale":["Photon smear"],
		       "BTagSF"  :["BTag SF"],
		       "Q2"     :["Q2"],
		       "Pdf"    :["PDF"],
		       "Pdfsignal":["PDF"],
		       "PU" :["Pileup"],
		       "MuEff"  :["Muon Eff"],
		       "PhoEff" :["Photon Eff"],
		       "JECTotal": ["JEC Total"],
		       "isr":["ISR"],
		       "fsr":["FSR"],
		       "MisIDEleshape": ["MisID Ele"],
		       }
	_channelText = "#mu+jets"

else:
	systematics = {"JER"     :["JER"],
		       "phosmear":["Photon scale"],
		       "phoscale":["Photon smear"],
		       "elesmear":["Electron scale"],
		       "elescale":["Electron smear"],
		       "BTagSF"  :["BTag SF"],
		       "Q2"     :["Q2"],
		       "Pdf"    :["PDF"],
		       "Pdfsignal"    :["PDF"],
		       "PU" :["Pileup"],
		       "EleEff" :["Electron Eff"],
		       "PhoEff" :["Photon Eff"],
		       "JECTotal": ["JEC Total"],
		       "isr":["ISR"],
		       "fsr":["FSR"],
		       "MisIDEleshape": ["MisID Ele"],
		       }
	_channelText = "e+jets"

#systematics={"PU":["Pileup"],}
CMS_lumi.channelText = _channelText
CMS_lumi.writeChannelText = True
CMS_lumi.writeExtraText = True

#Signal =["TTGamma_Prompt","TTGamma_NonPrompt"]
#M3_control =["TTGamma"]

#process2=Signal


legend= TLegend(0.55, 0.69,0.89,0.89)
legend.SetBorderSize(0);
legend.SetFillStyle(0);

oneline = TF1("oneline","1",0,9e9)
oneline.SetLineColor(kBlack)
oneline.SetLineStyle(2)


#errorband.SetLineColor(kBlack)
#errorband.SetLineStyle(2)
#errorband.SetFillStyle(3245)
print _file
print observe_
for o in observe_:
        if o=="CR1" or o=="CR2" or o=="CR_0photon":continue	
	if o=="M3_control" or o=="CR_0photon":
		process = MC_control
	else:
		process = MC_signal
		
		
	for p in process:
		if finalState=="mu" and "VJets_Prompt" in p:continue
		
		if o=="ChHad" and "NonPrompt" in p:
			systematics_use={"shapeDD":["Shape unc"]}
		else:
			systematics_use=systematics
	
		
                nominal = _file.Get("%s/%s/nominal"%(o,p))
		
		if "M3" in o or "ChHad" in o:
			nominal.Scale(1.,"width")
		nominal.SetLineColor(kBlack)
		nominal.SetLineWidth(2)
		nominal.SetMarkerColor(kBlack)
                
		for sys in systematics_use:
#			
			c1.Draw()
			c1.cd()
			if sys in ["isr","fsr","Q2"]:
				
				if p not in ["TTbar_Prompt","TTGamma_Prompt","TTbar_NonPrompt","TTGamma_NonPrompt","TTbar","TTGamma"] :continue
                        if sys=="Pdf":
				if p not in ["TTbar_Prompt","TTbar_NonPrompt","TTbar"]:continue
                        if sys=="Pdfsignal" :
                                #print o, p
				if p not in ["TTGamma_Prompt","TTGamma_NonPrompt","TTGamma"]:continue
		        	
			if sys=="MisIDEleshape" and ("_Prompt" not in p):continue
			
			if o=="Njet" and sys=="BTagSF":continue		
				
			if sys=="shapeDD" and ("M3" in o or "CR" in o): continue
			if sys=="shapeDD" and o=="ChHad" and "NonPrompt" not in p:continue
			
		#	print o,sys,p, _file		
			#if sys=="Pdfsignal":
			print "%s/%s/%sUp"%(o,p,sys)	
			up =  _file.Get("%s/%s/%sUp"%(o,p,sys))
			do =  _file.Get("%s/%s/%sDown"%(o,p,sys))
			if "M3" in o or "ChHad" in o:
				up.Scale(1.,"width")
				do.Scale(1.,"width")
			_max = max(up.GetMaximum(), do.GetMaximum(), nominal.GetMaximum())


			ratioUp = up.Clone("ratio_up")
			ratioDo = do.Clone("ratio_do")

			ratioUp.Divide(nominal)
			ratioDo.Divide(nominal)

			_ratiomax = max(ratioUp.GetMaximum(),ratioDo.GetMaximum())
			_ratiomin = min(ratioUp.GetMinimum(),ratioDo.GetMinimum())
#			_ratiomax=1.1
#			_ratiomin=0.9			
			if o=="Njet":
				up.GetYaxis().SetRangeUser(0.,_max+15.)
			else:
				up.SetMaximum(_max*1.4)

			up.SetLineWidth(2)
			up.SetLineColor(kRed)
			up.SetMarkerColor(kRed)
			up.Draw("E0,hist")
			up.GetXaxis().SetTitle("%s"%(observe_[o][0]))
			up.GetYaxis().SetTitle("#LT Events / GeV #GT")

			do.SetLineStyle(1)
                        do.SetLineWidth(2)
			do.SetLineColor(kBlue)
			do.SetMarkerColor(kBlue)
			do.Draw("E0,hist,same")
			nominal.Draw("E0,hist,same")		
			
			legend.Clear()
                        errorband=nominal.Clone("errorband")
			errorband.Sumw2()
			for bin_ in range(1,nominal.GetNbinsX()+1):
				errorband.SetBinError(bin_,nominal.GetBinError(bin_))
			
			errorband.SetFillColor(kBlack)
			errorband.SetLineColor(kBlack)
			errorband.SetLineStyle(2)
			errorband.SetFillStyle(3245)
			errorband.Draw("same,E2")
			legend.SetHeader("%s"%(process_signal[p][0]))
			legend.AddEntry(up,"%s"%(systematics_use[sys][0])+" "+"Up",'lp')
			legend.AddEntry(nominal,"Nominal",'lp')
                        legend.AddEntry(do,"%s"%(systematics_use[sys][0])+" "+"Down",'lp')

        		legend.Draw("same")
  			CMS_lumi.channelText = _channelText      	
        		CMS_lumi.CMS_lumi(c1, 4, 11)


			c2.cd()
			c2.ResetDrawn()
			c2.Draw()
			c2.cd()
			pad1.Draw()
			pad2.Draw()
			
			pad1.cd()

			_ratiomax = 1+1.1*(_ratiomax-1)
			_ratiomin = 1-1.1*(1-_ratiomin)
			ratioUp.SetMaximum(_ratiomax)
			ratioUp.SetMinimum(_ratiomin)


			ratioUp.SetTitle('')
			ratioUp.GetXaxis().SetLabelSize(gStyle.GetLabelSize()/(padRatio+padOverlap))
			ratioUp.GetYaxis().SetLabelSize(gStyle.GetLabelSize()/(padRatio+padOverlap))
			ratioUp.GetXaxis().SetTitleSize(gStyle.GetTitleSize()/(padRatio+padOverlap))
			ratioUp.GetYaxis().SetTitleSize(gStyle.GetTitleSize()/(padRatio+padOverlap))

			ratioUp.GetYaxis().SetTitle("Rel. Change")
			ratioUp.GetYaxis().SetTitleOffset(gStyle.GetTitleYOffset()*(padRatio+padOverlap-0.02))
			ratioUp.GetYaxis().CenterTitle()
			ratioUp.GetXaxis().SetTitle(up.GetXaxis().GetTitle())

			up.GetXaxis().SetTitle('')
			up.SetTitle('')
			up.GetXaxis().SetLabelSize(0)
			up.GetYaxis().SetLabelSize(gStyle.GetLabelSize()/(1.-padRatio+padOverlap))
			up.GetYaxis().SetTitleSize(gStyle.GetTitleSize()/(1.-padRatio+padOverlap))
			up.GetYaxis().SetTitleOffset(gStyle.GetTitleYOffset()*(1.-padRatio+padOverlap))


			ratioUp.GetYaxis().SetNdivisions(504)

			ratioUp.SetLineColor(kRed)
			ratioDo.SetLineColor(kBlue)
			if o=="ChHad" or "CR" in o:
                                pad1.SetLogy(1)
			else:
				pad1.SetLogy(0)
				
			up.Draw("E0,hist")
			do.Draw("E0,hist,same")
			nominal.Draw("E0,hist,same")
			
			#errorband.Draw("same,E2")
			temp=nominal.Clone("temp")
			legend.Draw("same")
			for i in range(temp.GetNbinsX()):
				temp.SetBinError(i+1,0.)
  			CMS_lumi.channelText = _channelText      	
        		CMS_lumi.CMS_lumi(c2, 4, 11)

			pad2.cd()
                    	errorband.Divide(temp)
			ratioUp.Draw("hist")
			ratioDo.Draw("hist,same")
			oneline.Draw("same")
			#errorband.Draw("same")	
				
        		Quiet(c2.SaveAs)("Systematics_July/%s_%s_%s_%s%sratio.pdf"%(o,p,sys,finalState,dir_))
