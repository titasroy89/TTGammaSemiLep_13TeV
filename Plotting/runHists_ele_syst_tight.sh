#!/bin/bash

job=$1
jobType=$2

if [ -z ${_CONDOR_SCRATCH_DIR} ] ; then
        echo "Running Interactively" ;
else
        echo "Running In Batch"
        cd ${_CONDOR_SCRATCH_DIR}
        echo ${_CONDOR_SCRATCH_DIR}
	source /cvmfs/cms.cern.ch/cmsset_default.sh
	export SCRAM_ARCH=slc6_amd64_gcc530
	eval `scramv1 project CMSSW CMSSW_8_0_25`
	cd CMSSW_8_0_25/src/
	eval `scramv1 runtime -sh` 
	echo "CMSSW: "$CMSSW_BASE
        echo "xrdcp root://cmseos.fnal.gov//store/user/"${USER}"/makeHistsfolder.tar.gz ."
        xrdcp root://cmseos.fnal.gov//store/user/${USER}/makeHistsfolder.tar.gz .
        echo "tar -xzf makeHistsfolder.tar.gz"
        tar -xzf makeHistsfolder.tar.gz
        rm makeHistsfolder.tar.gz
       
	
#	source /cvmfs/cms.cern.ch/cmsset_default.sh
	cd makeHistsfolder
        sleep 5
fi

eval `scramv1 runtime -sh`


systematic=false
channelDir="electrons"
tupleExtraName1=""
if [ "$jobType" == "EleEff" ] ;        then
        channel="ele"
        channelDir="electrons"
        tupleExtraName1="EleEff"
        systematic=true
fi
if [ "$jobType" == "PhoEff" ] ;        then
        channel="ele"
        channelDir="electrons"
        tupleExtraName1="PhoEff"
        systematic=true
fi
if [ "$jobType" == "phosmear" ] ;        then
        channel="ele"
        channelDir="electrons"
        tupleExtraName1="phosmear"
        systematic=true
fi
if [ "$jobType" == "phoscale" ] ;        then
        channel="ele"
        channelDir="electrons"
        tupleExtraName1="phoscale"
        systematic=true
fi
if [ "$jobType" == "elesmear" ] ;        then
        channel="ele"
        channelDir="electrons"
        tupleExtraName1="elesmear"
        systematic=true
fi
if [ "$jobType" == "elescale" ] ;        then
        channel="ele"
        channelDir="electrons"
        tupleExtraName1="elescale"
        systematic=true
fi

if [ "$jobType" == "PU" ] ;        then
        channel="ele"
        channelDir="electrons"
        tupleExtraName1="PU"
        systematic=true
fi
if [ "$jobType" == "BTagSF" ] ;        then
        channel="ele"
        channelDir="electrons"
        tupleExtraName1="BTagSF"
        systematic=true
fi

if [ "$jobType" == "JER" ] ;        then
        channel="ele"
        channelDir="electrons"
        tupleExtraName1="JER"
        systematic=true
fi
if [ "$jobType" == "JECTotal" ] ;        then
        channel="ele"
        channelDir="electrons"
        tupleExtraName1="JECTotal"
        systematic=true
fi

if [ "$jobType" == "Pdf" ] ;        then
        channel="ele"
        channelDir="electrons"
        tupleExtraName1="Pdf"
        systematic=true
fi

if [ "$jobType" == "Q2" ] ;        then
        channel="ele"
        channelDir="electrons"
        tupleExtraName1="Q2"
        systematic=true
fi


if [ "$jobType" == "isr" ] ;        then
        channel="ele"
        channelDir="electrons"
        tupleExtraName1="isr"
        systematic=true
fi

if [ "$jobType" == "fsr" ] ;        then
        channel="ele"
        channelDir="electrons"
        tupleExtraName1="fsr"
        systematic=true
fi




outputdir="root://cmseos.fnal.gov//store/user/lpctop/TTGamma/13TeV_Histograms/electrons/V08_00_26_07/"
#tight0bselection=false

sampleType=("TTGamma" \
"TTbar" \
"TTV" \
"TGJets" \
"SingleTop" \
"WJets" \
"ZJets" \
"WGamma" \
"ZGamma" \
"Diboson")



if [ "$systematic" = false ]; then

	echo "python makeHistograms.py -c Ele -s ${sampleType[job]} --Tight0b --plot phosel_Njet_barrel --plot phosel_Njet_GenuinePhoton_barrel --plot phosel_Njet_MisIDEle_barrel --plot phosel_Njet_NonPrompt_barrel --plot phosel_Njet_HadronicPhoton_barrel --plot phosel_Njet_HadronicFake_barrel"
	python makeHistograms.py -c Ele -s ${sampleType[job]} --Tight0b --plot phosel_Njet_barrel --plot phosel_Njet_GenuinePhoton_barrel --plot phosel_Njet_MisIDEle_barrel --plot phosel_Njet_NonPrompt_barrel --plot phosel_Njet_HadronicPhoton_barrel --plot phosel_Njet_HadronicFake_barrel


#	echo "xrdcp -f histograms/ele/hists_tight0b/${sampleType[job]}.root ${outputdir}hists_tight0b/"
#	xrdcp -f histograms/ele/hists_tight0b/${sampleType[job]}.root ${outputdir}hists_tight0b/


	echo "python makeHistograms.py -c Ele -s ${sampleType[job]} --Tight --morePlots"
        python makeHistograms.py -c Ele -s ${sampleType[job]} --Tight --morePlots


  #      echo "xrdcp -f histograms/ele/hists_tight/${sampleType[job]}.root ${outputdir}hists_tight/"
   #     xrdcp -f histograms/ele/hists_tight/${sampleType[job]}.root ${outputdir}hists_tight/


	echo "python makeHistograms.py -c Ele -s ${sampleType[job]} --LooseCRe3g0 --EgammaPlots"
        python makeHistograms.py -c Ele -s ${sampleType[job]} --LooseCRe3g0 --EgammaPlots
#

  #      echo "xrdcp -f histograms/ele/hists_looseCRe3g0/${sampleType[job]}.root ${outputdir}hists_tight/"
   #     xrdcp -f histograms/ele/hists_looseCRe3g0/${sampleType[job]}.root ${outputdir}hists_looseCRe3g0/



        echo "python makeHistograms.py -c QCDEle -s ${sampleType[job]} --Tight0b --plot phosel_Njet_barrel --plot phosel_Njet_GenuinePhoton_barrel --plot phosel_Njet_MisIDEle_barrel --plot phosel_Njet_NonPrompt_barrel --plot phosel_Njet_HadronicPhoton_barrel --plot phosel_Njet_HadronicFake_barrel"
        python makeHistograms.py -c QCDEle -s ${sampleType[job]} --Tight0b --plot phosel_Njet_barrel --plot phosel_Njet_GenuinePhoton_barrel --plot phosel_Njet_MisIDEle_barrel --plot phosel_Njet_NonPrompt_barrel --plot phosel_Njet_HadronicPhoton_barrel --plot phosel_Njet_HadronicFake_barrel


 #	echo "xrdcp -f histograms/ele/qcdhistsCR_tight0b/${sampleType[job]}.root ${outputdir}qcdhistsCR_tight0b/"
  #	xrdcp -f histograms/ele/qcdhistsCR_tight0b/${sampleType[job]}.root ${outputdir}qcdhistsCR_tight0b/

	echo "python makeHistograms.py -c QCDEle -s ${sampleType[job]} --Tight --morePlots"
 	python makeHistograms.py -c QCDEle -s ${sampleType[job]} --Tight --morePlots

#	echo "xrdcp -f histograms/ele/qcdhistsCR_tight/${sampleType[job]}.root ${outputdir}qcdhistsCR_tight/"
 #       xrdcp -f histograms/ele/qcdhistsCR_tight/${sampleType[job]}.root ${outputdir}qcdhistsCR_tight/

        
	echo "python makeHistograms.py -c QCDEle -s ${sampleType[job]} --LooseCRe3g0 --EgammaPlots"
        python makeHistograms.py -c QCDEle -s ${sampleType[job]} --LooseCRe3g0 --EgammaPlots

  #      echo "xrdcp -f histograms/ele/qcdhistsCR_looseCRe3g0/${sampleType[job]}.root ${outputdir}qcdhistsCR_looseCRe3g0/"
   #     xrdcp -f histograms/ele/qcdhistsCR_looseCRe3g0/${sampleType[job]}.root ${outputdir}qcdhistsCR_looseCRe3g0/

fi





if [ "$systematic" = true ]; then
        echo "python makeHistograms.py -c Ele -s ${sampleType[job]} --syst ${tupleExtraName1} --lev up --Tight0b --plot phosel_Njet_barrel --plot phosel_Njet_GenuinePhoton_barrel --plot phosel_Njet_MisIDEle_barrel --plot phosel_Njet_NonPrompt_barrel --plot phosel_Njet_HadronicPhoton_barrel --plot phosel_Njet_HadronicFake_barrel"
        python makeHistograms.py -c Ele -s ${sampleType[job]} --syst ${tupleExtraName1} --lev up --Tight0b --plot phosel_Njet_barrel --plot phosel_Njet_GenuinePhoton_barrel --plot phosel_Njet_MisIDEle_barrel --plot phosel_Njet_NonPrompt_barrel --plot phosel_Njet_HadronicPhoton_barrel --plot phosel_Njet_HadronicFake_barrel


 #       echo "xrdcp -f histograms/ele/hists${tupleExtraName1}_up_tight0b/${sampleType[job]}.root ${outputdir}hists${tupleExtraName1}_up_tight0b/"
  #      xrdcp -f histograms/ele/hists${tupleExtraName1}_up_tight0b/${sampleType[job]}.root ${outputdir}hists${tupleExtraName1}_up_tight0b/


        echo "python makeHistograms.py -c Ele -s ${sampleType[job]} --syst ${tupleExtraName1} --lev down --Tight0b --plot phosel_Njet_barrel --plot phosel_Njet_GenuinePhoton_barrel --plot phosel_Njet_MisIDEle_barrel --plot phosel_Njet_NonPrompt_barrel --plot phosel_Njet_HadronicPhoton_barrel --plot phosel_Njet_HadronicFake_barrel"
        python makeHistograms.py -c Ele -s ${sampleType[job]} --syst ${tupleExtraName1} --lev down --Tight0b --plot phosel_Njet_barrel --plot phosel_Njet_GenuinePhoton_barrel --plot phosel_Njet_MisIDEle_barrel --plot phosel_Njet_NonPrompt_barrel --plot phosel_Njet_HadronicPhoton_barrel --plot phosel_Njet_HadronicFake_barrel


   #     echo "xrdcp -f histograms/ele/hists${tupleExtraName1}_down_tight0b/${sampleType[job]}.root ${outputdir}hists${tupleExtraName1}_down_tight0b/"
    #    xrdcp -f histograms/ele/hists${tupleExtraName1}_down_tight0b/${sampleType[job]}.root ${outputdir}hists${tupleExtraName1}_down_tight0b/


	echo "python makeHistograms.py -c Ele -s ${sampleType[job]} --syst ${tupleExtraName1} --lev up --Tight --morePlots"
        python makeHistograms.py -c Ele -s ${sampleType[job]} --syst ${tupleExtraName1} --lev up --Tight --morePlots


  #      echo "xrdcp -f histograms/ele/hists${tupleExtraName1}_up_tight/${sampleType[job]}.root ${outputdir}hists${tupleExtraName1}_up_tight/"
   #     xrdcp -f histograms/ele/hists${tupleExtraName1}_up_tight/${sampleType[job]}.root ${outputdir}hists${tupleExtraName1}_up_tight/


        echo "python makeHistograms.py -c Ele -s ${sampleType[job]} --syst ${tupleExtraName1} --lev down --Tight --morePlots"
        python makeHistograms.py -c Ele -s ${sampleType[job]} --syst ${tupleExtraName1} --lev down --Tight --morePlots


     #   echo "xrdcp -f histograms/ele/hists${tupleExtraName1}_down_tight/${sampleType[job]}.root ${outputdir}hists${tupleExtraName1}_down_tight/"
      #  xrdcp -f histograms/ele/hists${tupleExtraName1}_down_tight/${sampleType[job]}.root ${outputdir}hists${tupleExtraName1}_down_tight/


	echo "python makeHistograms.py -c Ele -s ${sampleType[job]} --syst ${tupleExtraName1} --lev up --LooseCRe3g0 --EgammaPlots"
        python makeHistograms.py -c Ele -s ${sampleType[job]} --syst ${tupleExtraName1} --lev up --LooseCRe3g0 --EgammaPlots


  #      echo "xrdcp -f histograms/ele/hists${tupleExtraName1}_up_looseCRe3g0/${sampleType[job]}.root ${outputdir}hists${tupleExtraName1}_up_looseCRe3g0/"
   #     xrdcp -f histograms/ele/hists${tupleExtraName1}_up_looseCRe3g0/${sampleType[job]}.root ${outputdir}hists${tupleExtraName1}_up_looseCRe3g0/


        echo "python makeHistograms.py -c Ele -s ${sampleType[job]} --syst ${tupleExtraName1} --lev down --LooseCRe3g0 --EgammaPlots"
        python makeHistograms.py -c Ele -s ${sampleType[job]} --syst ${tupleExtraName1} --lev down --LooseCRe3g0 --EgammaPlots


     #   echo "xrdcp -f histograms/ele/hists${tupleExtraName1}_down_looseCRe3g0/${sampleType[job]}.root ${outputdir}hists${tupleExtraName1}_down_looseCRe3g0/"
      #  xrdcp -f histograms/ele/hists${tupleExtraName1}_down_looseCRe3g0/${sampleType[job]}.root ${outputdir}hists${tupleExtraName1}_down_looseCRe3g0/
fi







