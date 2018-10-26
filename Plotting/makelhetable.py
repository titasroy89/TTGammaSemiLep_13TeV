from ROOT import *


file_ =TFile.Open("root://cmseos.fnal.gov//store/user/lpctop/TTGamma/13TeV_AnalysisNtuples/electrons/V08_00_26_07/TTGamma_SingleLeptFromTbar_AnalysisNtuple.root")
tree = file_.Get("AnalysisTree")
print tree.GetEntries()
events =[]

table=''
count = 0.
#photon coming from a pion 
for entry in tree:
	print "Event Number : ",tree.event
	count+=1
        print "imc \t PID \t momPID \t GmomPID \t mcParentage \t Pt \t Phi \t Eta \t Mass \t mcStatus \t mcStatusFlag"
	for imc in range(len(tree.mcPID)):
	         	 
		 print imc, "\t", tree.mcPID[imc], "\t", tree.mcMomPID[imc], "\t", tree.mcGMomPID[imc], "\t", tree.mcParentage[imc],  "\t", "%.1f"%tree.mcPt[imc], "\t", "%.1f"%tree.mcPhi[imc], "\t", "%.1f"%tree.mcEta[imc], "\t", "%.1f"%tree.mcMass[imc], "\t", tree.mcStatus[imc], "\t", tree.mcStatusFlag[imc]
	if count==5:
		break
	print """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" 
        print 
        print 

 


#for i in range(events):
#	print tree.mcPt_.at(0), tree.

