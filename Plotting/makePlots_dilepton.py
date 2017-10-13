from ROOT import *
import os

import sys


padRatio = 0.25
padOverlap = 0.15
padGap = 0.01

_file  = TFile("histograms_dilep/dimu/hists.root")
plotDirectory = "plots_dilep/"
regionText = ", N_{j}#geq3, N_{b}#geq1"

isTight = False

if 'Tight' in sys.argv:
    plotDirectory = "tightplots_dilep/"        
    _file  = TFile("histograms_dilep/dimu/hists_tight.root")
    regionText = ", N_{j}#geq4, N_{b}#geq2"
if 'Loose' in sys.argv:
    plotDirectory = "looseplots_CSVv2/"
    _file  = TFile("histograms_CSV/mu/hists_loose.root")
    regionText = ", N_{j}#geq3, N_{b}#geq1"
if 'LooseCR' in sys.argv:
    plotDirectory = "2j1tCRplots_dilep/"
    _file  = TFile("histograms_dilep/mu/hists_2jControlRegion.root")
    regionText = ", N_{j}=2, N_{b}#geq1"

if 'TightCR' in sys.argv:
    plotDirectory = "tightplotsCR/"
    _file  = TFile("histograms/mu/hists_tightCR.root")
    regionText = ", N_{j}#geq3, N_{b}#geq2"

if "VeryLoose" in sys.argv:
    plotDirectory = "verylooseCR/"
    _file  = TFile("histograms_dilep/dimu/hists_2j0tag.root")
    regionText = ", N_{j}=2, N_{b}#geq0"

from sampleInformation import *

gROOT.SetBatch(True)




YesLog = True
NoLog=False




# Histogram Information:
# [X-axis title, 
#  Y-axis title,
#  Rebinning factor,
#  [x-min,x-max], -1 means keep as is
#  Extra text about region
#  log plot]


preselhistograms = {"jet1Pt"   : ["Leading Jet Pt (GeV)", "Events", 5, [-1,-1], regionText, YesLog],
                    "jet2Pt"   : ["Second Jet Pt (GeV)" , "Events", 5, [-1,-1], regionText, YesLog],
                    "jet3Pt"   : ["Third Jet Pt (GeV)"  , "Events", 5, [-1,-1], regionText, YesLog],
                    "muPt"     : ["Muon p_{T} (GeV)"    , "Events", 5, [-1,-1], regionText,  NoLog],
                    "muEta"    : ["Muon #eta"           , "Events", 5, [-1,-1], regionText,  NoLog],
                    "muPhi"    : ["Muon #phi"           , "Events", 5, [-1,-1], regionText,  NoLog],
                    "Njet"     : ["N Jets"              , "Events", 1, [-1,-1], regionText,  NoLog],
                    "Nbjet"    : ["N B-Jets"            , "Events", 1, [-1,-1], regionText,  NoLog],
                    "M3"       : ["M_{3} (GeV)"         , "Events", 5, [-1,-1], regionText,  NoLog],
                    "MET"      : ["MET (GeV)  "         , "Events", 5, [-1,-1], regionText,  NoLog],
                    "DilepMass": ["Dilepton Mass"              , "Events", 1, [-1,-1], regionText,  NoLog],
                    "DilepDelR": ["Delta R between two leptons", "Events", 1, [-1,-1], regionText,  NoLog],
                    "nVtx"     : ["N Vtx"               , "Events", 1, [-1,-1], regionText,  NoLog],
		    "WtransMass": ["W transverse mass" , "Events", 1, [-1,-1], regionText,  NoLog],
                    # "nVtxup"   : ["N Vtx"               , "Events", 1, [-1,-1], regionText,  NoLog],
                    # "nVtxdo"   : ["N Vtx"               , "Events", 1, [-1,-1], regionText,  NoLog],
                    # "nVtxNoPU" : ["N Vtx"               , "Events", 1, [-1,-1], regionText,  NoLog],
                    }



phoselhistograms = {"photonEt"                : ["Photon Et (GeV)"            , "Events", 5, [-1,-1], regionText,  NoLog],     
                    "photonPhi"               : ["Photon Phi (GeV)"           , "Events", 1, [-1,-1], regionText,  NoLog],    
                    "photonEta"               : ["Photon Eta (GeV)"           , "Events", 1, [-1,-1], regionText,  NoLog],    
                    "dRPhotonLepton"          : ["dR(Photon,Lepton)"          , "Events", 1, [-1,-1], regionText,  NoLog],
                    "dRPhotonJet"             : ["dR(Photon,Jet)"             , "Events", 1, [-1,-1], regionText,  NoLog],   
                    "M3"                      : ["M_{3} (GeV)"                , "Events", 5, [-1,-1], regionText,  NoLog],   
		    "DilepMass"		      : ["Dilepton Mass"              , "Events", 1, [-1,-1], regionText,  NoLog],
		    "DilepDelR"               : ["Delta R between two leptons", "Events", 1, [-1,-1], regionText,  NoLog],
		    "WtransMass"              : ["W transverse mass"          ,  "Events",1, [-1,-1], regionText,  NoLog],
                    "Njet"                    : ["N Jets"                     , "Events", 1, [-1,-1], regionText,  NoLog],
                    "Nbjet"                   : ["N B-Jets"                   , "Events", 1, [-1,-1], regionText,  NoLog],
                    "HoverE"                  : ["H over E"                   , "Events", 1, [-1,-1], regionText, YesLog],
                    "SIEIE"                   : ["Sigma Ieta Ieta"            , "Events", 1, [-1,-1], regionText, YesLog],
                    "ChIso"                   : ["Charged Hadron Iso (GeV)"   , "Events", 1, [-1,-1], regionText, YesLog],
                    "NeuIso"                  : ["Neutral Hadron Iso (GeV)"   , "Events", 1, [-1,-1], regionText, YesLog],
                    "PhoIso"                  : ["Photon Iso (GeV)"           , "Events", 1, [-1,-1], regionText, YesLog],
                    "noCut_HoverE"            : ["H over E"                   , "Events", 1, [-1,-1], regionText, YesLog],
                    "noCut_SIEIE"             : ["Sigma Ieta Ieta"            , "Events", 1, [-1,-1], regionText, YesLog],
                    "noCut_ChIso"             : ["Charged Hadron Iso (GeV)"   , "Events", 1, [-1,-1], regionText, YesLog],
                    "noCut_NeuIso"            : ["Neutral Hadron Iso (GeV)"   , "Events", 1, [-1,-1], regionText, YesLog],
                    "noCut_PhoIso"            : ["Photon Iso (GeV)"           , "Events", 1, [-1,-1], regionText, YesLog],
                    "AntiSIEIE_ChIso"         : ["Charged Hadron Iso (GeV)"   , "Events", 1, [-1,-1], regionText, YesLog],
                   # "AntiHoverE_ChIso"        : ["Charged Hadron Iso (GeV)"   , "Events", 1, [-1,-1], regionText,  NoLog],
                   # "AntiHoverEOrSIEIE_ChIso" : ["Charged Hadron Iso (GeV)"   , "Events", 1, [-1,-1], regionText,  NoLog],
                    }



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

sampleList[-2] = "QCDMu"
stackList = sampleList[:-1]

stackList.remove("QCDMu")
stackList.reverse()


_channelText = "#mu+jets"

CMS_lumi.channelText = _channelText
CMS_lumi.writeChannelText = True
CMS_lumi.writeExtraText = True


H = 600;
W = 800;

canvas = TCanvas('c1','c1',W,H)

# references for T, B, L, R                                                                                                             
T = 0.08*H
B = 0.12*H
L = 0.12*W
R = 0.04*W
canvas.SetFillColor(0)
canvas.SetBorderMode(0)
canvas.SetFrameFillStyle(0)
canvas.SetFrameBorderMode(0)
canvas.SetLeftMargin( L/W )
canvas.SetRightMargin( R/W )
canvas.SetTopMargin( T/H )
canvas.SetBottomMargin( B/H )
canvas.SetTickx(0)


canvasRatio = TCanvas('c1Ratio','c1Ratio',W,H)
# references for T, B, L, R                                                                                                             
T = 0.08*H
B = 0.12*H
L = 0.12*W
R = 0.04*W
canvasRatio.SetFillColor(0)
canvasRatio.SetBorderMode(0)
canvasRatio.SetFrameFillStyle(0)
canvasRatio.SetFrameBorderMode(0)
canvasRatio.SetLeftMargin( L/W )
canvasRatio.SetRightMargin( R/W )
canvasRatio.SetTopMargin( T/H )
canvasRatio.SetBottomMargin( B/H )
canvasRatio.SetTickx(0)
canvasRatio.SetTicky(0)
pad1 = TPad("p1","p1",0,padRatio-padOverlap,1,1)
pad2 = TPad("p2","p2",0,0,1,padRatio+padOverlap)
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

SetOwnership(canvas, False)
SetOwnership(canvasRatio, False)
SetOwnership(pad1, False)
SetOwnership(pad2, False)

canvasRatio.cd()
pad1.Draw()
pad2.Draw()


canvas.cd()

legList = {'TTGamma': [kAzure+3, 't#bar{t}+#gamma'],
          'TTJets': [kRed+1, 't#bar{t}+jets'],
          'TTV': [kRed+1, 't#bar{t}+V'],
          'Vgamma': [kGray, 'W/Z+#gamma'],
          'SingleTop': [kMagenta, 'Single t'],
          'WJets': [kGreen -3, 'W+jets'],
          'ZJets': [kGreen -3, 'Z+jets'],}
#          'QCDMu': [kYellow, 'Multijet'],
         # }

mcList = {'TTGamma': [kOrange],
          'TTbar': [kRed+1],
          'TTV': [kRed-7],
          'SingleTop': [kOrange-3],
          'WGamma': [kBlue-4],
          'ZGamma': [kBlue-2],
          'WJets': [kCyan-3],
          'ZJets': [kCyan-5],
    #      'QCDMu': [kGreen+3],
          }


legendHeightPer = 0.04

legend = TLegend(0.71, 1-T/H-0.01 - legendHeightPer*(len(legList)+1), 1-R/W-0.01, 1-(T/H)-0.01)

legendR = TLegend(0.71, 0.99 - (T/H)/(1.-padRatio+padOverlap) - legendHeightPer/(1.-padRatio+padOverlap)*(len(legList)+1), 0.99-(R/W), 0.99-(T/H)/(1.-padRatio+padOverlap))
legendR.SetBorderSize(0)
legendR.SetFillColor(0)



legend.SetBorderSize(0)
legend.SetFillColor(0)

histName = preselhistograms.keys()[0]
legList = stackList[:]
legList.reverse()
#print legList
#print histName
dataHist = _file.Get("DataMu/presel_%s_DataMu"%(histName))
legend.AddEntry(dataHist, "Data", 'pe')
legendR.AddEntry(dataHist, "Data", 'pe')

for sample in legList:
 #   print sample, histName
    hist = _file.Get("%s/presel_%s_%s"%(sample,histName,sample))
    hist.SetFillColor(mcList[sample][0])
    hist.SetLineColor(mcList[sample][0])
    legend.AddEntry(hist,sample,'f')
    legendR.AddEntry(hist,sample,'f')


TGaxis.SetMaxDigits(3)

def drawHist(histName,plotInfo, plotDirectory, _file):

    canvas.cd()
    canvas.ResetDrawn()
    stack = THStack(histName,histName)
    for sample in stackList:
        print sample, histName
        hist = _file.Get("%s/%s_%s"%(sample,histName,sample)).Clone(sample)
        hist.SetFillColor(mcList[sample][0])
        hist.SetLineColor(mcList[sample][0])
        hist.Rebin(plotInfo[2])
        stack.Add(hist)

    dataHist = _file.Get("DataMu/%s_DataMu"%(histName))
    dataHist.Rebin(plotInfo[2])


    #histograms list has flag whether it's log or not
    canvas.SetLogy(plotInfo[-1])
    canvas.SetLogx(plotInfo[-1])

    stack.SetMaximum(1.35*max(dataHist.GetMaximum(),stack.GetMaximum()))
    stack.Draw("hist")
    # histograms list has x-axis title
    stack.GetHistogram().GetXaxis().SetTitle(plotInfo[0])
    if not -1 in plotInfo[3]:
        stack.GetHistogram().GetXaxis().SetRangeUser(plotInfo[3][0],plotInfo[3][1])
        dataHist.GetXaxis().SetRangeUser(plotInfo[3][0],plotInfo[3][1])
    stack.GetHistogram().GetYaxis().SetTitle(plotInfo[1])

    dataHist.Draw("e,X0,same")
    legend.Draw("same")

    CMS_lumi.channelText = _channelText+plotInfo[4]
    CMS_lumi.CMS_lumi(canvas, 4, 11)
    canvas.Print("%s/%s.pdf"%(plotDirectory,histName),".pdf")
    canvas.Print("%s/%s.png"%(plotDirectory,histName),".png")

    ratio = dataHist.Clone("temp")
    ratio.Divide(stack.GetStack().Last())
 
 
    pad1.Clear()
    pad2.Clear()

    canvasRatio.cd()
    canvasRatio.ResetDrawn()

    pad1.Clear()
    pad2.Clear()


    pad1.cd()

    pad1.SetLogy(plotInfo[-1])
    #pad1.SetLogx(plotInfo[-1])
    stack.Draw('HIST')
#    pad1.Update()
    y2 = pad1.GetY2()
    
    stack.SetMinimum(1)
#    pad1.Update()
    stack.GetXaxis().SetTitle('')
#    stack.GetYaxis().SetTitle(dataHist.GetYaxis().GetTitle())

    stack.SetTitle('')
    stack.GetXaxis().SetLabelSize(0)
    stack.GetYaxis().SetLabelSize(gStyle.GetLabelSize()/(1.-padRatio+padOverlap))
    stack.GetYaxis().SetTitleSize(gStyle.GetTitleSize()/(1.-padRatio+padOverlap))
    stack.GetYaxis().SetTitleOffset(gStyle.GetTitleYOffset()*(1.-padRatio+padOverlap))
    dataHist.Draw('E,X0,SAME')
    legendR.Draw()
    ratio.SetTitle('')
            
    ratio.GetXaxis().SetLabelSize(gStyle.GetLabelSize()/(padRatio+padOverlap))
    ratio.GetYaxis().SetLabelSize(gStyle.GetLabelSize()/(padRatio+padOverlap))
    ratio.GetXaxis().SetTitleSize(gStyle.GetTitleSize()/(padRatio+padOverlap))
    ratio.GetYaxis().SetTitleSize(gStyle.GetTitleSize()/(padRatio+padOverlap))
    ratio.GetYaxis().SetTitleOffset(gStyle.GetTitleYOffset()*(padRatio+padOverlap-padGap))
    ratio.GetYaxis().SetRangeUser(0.75,1.25)
    ratio.GetYaxis().SetNdivisions(504)
    ratio.GetXaxis().SetTitle(plotInfo[0])
    ratio.GetYaxis().SetTitle("Data/MC")

    pad2.cd()
    ratio.SetMarkerStyle(dataHist.GetMarkerStyle())
    ratio.SetMarkerSize(dataHist.GetMarkerSize())
    ratio.SetLineColor(dataHist.GetLineColor())
    ratio.SetLineWidth(dataHist.GetLineWidth())

    oneLine = TF1("oneline","1",-9e9,9e9)
    oneLine.SetLineColor(kBlack)
    oneLine.SetLineWidth(1)
    oneLine.SetLineStyle(2)

    ratio.Draw('e,x0')
    oneLine.Draw("same")

#    pad2.Update()
    CMS_lumi.CMS_lumi(pad1, 4, 11)
    canvasRatio.Update()
    canvasRatio.RedrawAxis()

    canvasRatio.SaveAs("%s/%s_ratio.pdf"%(plotDirectory,histName))
    canvasRatio.SaveAs("%s/%s_ratio.png"%(plotDirectory,histName))
    canvasRatio.SetLogy(0)



for histName in preselhistograms:
	drawHist("presel_%s"%histName,preselhistograms[histName],plotDirectory,_file)

for histName in phoselhistograms:
    	drawHist("phosel_%s"%histName,phoselhistograms[histName],plotDirectory,_file)
#    drawHist("presel_%s"%histName,preselhistograms[histName],plotDirectory,_file)

# _file2  = TFile("histograms/mu/testBtaghists.root")

# drawHist("njets1Tag",      ["NJets", "Events", 1, [-1,10], ", =1 b-tag"    , NoLog], plotDirectory, _file2)
# drawHist("njets2Tag",      ["NJets", "Events", 1, [-1,10], ", #geq2 b-tags", NoLog], plotDirectory, _file2)
# drawHist("phoselnjets1Tag",["NJets", "Events", 1, [-1,10], ", =1 b-tag"    , NoLog], plotDirectory, _file2)
# drawHist("phoselnjets2Tag",["NJets", "Events", 1, [-1,10], ", #geq2 b-tags", NoLog], plotDirectory, _file2)
