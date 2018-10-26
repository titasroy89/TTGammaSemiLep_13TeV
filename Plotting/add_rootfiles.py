from ROOT import *


f1_mu= TFile("Combine_withDDTemplateData_v6_mu_tight_binned_PDF.root","read")

f2_ele=TFile("Combine_withDDTemplateData_v6_ele_tight_binned_PDF.root","read")


combFile=TFile("Combine_semilep.root","recreate")

observations =["ChHad","M3","M3_control","btag"]


#if finalState=="mu":
 #       systematics = ["JER","JECTotal","phosmear","phoscale","BTagSF","Q2","Pdf","PU","MuEff","PhoEff"]
#else:
 #       systematics = ["JER","JECTotal","phosmear","phoscale","BTagSF","Q2","Pdf","PU","EleEff","PhoEff","elesmear","elescale"]

process = ["data_obs","TTGamma_Prompt","TTGamma_NonPrompt","TTbar_Prompt","TTbar_NonPrompt","VGamma_Prompt","VGamma_NonPrompt","Other_Prompt","Other_NonPrompt"]
for obs in observations:
	
	if obs=="M3_control":
		samples=["TTGamma","TTbar","VGamma","Other","data_obs"]
	else:
		samples=process
	for s in samples:
		combFile.mkdir("%s/%s"%(obs,s))
		combFile.cd("%s/%s"%(obs,s))
		print f1_mu,"%s/%s/nominal"%(obs,s)	
		nom=f1_mu.Get("%s/%s/nominal"%(obs,s)).Clone("nomina")
                print f1_mu, "%s/%s/nominal"%(obs,s)
		nom.Add(f2_ele.Get("%s/%s/nominal"%(obs,s)))
		nom.Write("nominal")
		if "TT" in s:
			systematics=["JER","JECTotal","phosmear","phoscale","BTagSF","Q2","Pdf","PU","PhoEff","isr","fsr"]
		else:
			systematics=["JER","JECTotal","phosmear","phoscale","BTagSF","Q2","Pdf","PU","PhoEff"]
		
		if "_Prompt" in s:
			systematics.append("MisIDEleshape")
                if "ChHad" in obs and "_NonPrompt" in s:
			systematics=["shapeDD"]
		for syst in systematics:
			print syst
                        if syst=="Q2" or "Pdf" in syst:
				if "TT" not in s: continue
                        if "BTagSF" in syst and obs=="btag":continue
			if s=="data_obs":continue
			if "TTGamma" in s and syst=="Pdf":
                                
				sys=f1_mu.Get("%s/%s/%ssignalUp"%(obs,s,syst)).Clone("%sUp"%syst)
				sys.Add(f2_ele.Get("%s/%s/%ssignalUp"%(obs,s,syst)))
				sys2=f1_mu.Get("%s/%s/%ssignalDown"%(obs,s,syst)).Clone("%sDown"%syst)
                                sys2.Add(f2_ele.Get("%s/%s/%ssignalDown"%(obs,s,syst)))
				sys.Write("%ssignalUp"%syst)
				sys2.Write("%ssignalDown"%syst)

				
			else:
				print f1_mu, "%s/%s/%sUp"%(obs,s,syst)
                                sys=f1_mu.Get("%s/%s/%sUp"%(obs,s,syst)).Clone("%sUp"%syst)
				print f2_ele, obs,s,syst
				sys.Add(f2_ele.Get("%s/%s/%sUp"%(obs,s,syst)))
				sys2=f1_mu.Get("%s/%s/%sDown"%(obs,s,syst)).Clone("%sDown"%syst)
                                sys2.Add(f2_ele.Get("%s/%s/%sDown"%(obs,s,syst)))
				sys.Write("%sUp"%syst)
                                sys2.Write("%sDown"%syst)

		for syst in ["EleEff", "elescale","elesmear"]:
			if s=="data_obs":continue
			if obs=="ChHad" and "_NonPrompt" in s:continue
			sys=f2_ele.Get("%s/%s/%sUp"%(obs,s,syst))
			print f1_mu, "%s/%s/nominal"%(obs,s)
			sys.Add(f1_mu.Get("%s/%s/nominal"%(obs,s)))
			print f2_ele, "%s/%s/%sDown"%(obs,s,syst)
			sys2=f2_ele.Get("%s/%s/%sDown"%(obs,s,syst)) 
			sys2.Add(f1_mu.Get("%s/%s/nominal"%(obs,s)))     
			sys.Write("%sUp"%syst)
                        sys2.Write("%sDown"%syst)	

		for syst in ["MuEff"]:
			if s=="data_obs":continue
			if obs=="ChHad" and "_NonPrompt" in s:continue
			sys=f1_mu.Get("%s/%s/%sUp"%(obs,s,syst)) 
                        sys.Add(f2_ele.Get("%s/%s/nominal"%(obs,s)))     

                        sys2=f1_mu.Get("%s/%s/%sDown"%(obs,s,syst))
                        sys2.Add(f2_ele.Get("%s/%s/nominal"%(obs,s)))
                        sys.Write("%sUp"%syst)
                        sys2.Write("%sDown"%syst)
		
			



combFile.Close()
