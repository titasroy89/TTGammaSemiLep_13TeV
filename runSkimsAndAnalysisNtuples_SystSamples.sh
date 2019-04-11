#!/bin/bash

job=$1
jobType=$2

if [ -z ${_CONDOR_SCRATCH_DIR} ] ; then 
	echo "Running Interactively" ; 
else
	echo "Running In Batch"
	cd ${_CONDOR_SCRATCH_DIR}
	echo ${_CONDOR_SCRATCH_DIR}
	echo "xrdcp root://cmseos.fnal.gov//store/user/troy2012/CMSSW_8_0_26_patch1.tgz ." 
	xrdcp root://cmseos.fnal.gov//store/user/troy2012/CMSSW_8_0_26_patch1.tgz .
	echo "tar -xvf CMSSW_8_0_26_patch1.tgz"
	tar -xzf CMSSW_8_0_26_patch1.tgz
	cd CMSSW_8_0_26_patch1/src/
	source /cvmfs/cms.cern.ch/cmsset_default.sh
	cd  TTGammaSemiLep_13TeV/
	echo "xrdcp -r root://cmseos.fnal.gov//store/user/dnoonan/DataPUfiles_2016.tgz ."
	xrdcp -r root://cmseos.fnal.gov//store/user/dnoonan/Data_Pileup.tgz .
	tar -xvf Data_Pileup.tgz
	sleep 5
fi

eval `scramv1 runtime -sh`
channel="mu"
channelDir="muons"
tupleExtraName1=""
tupleExtraName2=""
if [ "$jobType" == "mu" ] ;	then
	channel="mu"
	channelDir="muons"
fi
if [ "$jobType" == "ele" ] ;	then
	channel="ele"
	channelDir="electrons"
fi


lpctop="root://cmseos.fnal.gov//store/user/lpctop/TTGamma/13TeV_"
outputdir="root://cmseos.fnal.gov//store/user/troy2012/13TeV_"
DannyEOS="root://cmseos.fnal.gov//store/user/dnoonan/13TeV_ggNTuples/V08_00_26_07/"
GGNtupleGroupEOSMC="root://cmseos.fnal.gov//store/user/lpcggntuples/ggNtuples/13TeV/mc/V08_00_26_07/"
TitasEOS="root://cmseos.fnal.gov//store/user/troy2012/13TeV_ggNTuples/V08_00_26_07/"
GGNtupleGroupEOSData="root://cmseos.fnal.gov//store/user/lpcggntuples/ggNtuples/13TeV/data/V08_00_26_07/"
LPCtop="root://cmseos.fnal.gov//store/user/lpctop/13TeV_ggNTuples/V08_00_26_07/"
LPC="root://cmseos.fnal.gov//store/user/lpctop/TTGamma/13TeV_ggNTuples/V08_00_26_07/"



inputfiles=("xrdfs root://cmseos.fnal.gov ls -u /store/user/lpctop/TopMass/13TeV_ggNTuples/V08_00_26_07/TT_TuneCUETP8M2T4_GluonMoveCRTune_erdON_13TeV-powheg-pythia8/crab_TT_TuneCUETP8M2T4_GluonMoveCRTune_erdON_13TeV-powheg-pythia8/181217_224039/0000/" \
"xrdfs root://cmseos.fnal.gov ls -u /store/user/lpctop/TTGamma/13TeV_ggNTuples/V08_00_26_07/TT_TuneCUETP8M2T4_GluonMoveCRTune_13TeV-powheg-pythia8/crab_TT_TuneCUETP8M2T4_GluonMoveCRTune_13TeV-powheg-pythia8/190210_030605/0000/" \
"xrdfs root://cmseos.fnal.gov ls -u /store/user/lpctop/TopMass/13TeV_ggNTuples/V08_00_26_07/TT_TuneCUETP8M2T4_QCDbasedCRTune_erdON_13TeV-powheg-pythia8/crab_TT_TuneCUETP8M2T4_QCDbasedCRTune_erdON_13TeV-powheg-pythia8/181217_224106/0000/" \
"xrdfs root://cmseos.fnal.gov ls -u /store/user/lpctop/TopMass/13TeV_ggNTuples/V08_00_26_07/TT_TuneCUETP8M2T4_QCDbasedCRTune_erdON_13TeV-powheg-pythia8/crab_TT_TuneCUETP8M2T4_QCDbasedCRTune_erdON_13TeV-powheg-pythia8-ext1/181219_145300/0000/" \
"xrdfs root://cmseos.fnal.gov ls -u /store/user/lpctop/TopMass/13TeV_ggNTuples/V08_00_26_07/TT_TuneCUETP8M2T4_erdON_13TeV-powheg-pythia8/crab_TT_TuneCUETP8M2T4_erdON_13TeV-powheg-pythia8/181217_223849/0000/" \
"xrdfs root://cmseos.fnal.gov ls -u /store/user/lpctop/TopMass/13TeV_ggNTuples/V08_00_26_07/TT_TuneCUETP8M2T4_erdON_13TeV-powheg-pythia8/crab_TT_TuneCUETP8M2T4_erdON_13TeV-powheg-pythia8-ext1/181217_223920/0000/" \
"xrdfs root://cmseos.fnal.gov ls -u /store/user/lpctop/TopMass/13TeV_ggNTuples/V08_00_26_07/TT_TuneCUETP8M2T4down_13TeV-powheg-pythia8/crab_TT_TuneCUETP8M2T4down_13TeV-powheg-pythia8/181217_223738/0000/" \
"xrdfs root://cmseos.fnal.gov ls -u /store/user/lpctop/TopMass/13TeV_ggNTuples/V08_00_26_07/TT_TuneCUETP8M2T4down_13TeV-powheg-pythia8/crab_TT_TuneCUETP8M2T4down_13TeV-powheg-pythia8-ext1/181217_223806/0000/" \
"xrdfs root://cmseos.fnal.gov ls -u /store/user/lpctop/TopMass/13TeV_ggNTuples/V08_00_26_07/TT_TuneCUETP8M2T4up_13TeV-powheg-pythia8/crab_TT_TuneCUETP8M2T4up_13TeV-powheg-pythia8/181217_223638/0000/" \
"xrdfs root://cmseos.fnal.gov ls -u /store/user/lpctop/TopMass/13TeV_ggNTuples/V08_00_26_07/TT_TuneCUETP8M2T4up_13TeV-powheg-pythia8/crab_TT_TuneCUETP8M2T4up_13TeV-powheg-pythia8-ext1/181217_223710/0000/"  \
"xrdfs root://cmseos.fnal.gov ls -u /store/user/lpctop/TopMass/13TeV_ggNTuples/V08_00_26_07/TT_hdampDOWN_TuneCUETP8M2T4_13TeV-powheg-pythia8/crab_TT_hdampDOWN_TuneCUETP8M2T4_13TeV-powheg-pythia8/181216_231804/0000/"  \
"xrdfs root://cmseos.fnal.gov ls -u /store/user/lpctop/TopMass/13TeV_ggNTuples/V08_00_26_07/TT_hdampDOWN_TuneCUETP8M2T4_13TeV-powheg-pythia8/crab_TT_hdampDOWN_TuneCUETP8M2T4_13TeV-powheg-pythia8-ext1/190101_210317/0000/" \
"xrdfs root://cmseos.fnal.gov ls -u /store/user/lpctop/TopMass/13TeV_ggNTuples/V08_00_26_07/TT_hdampUP_TuneCUETP8M2T4_13TeV-powheg-pythia8/crab_TT_hdampUP_TuneCUETP8M2T4_13TeV-powheg-pythia8/181216_231701/0000/" \
"xrdfs root://cmseos.fnal.gov ls -u /store/user/lpctop/TopMass/13TeV_ggNTuples/V08_00_26_07/TT_hdampUP_TuneCUETP8M2T4_13TeV-powheg-pythia8/crab_TT_hdampUP_TuneCUETP8M2T4_13TeV-powheg-pythia8-ext1/181216_231731/0000/" \
$LPC"TTGamma_Dilept_TuneCUETP8M2T4_13TeV-madgraph-fsrdown-pythia8.root" \
$LPC"TTGamma_Dilept_TuneCUETP8M2T4_13TeV-madgraph-fsrup-pythia8.root" \
$LPC"TTGamma_Dilept_TuneCUETP8M2T4_13TeV-madgraph-isrdown-pythia8.root" \
$LPC"TTGamma_Dilept_TuneCUETP8M2T4_13TeV-madgraph-isrup-pythia8.root" \
$LPC"TTGamma_SingleLeptFromT_TuneCUETP8M2T4_13TeV-amcatnlo-fsrdown-pythia8-pythia8.root" \
$LPC"TTGamma_SingleLeptFromT_TuneCUETP8M2T4_13TeV-amcatnlo-fsrup-pythia8-pythia8.root" \
$LPC"TTGamma_SingleLeptFromT_TuneCUETP8M2T4_13TeV-amcatnlo-isrdown-pythia8-pythia8.root" \
$LPC"TTGamma_SingleLeptFromT_TuneCUETP8M2T4_13TeV-amcatnlo-isrup-pythia8-pythia8.root" \
$LPC"TTGamma_SingleLeptFromTbar_TuneCUETP8M2T4_13TeV-amcatnlo-fsrdown-pythia8-pythia8.root" \
$LPC"TTGamma_SingleLeptFromTbar_TuneCUETP8M2T4_13TeV-amcatnlo-fsrup-pythia8-pythia8.root" \
$LPC"TTGamma_SingleLeptFromTbar_TuneCUETP8M2T4_13TeV-amcatnlo-isrdown-pythia8-pythia8.root" \
$LPC"TTGamma_SingleLeptFromTbar_TuneCUETP8M2T4_13TeV-amcatnlo-isrup-pythia8-pythia8.root" \
$LPCtop"TT_TuneCUETP8M2T4_13TeV-powheg-isrup-pythia8.root" \
$LPCtop"TT_TuneCUETP8M2T4_13TeV-powheg-isrdown-pythia8.root" \
$LPCtop"TT_TuneCUETP8M2T4_13TeV-powheg-fsrup-pythia8.root" \
$LPCtop"TT_TuneCUETP8M2T4_13TeV-powheg-fsrdown-pythia8.root")


sampleType=("TTbarPowheg_GluonMoveCRTune_erdON" \
"TTbarPowheg_GluonMoveCRTune" \
"TTbarPowheg_QCDbasedCRTune_erdON" \
"TTbarPowheg_QCDbasedCRTune_erdON_ext1" \
"TTbarPowheg_TuneCUETP8M2T4_erdON" \
"TTbarPowheg_TuneCUETP8M2T4_erdON_ext1" \
"TTbarPowheg_TuneCUETP8M2T4down" \
"TTbarPowheg_TuneCUETP8M2T4down_ext1" \
"TTbarPowheg_TuneCUETP8M2T4up" \
"TTbarPowheg_TuneCUETP8M2T4up_ext1" \
"TTbarPowheg_hdampDOWN" \
"TTbarPowheg_hdampDOWN_ext1" \
"TTbarPowheg_hdampUP" \
"TTbarPowheg_hdampUP_ext1" \
"TTGamma_Dilepton_fsrDown" \
"TTGamma_Dilepton_fsrUp" \
"TTGamma_Dilepton_isrDown" \
"TTGamma_Dilepton_isrUp" \
"TTGamma_SingleLeptFromT_fsrDown" \
"TTGamma_SingleLeptFromT_fsrUp" \
"TTGamma_SingleLeptFromT_isrDown" \
"TTGamma_SingleLeptFromT_isrUp" \
"TTGamma_SingleLeptFromTbar_fsrDown" \
"TTGamma_SingleLeptFromTbar_fsrUp" \
"TTGamma_SingleLeptFromTbar_isrDown" \
"TTGamma_SingleLeptFromTbar_isrUp" \
"TTbarPowheg_isrUp" \
"TTbarPowheg_isrDown" \
"TTbarPowheg_fsrUp" \
"TTbarPowheg_fsrDown")

skimarea="root://cmseos.fnal.gov//store/user/troy2012/13TeV_skims/${channelDir}/V08_00_26_07/"

inputfiles=($skimarea"TTbarPowheg_GluonMoveCRTune_erdON_skim.root" \
$skimarea"TTbarPowheg_GluonMoveCRTune_skim.root" \
$skimarea"TTbarPowheg_QCDbasedCRTune_erdON_skim.root" \
$skimarea"TTbarPowheg_QCDbasedCRTune_erdON_ext1_skim.root" \
$skimarea"TTbarPowheg_TuneCUETP8M2T4_erdON_skim.root" 
$skimarea"TTbarPowheg_TuneCUETP8M2T4_erdON_ext1_skim.root" \
$skimarea"TTbarPowheg_TuneCUETP8M2T4down_skim.root" \
$skimarea"TTbarPowheg_TuneCUETP8M2T4down_ext1_skim.root" \
$skimarea"TTbarPowheg_TuneCUETP8M2T4up_skim.root" \
$skimarea"TTbarPowheg_TuneCUETP8M2T4up_ext1_skim.root" \
$skimarea"TTbarPowheg_hdampDOWN_skim.root" \
$skimarea"TTbarPowheg_hdampDOWN_ext1_skim.root" \
$skimarea"TTbarPowheg_hdampUP_skim.root" \
$skimarea"TTbarPowheg_hdampUP_ext1_skim.root" \
$skimarea"TTGamma_Dilepton_fsrDown_skim.root" \
$skimarea"TTGamma_Dilepton_fsrUp_skim.root" \
$skimarea"TTGamma_Dilepton_isrDown_skim.root" \
$skimarea"TTGamma_Dilepton_isrUp_skim.root" \
$skimarea"TTGamma_SemiLeptFromT_fsrDown_skim.root" \
$skimarea"TTGamma_SemiLeptFromT_fsrUp_skim.root" \
$skimarea"TTGamma_SemiLeptFromT_isrDown_skim.root" \
$skimarea"TTGamma_SemiLeptFromT_isrUp_skim.root" \
$skimarea"TTGamma_SemiLeptFromTbar_fsrDown_skim.root" \
$skimarea"TTGamma_SemiLeptFromTbar_fsrUp_skim.root" \
$skimarea"TTGamma_SemiLeptFromTbar_isrDown_skim.root" \
$skimarea"TTGamma_SemiLeptFromTbar_isrUp_skim.root" \
$skimarea"TTbarPowheg_isrUp_skim.root" \
$skimarea"TTbarPowheg_isrDown_skim.root" \
$skimarea"TTbarPowheg_fsrUp_skim.root" \
$skimarea"TTbarPowheg_fsrDown_skim.root")

skimarealpctop="root://cmseos.fnal.gov//store/user/lpctop/TTGamma/13TeV_skims/${channelDir}/V08_00_26_07/"

inputfileslpctop=($skimarealpctop"TTbarPowheg_QCDbasedCRTune_erdON_full_skim.root" \
$skimarealpctop"TTbarPowheg_TuneCUETP8M2T4_erdON_full_skim.root" \
$skimarealpctop"TTbarPowheg_TuneCUETP8M2T4down_full_skim.root" \
$skimarealpctop"TTbarPowheg_hdampDOWN_full_skim.root" \
$skimarealpctop"TTbarPowheg_hdampUP_full_skim.root")





sampleOutput=("GluonMoveCRTune_erdON_up_TTbarPowheg" \
"GluonMoveCRTune_TTbarPowheg" \
"QCDbasedCRTune_erdON_up_ext0_TTbarPowheg" \
"QCDbasedCRTune_erdON_up_ext1_TTbarPowheg" \
"TuneCUETP8M2T4_erdON_up_ext0_TTbarPowheg" \
"TuneCUETP8M2T4_erdON_up_ext1_TTbarPowheg" \
"Tune_down_ext0_TTbarPowheg" \
"Tune_down_ext1_TTbarPowheg" \
"Tune_up_ext0_TTbarPowheg" \
"Tune_up_ext1_TTbarPowheg" \
"hdamp_down_ext0_TTbarPowheg" \
"hdamp_down_ext1_TTbarPowheg" \
"hdamp_up_ext0_TTbarPowheg" \
"hdamp_up_ext1_TTbarPowheg" \
"fsr_down_TTGamma_Dilepton" \
"fsr_up_TTGamma_Dilepton" \
"isr_down_TTGamma_Dilepton" \
"isr_up_TTGamma_Dilepton" \
"fsr_down_TTGamma_SingleLeptFromT" \
"fsr_up_TTGamma_SingleLeptFromT" \
"isr_down_TTGamma_SingleLeptFromT" \
"isr_up_TTGamma_SingleLeptFromT" \
"fsr_down_TTGamma_SingleLeptFromTbar" \
"fsr_up_TTGamma_SingleLeptFromTbar" \
"isr_down_TTGamma_SingleLeptFromTbar" \
"isr_up_TTGamma_SingleLeptFromTbar" \
"isr_up_TTbarPowheg" \
"isr_down_TTbarPowheg" \
"fsr_up_TTbarPowheg" \
"fsr_down_TTbarPowheg")


sampleOutput_new=("QCDbasedCRTune_erdON_TTbarPowheg" \
"TuneCUETP8M2T4_erdON_TTbarPowheg" \
"TuneCUETP8M2T4down_TTbarPowheg" \
"hdampDOWN_TTbarPowheg" \
"hdampUP_TTbarPowheg")

#echo "AnalysisNtuple/makeSkim ${channel} ${sampleType[job]}_skim.root `${inputfiles[job]} |grep ".root"` "
#AnalysisNtuple/makeSkim ${channel} ${sampleType[job]}_skim.root `${inputfiles[job]} |grep ".root"` 

echo "AnalysisNtuple/makeAnalysisNtuple ${sampleOutput[job]} . ${inputfiles[job]}"
AnalysisNtuple/makeAnalysisNtuple ${sampleOutput[job]} . ${inputfiles[job]}


#echo "xrdcp -f ${sampleType[job]}_skim.root ${outputdir}skims/${channelDir}/V08_00_26_07/"
#xrdcp -f ${sampleType[job]}_skim.root ${outputdir}skims/${channelDir}/V08_00_26_07/

echo "xrdcp -f ${sampleOutput[job]}_AnalysisNtuple.root ${lpctop}AnalysisNtuples_new/systematics_${channelDir}/V08_00_26_07/"
xrdcp -f ${sampleOutput[job]}_AnalysisNtuple.root ${lpctop}AnalysisNtuples_new/systematics_${channelDir}/V08_00_26_07/


