from ROOT import *

import sys
import os

import subprocess
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-t", "--toys", dest="toys", default="10",type='int',
                     help="Specify how many toys you want to run on" )

(options, args) = parser.parse_args()

n_toys =options.toys

rand = TRandom3(0)
seeds=[]
for i in range(n_toys):
	seeds.append(rand.Integer(10000000))
#print seeds
#exit()

def run_commands(listofcommands):
        for command in listofcommands:
                print command
                p = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                f = p.communicate()

        return


#systematics =["TTbar_norm","VGamma_norm","VJets_norm","SingleTop_norm","Others_norm","Pileup","MuEff","Pdf","Q2","JECTotal","PhoEff","lumi","JER","BTagSF","phoscale","phosmear"]
#vals_=["pull","pull_up","pull_do","imp","imp_up","imp_do"]

#outputFile = TFile("PullsandImpacts.root","recreate")
#outputTree = TTree("CombineTree","CombineTree")
#TTbar_norm_pull=0.
#myvar = array( 'i', [ 0 ] )

#outputTree.Branch('myvar', myvar, 'myvar/I')

#outputTree.Branch("TTbar_norm_pull",&TTbar_norm_pull)
#for v in vals_:
#	for sys in systematics:
 #               sys_v=0.
#		print sys+"_"+v, "%s_%s"%(sys,v)
#		outputTree.Branch("%s_%s"%(sys,v), sys+"_"+v)


		



for seed in seeds:

	commands = ["combineTool.py -M Impacts -d datacard_Syst_ele_v5_binned.txt -m 125 --doInitialFit --robustFit 1 -t 1 --expectSignal=1. -s %i"%seed,
            "mv higgsCombine_initialFit_Test.MultiDimFit.mH125.%i.root higgsCombine_initialFit_Test.MultiDimFit.mH125.root"%seed,
            "combineTool.py -M Impacts -d datacard_Syst_ele_v5_binned.txt -m 125 --robustFit 1 --doFits -t 1 --expectSignal=1. -s %i"%seed]

	run_commands(commands)

	directoryContents = os.listdir(".")

	systList = []
	commands = []
	for fName in directoryContents:
    		if "higgsCombine_paramFit_Test" in fName:
        		syst = fName.split("higgsCombine_paramFit_Test_")[-1].split(".")[0]
        		print syst, fName
        		systList.append(fName)
        		commands.append("mv higgsCombine_paramFit_Test_%s.MultiDimFit.mH125.%i.root higgsCombine_paramFit_Test_%s.MultiDimFit.mH125.root"%(syst,seed, syst))
       
	run_commands(commands)

	commands=[]
	commands.append("combineTool.py -M Impacts -d datacard_Syst_ele_v5_binned.txt -m 125 -o impacts_toys.json")
	commands.append("plotImpacts.py -i impacts_toys.json -o impacts_trial -t parameterNames")
#	commands.append("mv impacts_.pdf impacts_%i.pdf"%seed)
#	commands.append("python extractpulls.py")

	run_commands(commands)



#outputFile.Close()

