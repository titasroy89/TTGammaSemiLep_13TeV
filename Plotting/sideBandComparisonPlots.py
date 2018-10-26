from ROOT import *
gROOT.SetBatch(True)
gStyle.SetOptStat(0)

import os
import CMS_lumi

from Style import *
thestyle = Style()
HasCMSStyle = False
style = None

if os.path.isfile('tdrstyle.C'):
    ROOT.gROOT.ProcessLine('.L tdrstyle.C')
    ROOT.setTDRStyle()
    print "Found tdrstyle.C file, using this style."
    HasCMSStyle = True
    if os.path.isfile('CMSTopStyle.cc'):
        gROOT.ProcessLine('.L CMSTopStyle.cc+')
        style = CMSTopStyle()
        style.setupICHEPv1()
        print "Found CMSTopStyle.cc file, use TOP style if requested in xml file."
if not HasCMSStyle:
    print "Using default style defined in cuy package."
    thestyle.SetStyle()

ROOT.gROOT.ForceStyle()

from optparse import OptionParser
parser = OptionParser()

parser.add_option("-c", "--channel", dest="channel", default="mu",type='string',
#                  choices=['ele','mu','Ele','Mu'],
		  help="Specify which channel mu or ele? default is mu" )

(options,args) = parser.parse_args()

channel = options.channel.lower()



_directory = "histograms/%s/hists_tight/"%channel

_sampleList = ["TTbar",
               "Diboson",
               "SingleTop",
               "TGJets",
               "TTGamma",
               "TTV",
               "WGamma",
               "WJets",
               "ZGamma",
               "ZJets",
	       "QCD_DD"]



#print _sampleList[1:]
#print _sampleList[:1]
#exit()

if channel=="mu":
    _fileData = TFile("%sDataMu.root","read")

    histData_barrel = _fileData.Get("phosel_AntiSIEIE_ChIso_barrel_DataMu")
    histData_barrel.SetDirectory(0)

    # histData_endcap = _fileData.Get("phosel_AntiSIEIE_ChIso_endcap_DataMu")
    # histData_endcap.SetDirectory(0)

if channel=="ele":
    _fileData = TFile("%sDataEle.root","read")

    histData_barrel = _fileData.Get("phosel_AntiSIEIE_ChIso_barrel_DataEle")
    histData_barrel.SetDirectory(0)

    # histData_endcap = _fileData.Get("phosel_AntiSIEIE_ChIso_endcap_DataEle")
    # histData_endcap.SetDirectory(0)


if channel=="both":
	 _fileData = TFile("histograms/mu/hists_tight/DataMu.root","read")
	 histData_barrel = _fileData.Get("phosel_AntiSIEIE_ChIso_barrel_DataMu")
	 _fileData2 = TFile("histograms/ele/hists_tight/DataEle.root","read")
	 histData_barrel.Add(_fileData2.Get("phosel_AntiSIEIE_ChIso_barrel_DataEle"))


_fileMC_ele = TFile("histograms/ele/hists_tight/TTbar.root","read")
_fileMC_mu = TFile("histograms/mu/hists_tight/TTbar.root","read")

histMC_barrel=_fileMC_ele.Get("phosel_noCut_ChIso_HadronicFake_barrel_TTbar").Clone("MC")

histMC_barrel.Add(_fileMC_ele.Get("phosel_noCut_ChIso_HadronicPhoton_barrel_TTbar"))
histMC_barrel.Add(_fileMC_mu.Get("phosel_noCut_ChIso_HadronicFake_barrel_TTbar"))
histMC_barrel.Add(_fileMC_mu.Get("phosel_noCut_ChIso_HadronicPhoton_barrel_TTbar"))

print histMC_barrel
#_sampleList.remove("QCD_DD")
for sample in _sampleList[1:]:

	print sample
	print histMC_barrel
		
	_file1 = TFile("histograms/ele/hists_tight/%s.root"%(sample),"read")
	_file2 = TFile("histograms/mu/hists_tight/%s.root"%(sample),"read")
	print histMC_barrel
	if sample=="QCD_DD":
		histMC_barrel.Add(_file1.Get("phosel_noCut_ChIso_barrel_%s"%sample))
		histMC_barrel.Add(_file2.Get("phosel_noCut_ChIso_barrel_%s"%sample))
	else:
	#print histMC_barrel
	#print ("phosel_noCut_ChIso_HadronicFake_barrel_%s"%sample), _fileMC_ele
		histMC_barrel.Add(_file1.Get("phosel_noCut_ChIso_HadronicFake_barrel_%s"%sample))
		histMC_barrel.Add(_file1.Get("phosel_noCut_ChIso_HadronicPhoton_barrel_%s"%sample))
		histMC_barrel.Add(_file2.Get("phosel_noCut_ChIso_HadronicFake_barrel_%s"%sample))
        	histMC_barrel.Add(_file2.Get("phosel_noCut_ChIso_HadronicPhoton_barrel_%s"%sample))

import array
xBins = array.array('d',[0,.1,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])

histMC_barrel=histMC_barrel.Rebin(len(xBins)-1,"",xBins)
histData_barrel=histData_barrel.Rebin(len(xBins)-1,"",xBins)
print histMC_barrel.Integral()
print histData_barrel.Integral()
histMC_barrel.SetFillColor(kGray)
histMC_barrel.SetLineColor(kGray)
histMC_barrel.SetMarkerSize(0)
histData_barrel.SetMarkerStyle(20)
histData_barrel.SetMarkerColor(kBlack)
histData_barrel.SetLineColor(kBlack)
leg = TLegend(0.45,0.7,0.85,0.85)
leg.SetBorderSize(0)
leg.SetFillColor(0)

leg.AddEntry(histData_barrel,"Data #sigma_{i#eta i#eta} sideband","p")
leg.AddEntry(histMC_barrel,"MC Nonprompt photons","f")

_channelText="e/#mu+jets"

CMS_lumi.channelText = _channelText
CMS_lumi.writeChannelText = True
CMS_lumi.writeExtraText = True


H = 600;
W = 800;


# references for T, B, L, R                                                                                                             
T = 0.08*H
B = 0.12*H
L = 0.12*W
R = 0.1*W

canvas = TCanvas('c1','c1',W,H)
canvas.SetFillColor(0)
canvas.SetBorderMode(0)
canvas.SetFrameFillStyle(0)
canvas.SetFrameBorderMode(0)
canvas.SetLeftMargin( L/W )
canvas.SetRightMargin( R/W )
canvas.SetTopMargin( T/H )
canvas.SetBottomMargin( B/H )
canvas.SetTickx(0)



frame = TH1F("frame","",10,0,20)
frame.SetTitle("Barrel photons")
frame.SetMaximum(0.11)
frame.GetXaxis().SetTitle("Photon charged-hadron isolation (GeV)")
frame.GetYaxis().SetTitle("Normalized events")

frame.Draw()
histMC_barrel.DrawNormalized('hist,same')
histData_barrel.DrawNormalized('e,same')
gPad.RedrawAxis()
leg.Draw("same")
CMS_lumi.CMS_lumi(canvas, 4, 11)
#canvas.SetLogy()
canvas.SaveAs("DataSideband_vs_MCnonprompt_barrel.pdf")



#canvas.SaveAs("trial.pdf")

exit()
sample = _sampleList[0]
print sample
_fileMC = TFile("%s/%s.root"%(_directory,sample),"read")
print _fileMC

histMC_barrel = _fileMC.Get("phosel_noCut_ChIso_HadronicFake_barrel_%s"%sample)
histMC_barrel.SetDirectory(0)

histMC_barrel.Add(_fileMC.Get("phosel_noCut_ChIso_HadronicPhoton_barrel_%s"%sample))

# histMC_endcap = _fileMC.Get("phosel_noCut_ChIso_HadronicFake_endcap_%s"%sample)
# histMC_endcap.SetDirectory(0)

# histMC_endcap.Add(_fileMC.Get("phosel_noCut_ChIso_HadronicPhoton_endcap_%s"%sample))


exit()

print "HERE"

print sample, "phosel_AntiSIEIE_SB1_ChIso_HadronicFake_barrel_%s"%sample
print _fileMC
histMC_SB1_barrel = _fileMC.Get("phosel_AntiSIEIE_SB1_ChIso_HadronicFake_barrel_%s"%sample)
histMC_SB1_barrel.SetDirectory(0)
histMC_SB1_barrel.Add(_fileMC.Get("phosel_AntiSIEIE_SB1_ChIso_HadronicPhoton_barrel_%s"%sample))

# histMC_SB1_endcap = _fileMC.Get("phosel_AntiSIEIE_SB1_ChIso_HadronicFake_endcap_%s"%sample)
# histMC_SB1_endcap.SetDirectory(0)
# histMC_SB1_endcap.Add(_fileMC.Get("phosel_AntiSIEIE_SB1_ChIso_HadronicPhoton_endcap_%s"%sample))



histMC_SB2_barrel = _fileMC.Get("phosel_AntiSIEIE_SB2_ChIso_HadronicFake_barrel_%s"%sample)
histMC_SB2_barrel.SetDirectory(0)
histMC_SB2_barrel.Add(_fileMC.Get("phosel_AntiSIEIE_SB2_ChIso_HadronicPhoton_barrel_%s"%sample))

# histMC_SB2_endcap = _fileMC.Get("phosel_AntiSIEIE_SB2_ChIso_HadronicFake_endcap_%s"%sample)
# histMC_SB2_endcap.SetDirectory(0)
# histMC_SB2_endcap.Add(_fileMC.Get("phosel_AntiSIEIE_SB2_ChIso_HadronicPhoton_endcap_%s"%sample))


histMC_SB_barrel = histMC_SB1_barrel.Clone("histMC_SB_barrel")
histMC_SB_barrel.Add(histMC_SB2_barrel)
histMC_SB_barrel.SetDirectory(0)

# histMC_SB_endcap = histMC_SB1_endcap.Clone("histMC_SB_endcap")
# histMC_SB_endcap.Add(histMC_SB2_endcap)
# histMC_SB_endcap.SetDirectory(0)


for sample in _sampleList[1:]:
    print sample
    _fileMC = TFile("%s%s.root"%(_directory,sample),"read")
    histMC_barrel.Add(_fileMC.Get("phosel_noCut_ChIso_HadronicFake_barrel_%s"%sample))
    histMC_barrel.Add(_fileMC.Get("phosel_noCut_ChIso_HadronicPhoton_barrel_%s"%sample))

    # histMC_endcap.Add(_fileMC.Get("phosel_noCut_ChIso_HadronicFake_endcap_%s"%sample))
    # histMC_endcap.Add(_fileMC.Get("phosel_noCut_ChIso_HadronicPhoton_endcap_%s"%sample))

    histMC_SB1_barrel.Add(_fileMC.Get("phosel_AntiSIEIE_SB1_ChIso_HadronicFake_barrel_%s"%sample))
    histMC_SB1_barrel.Add(_fileMC.Get("phosel_AntiSIEIE_SB1_ChIso_HadronicPhoton_barrel_%s"%sample))
    # histMC_SB1_endcap.Add(_fileMC.Get("phosel_AntiSIEIE_SB1_ChIso_HadronicFake_endcap_%s"%sample))
    # histMC_SB1_endcap.Add(_fileMC.Get("phosel_AntiSIEIE_SB1_ChIso_HadronicPhoton_endcap_%s"%sample))

    histMC_SB2_barrel.Add(_fileMC.Get("phosel_AntiSIEIE_SB2_ChIso_HadronicFake_barrel_%s"%sample))
    histMC_SB2_barrel.Add(_fileMC.Get("phosel_AntiSIEIE_SB2_ChIso_HadronicPhoton_barrel_%s"%sample))
    # histMC_SB2_endcap.Add(_fileMC.Get("phosel_AntiSIEIE_SB2_ChIso_HadronicFake_endcap_%s"%sample))
    # histMC_SB2_endcap.Add(_fileMC.Get("phosel_AntiSIEIE_SB2_ChIso_HadronicPhoton_endcap_%s"%sample))


histMC_barrel.SetFillColor(kGray)
histMC_barrel.SetLineColor(kGray)
histMC_barrel.SetMarkerSize(0)

histData_barrel.SetMarkerStyle(20)
histData_barrel.SetMarkerColor(kBlack)
histData_barrel.SetLineColor(kBlack)

# histMC_endcap.SetFillColor(kGray)
# histMC_endcap.SetLineColor(kGray)
# histMC_endcap.SetMarkerSize(0)

# histData_endcap.SetMarkerStyle(20)
# histData_endcap.SetMarkerColor(kBlack)
# histData_endcap.SetLineColor(kBlack)


import array
xBins = array.array('d',[0,.1,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])

histMC_barrel    = histMC_barrel.Rebin(21,"",xBins)
histMC_SB_barrel = histMC_SB_barrel.Rebin(21,"",xBins)
histMC_SB1_barrel = histMC_SB1_barrel.Rebin(21,"",xBins)
histMC_SB2_barrel = histMC_SB2_barrel.Rebin(21,"",xBins)
histData_barrel  = histData_barrel.Rebin(21,"",xBins)
# histMC_endcap    = histMC_endcap.Rebin(21,"",xBins)
# histMC_SB_endcap = histMC_SB_endcap.Rebin(21,"",xBins)
# histMC_SB1_endcap = histMC_SB1_endcap.Rebin(21,"",xBins)
# histMC_SB2_endcap = histMC_SB2_endcap.Rebin(21,"",xBins)
# histData_endcap  = histData_endcap.Rebin(21,"",xBins)

leg = TLegend(0.45,0.7,0.85,0.85)
leg.SetBorderSize(0)
leg.SetFillColor(0)

leg.AddEntry(histData_barrel,"Data #sigma_{#eta#eta} sideband","p")
leg.AddEntry(histMC_barrel,"MC Nonprompt photons","f")


if channel=="mu":
	_channelText = "#mu+jets, #geq4j#geq1b"
elif channel=="ele":
        _channelText = "e+jets, #geq4j#geq1b"

CMS_lumi.channelText = _channelText
CMS_lumi.writeChannelText = True
CMS_lumi.writeExtraText = True


H = 600;
W = 800;


# references for T, B, L, R                                                                                                             
T = 0.08*H
B = 0.12*H
L = 0.12*W
R = 0.1*W

canvas = TCanvas('c1','c1',W,H)
canvas.SetFillColor(0)
canvas.SetBorderMode(0)
canvas.SetFrameFillStyle(0)
canvas.SetFrameBorderMode(0)
canvas.SetLeftMargin( L/W )
canvas.SetRightMargin( R/W )
canvas.SetTopMargin( T/H )
canvas.SetBottomMargin( B/H )
canvas.SetTickx(0)



frame = TH1F("frame","",10,0,20)
frame.SetTitle("Barrel photons")
frame.SetMaximum(0.11)
frame.GetXaxis().SetTitle("Photon charged-hadron isolation (GeV)")
frame.GetYaxis().SetTitle("Normalized events")

frame.Draw()
histMC_barrel.DrawNormalized('hist,same')
histData_barrel.DrawNormalized('e,same')
gPad.RedrawAxis()
leg.Draw("same")
CMS_lumi.CMS_lumi(canvas, 4, 11)

canvas.SaveAs("plots_%s/DataSideband_vs_MCnonprompt_barrel.pdf"%channel)


# frame.SetTitle("Endcap photons")
# frame.Draw()
# histMC_endcap.DrawNormalized('HIST,same')
# histData_endcap.DrawNormalized('e,same')
# leg.Draw("same")

# CMS_lumi.CMS_lumi(canvas, 4, 11)

# canvas.SaveAs("plots_%s/DataSideband_vs_MCnonprompt_endcap.pdf"%channel)


histMC_barrel.SetLineColor(kBlue)
histMC_SB_barrel.SetLineColor(kRed)
histMC_SB1_barrel.SetLineColor(kBlue)
histMC_SB2_barrel.SetLineColor(kRed)

histMC_barrel.SetMarkerColor(kBlue)
histMC_SB_barrel.SetMarkerColor(kRed)
histMC_SB1_barrel.SetMarkerColor(kBlue)
histMC_SB2_barrel.SetMarkerColor(kRed)

histMC_barrel.SetLineWidth(2)
histMC_SB_barrel.SetLineWidth(2)
histMC_SB1_barrel.SetLineWidth(2)
histMC_SB2_barrel.SetLineWidth(2)

histMC_barrel.SetMarkerStyle(20)
histMC_SB_barrel.SetMarkerStyle(20)
histMC_SB1_barrel.SetMarkerStyle(20)
histMC_SB2_barrel.SetMarkerStyle(20)

histMC_barrel.SetMarkerSize(1.)


# histMC_endcap.SetLineColor(kBlack)
# histMC_SB1_endcap.SetLineColor(kBlue)
# histMC_SB2_endcap.SetLineColor(kRed)

# histMC_endcap.SetMarkerColor(kBlack)
# histMC_SB1_endcap.SetMarkerColor(kBlue)
# histMC_SB2_endcap.SetMarkerColor(kRed)

# histMC_endcap.SetLineWidth(2)
# histMC_SB1_endcap.SetLineWidth(2)
# histMC_SB2_endcap.SetLineWidth(2)

# histMC_endcap.SetMarkerStyle(20)
# histMC_SB1_endcap.SetMarkerStyle(20)
# histMC_SB2_endcap.SetMarkerStyle(20)

# histMC_endcap.SetMarkerSize(1.)

leg = TLegend(0.4,0.7,0.85,0.89)
leg.SetBorderSize(0)
leg.SetFillColor(0)

leg.AddEntry(histData_barrel,"Data 0.011 < #sigma_{#eta#eta}<0.02","p")
leg.AddEntry(histMC_barrel,"Nonprompt MC #sigma_{#eta#eta}<0.0102",'lp')
leg.AddEntry(histMC_SB_barrel,"Nonprompt MC 0.011 < #sigma_{#eta#eta}<0.02",'lp')
# leg.AddEntry(histMC_SB1_barrel,"0.011 < #sigma_{#eta#eta}<0.015",'lp')
# leg.AddEntry(histMC_SB2_barrel,"0.015 < #sigma_{#eta#eta}<0.02",'lp')

frame.SetTitle("")
frame.Draw()
histMC_SB_barrel.DrawNormalized("e,same")
histMC_barrel.DrawNormalized("e,same")
histData_barrel.DrawNormalized("e,same")
leg.Draw("same")

CMS_lumi.extraText = "Simulation"

CMS_lumi.CMS_lumi(canvas, 4, 11)

canvas.SaveAs("plots_%s/DataMCnonprompt_SignalRegion_Sideband_Comparison_barrel.pdf"%channel)

leg.Clear()

leg = TLegend(0.4,0.7,0.85,0.89)
leg.SetBorderSize(0)
leg.SetFillColor(0)

#leg.AddEntry(histData_barrel,"Data 0.011 < #sigma_{#eta#eta}<0.02","p")
leg.AddEntry(histMC_barrel,"Nonprompt MC #sigma_{#eta#eta}<0.0102",'lp')
leg.AddEntry(histMC_SB_barrel,"Nonprompt MC 0.011 < #sigma_{#eta#eta}<0.02",'lp')
# leg.AddEntry(histMC_SB1_barrel,"0.011 < #sigma_{#eta#eta}<0.015",'lp')
# leg.AddEntry(histMC_SB2_barrel,"0.015 < #sigma_{#eta#eta}<0.02",'lp')

frame.SetTitle("")
frame.Draw()
histMC_SB_barrel.DrawNormalized("e,same")
histMC_barrel.DrawNormalized("e,same")
#histData_barrel.DrawNormalized("e,same")
leg.Draw("same")

CMS_lumi.extraText = "Simulation"

CMS_lumi.CMS_lumi(canvas, 4, 11)

canvas.SaveAs("plots_%s/MCnonprompt_SignalRegion_Sideband_Comparison_barrel.pdf"%channel)





# leg.AddEntry(histMC_endcap,"#sigma_{#eta#eta}<0.03001",'lp')
# leg.AddEntry(histMC_SB1_endcap,"0.03001 < #sigma_{#eta#eta}<0.035",'lp')
# leg.AddEntry(histMC_SB2_endcap,"0.035 < #sigma_{#eta#eta}<0.04",'lp')

# frame.Draw()
# histMC_SB2_endcap.DrawNormalized("e,same")
# histMC_SB1_endcap.DrawNormalized("e,same")
# histMC_endcap.DrawNormalized("e,same")
# leg.Draw("same")
# canvas.SaveAs("plots_%s/MCnonprompt_SignalRegion_Sideband_Comparison_endcap.pdf"%channel)
