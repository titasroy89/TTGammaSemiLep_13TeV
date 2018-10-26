## Make root files for combine with different MC signals and their systematics###
##uncertainties in both electron and muon channel####

from ROOT import *
import math
import os
import sys
from array import array
import CMS_lumi

from Style import *
thestyle = Style()
random=TRandom3(0)

_file = {}
from optparse import OptionParser


parser = OptionParser()

parser.add_option("-c", "--channel", dest="channel", default="mu",type='str',
                  help="Specify which channel mu or ele? default is mu" )
parser.add_option("--Tight","--tight", dest="isTightSelection", default=False,action="store_true",
                     help="Use 4j2t selection" )

(options, args) = parser.parse_args()


finalState = options.channel
TightSelection = options.isTightSelection

samples =["TTGamma","TTbar","TTV","TGJets","SingleTop","WJets","ZJets","WGamma","ZGamma","Diboson"]
if finalState=="mu":
	samples.append("DataMu")
else:
	samples.append("DataEle")

if TightSelection:
	for s in samples:
        	_file[s] = TFile("/uscms_data/d3/troy2012/CMSSW_8_0_26_patch1/src/TTGammaSemiLep_13TeV/Plotting/histograms/%s/hists_tight/%s.root"%(finalState,s))
else:
	for s in samples:
		print s
                _file[s] = TFile("/uscms_data/d3/troy2012/CMSSW_8_0_26_patch1/src/TTGammaSemiLep_13TeV/Plotting/histograms/%s/hists/%s.root"%(finalState,s))

#exit()
misIDEleSF = 1.
HistDict={}






binsChHad = [0.,0.1,1.,2.,3.,4.,5.,6.,7.,8.,9.,10.,11.,12.,13.,14.,15.,16.,17.,18.,19.,20.]

observables={"ChHad":["noCut_ChIso",binsChHad],
             "AntiSIEIE":["AntiSIEIE_ChIso",binsChHad],
	    }

#print sorted(observables.keys())[:2]


process_signal = {"TTGamma_Prompt":["TTGamma"],
	   "TTGamma_NonPrompt":["TTGamma"],
           "TTbar_Prompt": ["TTbar"],
           "TTbar_NonPrompt": ["TTbar"],
           "VGamma_Prompt":["ZGamma","WGamma"],
           "VGamma_NonPrompt":["ZGamma","WGamma"],
           "VJets_Prompt":["ZJets", "WJets"],
           "VJets_NonPrompt":["ZJets", "WJets"],
           "Other_Prompt":["TTV", "Diboson", "TGJets", "SingleTop"],
           "Other_NonPrompt":["TTV", "Diboson","TGJets", "SingleTop"],
	}



process_control ={"TTGamma":["TTGamma"],
		  "TTbar":  ["TTbar"],
		  "VGamma":["ZGamma", "WGamma"],
		  "VJets":["WJets", "ZJets"],
		  "Other":[ "TTV", "Diboson","TGJets", "SingleTop"],
		}	





##### Make Prompt and NonPrompt MC templates#######
process={}
for obs in observables:
	HistDict[obs]={}
	
	
		

	for p in process_signal:
			
		 s = process_signal[p][0]
		 if "NonPrompt" in p:
				 print _file[s]
				 print "phosel_%s_HadronicPhoton_barrel_%s"%(observables[obs][0],s)
				 HistDict[obs][p]   = _file[s].Get("phosel_%s_HadronicPhoton_barrel_%s"%(observables[obs][0],s)).Clone("%s_%s"%(obs,p))
				 HistDict[obs][p].Add(_file[s].Get("phosel_%s_HadronicFake_barrel_%s"%(observables[obs][0],s)))
				

		 if "_Prompt" in p:
				print "phosel_%s_GenuinePhoton_barrel_%s"%(observables[obs][0],s)
			 	HistDict[obs][p]   = _file[s].Get("phosel_%s_GenuinePhoton_barrel_%s"%(observables[obs][0],s)).Clone("%s_%s"%(obs,p))
			 	HistDict[obs][p].Add(_file[s].Get("phosel_%s_MisIDEle_barrel_%s"%(observables[obs][0],s)))
									
				
		 for s in process_signal[p][1:]:
				if "_Prompt" in p:
					if (finalState=="mu") and ("VJets" in p):continue	
					HistDict[obs][p].Add(_file[s].Get("phosel_%s_GenuinePhoton_barrel_%s"%(observables[obs][0],s)))
					HistDict[obs][p].Add(_file[s].Get("phosel_%s_MisIDEle_barrel_%s"%(observables[obs][0],s)))
					
				if "_NonPrompt" in p:
					HistDict[obs][p].Add(_file[s].Get("phosel_%s_HadronicPhoton_barrel_%s"%(observables[obs][0],s)))
                                        HistDict[obs][p].Add(_file[s].Get("phosel_%s_HadronicFake_barrel_%s"%(observables[obs][0],s)))


			
		 HistDict[obs][p]= HistDict[obs][p].Rebin(21,"",array('d',binsChHad))



if finalState=="ele":
	h1 = _file["DataEle"].Get("phosel_AntiSIEIE_ChIso_barrel_DataEle").Clone("ChHad_NonPrompt")
else:
	h1 = _file["DataMu"].Get("phosel_AntiSIEIE_ChIso_barrel_DataMu").Clone("ChHad_NonPrompt")
h1 = h1.Rebin(21,"",array('d',binsChHad))

total = h1.Integral(-1,-1)
NormFactor={}



for p in process_signal:
	NormFactor[p]={}
	if "_NonPrompt" in p:
		p1=p.strip("NonPrompt")
		p1= p1.strip("_")
		if finalState=="ele":
			HistDict["ChHad"]["%s_DD"%p1] = _file["DataEle"].Get("phosel_AntiSIEIE_ChIso_barrel_DataEle").Clone("ChHad_NonPrompt")
		else:
			HistDict["ChHad"]["%s_DD"%p1] = _file["DataMu"].Get("phosel_AntiSIEIE_ChIso_barrel_DataMu").Clone("ChHad_NonPrompt")
		HistDict["ChHad"]["%s_DD"%p1]=HistDict["ChHad"]["%s_DD"%p1].Rebin(21,"",array('d',binsChHad))
		NormFactor["%s_DD"%p1]=HistDict["ChHad"][p].Integral(-1,-1)
		HistDict["ChHad"]["%s_DD"%p1].Scale(NormFactor["%s_DD"%p1]/total)




		
		
	




###We need MC NonPrompt templates in fit region for shape uncertainty on DataDriven templates
c1 = TCanvas('c1','c1',1000,1000)
c1.SetFillColor(0)
c1.SetBorderMode(0)
c1.SetFrameFillStyle(0)

HistDict["AntiSIEIE"]["TTbar_NonPrompt"].SetLineColor(kRed)
HistDict["ChHad"]["TTbar_NonPrompt"].SetLineColor(kBlue)
HistDict["ChHad"]["TTbar_NonPrompt"].DrawNormalized("hist")
HistDict["AntiSIEIE"]["TTbar_NonPrompt"].DrawNormalized("hist,same")
c1.SaveAs("ttbar_diff_1.pdf")

c1.Clear()



nbins = HistDict["ChHad"]["TTGamma_NonPrompt"].GetNbinsX()

if nbins != HistDict["AntiSIEIE"]["TTGamma_NonPrompt"].GetNbinsX():
	print "binsChHad not equal in two regions !! abort !!"
	exit()
diff=0.

#HistDict["AntiSIEIE"]["TTbar_NonPrompt"].Scale(1/HistDict["AntiSIEIE"]["TTbar_NonPrompt"].Integral(-1,-1))
#HistDict["ChHad"]["TTbar_NonPrompt"].Scale(1/HistDict["ChHad"]["TTbar_NonPrompt"].Integral(-1,-1))
unc_=[]
#for p in process_control:
	
	
#	if p=="TTbar":continue
#	print "%s_NonPrompt"%p
#	HistDict["AntiSIEIE"]["TTbar_NonPrompt"].Add(HistDict["AntiSIEIE"]["%s_NonPrompt"%p].Scale(1/HistDict["AntiSIEIE"]["%s_NonPrompt"%p].Integral(-1,-1)))
#	HistDict["ChHad"]["TTbar_NonPrompt"].Add(HistDict["ChHad"]["%s_NonPrompt"%p].Scale(1/HistDict["ChHad"]["%s_NonPrompt"%p].Integral(-1,-1)))
#	HistDict["AntiSIEIE"]["%s_NonPrompt"%p].Scale(1/HistDict["AntiSIEIE"]["%s_NonPrompt"%p].Integral())
#	HistDict["ChHad"]["%s_NonPrompt"%p].Scale(1/HistDict["ChHad"]["%s_NonPrompt"%p].Integral())


for p in process_control:


       if p=="TTbar":continue
#       print "%s_NonPrompt"%p
       HistDict["AntiSIEIE"]["TTbar_NonPrompt"].Add(HistDict["AntiSIEIE"]["%s_NonPrompt"%p])
       HistDict["ChHad"]["TTbar_NonPrompt"].Add(HistDict["ChHad"]["%s_NonPrompt"%p])

HistDict["AntiSIEIE"]["TTbar_NonPrompt"].Scale(1/HistDict["AntiSIEIE"]["TTbar_NonPrompt"].Integral())
HistDict["ChHad"]["TTbar_NonPrompt"].Scale(1/HistDict["ChHad"]["TTbar_NonPrompt"].Integral())

gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)
c1 = TCanvas('c1','c1',1000,1000)
c1.SetFillColor(0)
c1.SetBorderMode(0)
c1.SetFrameFillStyle(0)
legend= TLegend(0.55, 0.69,0.89,0.89)
legend.SetBorderSize(0);
legend.SetFillStyle(0);

HistDict["AntiSIEIE"]["TTbar_NonPrompt"].SetLineColor(kRed)
legend.AddEntry(HistDict["AntiSIEIE"]["TTbar_NonPrompt"], "Sideband NonPrompt MC",'lp')
HistDict["ChHad"]["TTbar_NonPrompt"].SetLineColor(kBlue)
legend.AddEntry(HistDict["ChHad"]["TTbar_NonPrompt"], "FitRegion NonPrompt MC",'lp')
HistDict["ChHad"]["TTbar_NonPrompt"].Draw("hist")
HistDict["AntiSIEIE"]["TTbar_NonPrompt"].Draw("hist,same")
legend.Draw("same")
c1.SaveAs("NonPromptvsPrompt_diff_2.pdf")

c1.Clear()






exit()


for bin_ in range(nbins):
       	    
	diff=HistDict["ChHad"]["TTbar_NonPrompt"].GetBinContent(bin_+1)-HistDict["AntiSIEIE"]["TTbar_NonPrompt"].GetBinContent(bin_+1)
       # print bin_, HistDict["ChHad"]["TTbar_NonPrompt"].GetBinContent(bin_+1), HistDict["AntiSIEIE"]["TTbar_NonPrompt"].GetBinContent(bin_+1), diff,HistDict["AntiSIEIE"]["TTbar_NonPrompt"].GetBinContent(bin_+1)          
	unc_.append(diff/HistDict["AntiSIEIE"]["TTbar_NonPrompt"].GetBinContent(bin_+1)) 
		 



HistDict_up={}
HistDict_up["ChHad"]={}
HistDict_do={}
HistDict_do["ChHad"]={}
for p in process_control:

        HistDict_up["ChHad"]["%s_DD"%p] ={}
        HistDict_do["ChHad"]["%s_DD"%p] ={}
        HistDict_up["ChHad"]["%s_DD"%p]["shapeDD"] = TH1F("%s_shapeDD"%p,"%s_shapeDD"%p,21,0,20)
        HistDict_up["ChHad"]["%s_DD"%p]["shapeDD"] = HistDict_up["ChHad"]["%s_DD"%p]["shapeDD"].Rebin(21,"",array('d',binsChHad))

        HistDict_do["ChHad"]["%s_DD"%p]["shapeDD"] = TH1F("%s_shapeDD"%p,"%s_shapeDD"%p,21,0,20)
        HistDict_do["ChHad"]["%s_DD"%p]["shapeDD"] = HistDict_do["ChHad"]["%s_DD"%p]["shapeDD"].Rebin(21,"",array('d',binsChHad))
        for bin_ in range(nbins):

                orig_=HistDict["ChHad"]["%s_DD"%p].GetBinContent(bin_+1)
                up = orig_+orig_*unc_[bin_]
                do = orig_-orig_*unc_[bin_]
           
                print p, orig_,unc_[bin_], orig_+orig_*unc_[bin_], orig_-orig_*unc_[bin_]
                HistDict_up["ChHad"]["%s_DD"%p]["shapeDD"].SetBinContent(bin_+1,up)
                HistDict_do["ChHad"]["%s_DD"%p]["shapeDD"].SetBinContent(bin_+1,do)

	
	





c1 = TCanvas('c1','c1',1000,1000)
c1.SetFillColor(0)
c1.SetBorderMode(0)
c1.SetFrameFillStyle(0)

HistDict["AntiSIEIE"]["TTbar_NonPrompt"].SetLineColor(kRed)
HistDict["ChHad"]["TTbar_NonPrompt"].SetLineColor(kBlue)
HistDict["ChHad"]["TTbar_NonPrompt"].Draw("hist")
HistDict["AntiSIEIE"]["TTbar_NonPrompt"].Draw("hist,same")
c1.SaveAs("ttbar_diff.pdf")

c1.Clear()
HistDict_up["ChHad"]["TTbar_DD"]["shapeDD"].SetLineColor(kRed)
HistDict_up["ChHad"]["TTbar_DD"]["shapeDD"].Draw("hist")
HistDict["ChHad"]["TTbar_DD"].SetLineColor(kBlack)

HistDict_do["ChHad"]["TTbar_DD"]["shapeDD"].SetLineColor(kBlue)
HistDict["ChHad"]["TTbar_DD"].Draw("hist,same")
HistDict_do["ChHad"]["TTbar_DD"]["shapeDD"].Draw("hist,same")

c1.SaveAs("TTbar_shape.pdf")
