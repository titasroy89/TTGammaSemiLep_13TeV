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
if [ "$jobType" == "QCD" ] ;	then
	channel="qcdmu"
	channelDir="qcdmuons"
	tupleExtraName1="QCDcr_"
	tupleExtraName2="__QCDcr"
fi
if [ "$jobType" == "Dilep" ] ;	then
	channel="dimu"
	channelDir="dimuons"
	tupleExtraName1="Dilep_"
	tupleExtraName2="__Dilep"
fi

outputdir="root://cmseos.fnal.gov//store/user/lpctop/TTGamma/13TeV_"

DannyEOS="root://cmseos.fnal.gov//store/user/dnoonan/13TeV_ggNTuples/V08_00_26_07/"
GGNtupleGroupEOSMC="root://cmseos.fnal.gov//store/user/lpcggntuples/ggNtuples/13TeV/mc/V08_00_26_07/"
TitasEOS="root://cmseos.fnal.gov//store/user/troy2012/13TeV_ggNTuples/V08_00_26_07/"
GGNtupleGroupEOSData="root://cmseos.fnal.gov//store/user/lpcggntuples/ggNtuples/13TeV/data/V08_00_26_07/"
LPCtop="root://cmseos.fnal.gov//store/user/lpctop/TTGamma/13TeV_ggNTuples/V08_00_26_07/"

inputfiles=("xrdfs root://cmseos.fnal.gov ls -u /store/user/lpctop/TopMass/13TeV_ggNTuples/V08_00_26_07/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/crab_TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/180423_165006/0000/" \
$DannyEOS"TTGamma_SingleLeptFromTbar_TuneCUETP8M2T4_13TeV-amcatnlo-pythia8.root" \
$DannyEOS"TTGamma_SingleLeptFromT_TuneCUETP8M2T4_13TeV-amcatnlo-pythia8.root" \
$DannyEOS"TTGamma_Dilept_TuneCUETP8M2T4_13TeV-amcatnlo-pythia8.root" \
$DannyEOS"TTGamma_Hadronic_TuneCUETP8M2T4_13TeV-amcatnlo-pythia8.root" \
$LPCtop"TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_newGenParticleList_1.root" \
$LPCtop"TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_newGenParticleList_2.root" \
$LPCtop"TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_newGenParticleList_3.root" \
$LPCtop"TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_newGenParticleList_4.root" \
$DannyEOS"TGJets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8.root" \
$LPCtop"W1JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_newGenParticleList.root" \
$LPCtop"W2JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_newGenParticleList.root" \
$LPCtop"W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_newGenParticleList.root" \
$LPCtop"W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_newGenParticleList.root" \
$TitasEOS"DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root" \
$TitasEOS"DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_1.root "$TitasEOS"DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext2.root" \
$TitasEOS"ST_s-channel_4f_InclusiveDecays_13TeV-amcatnlo-pythia8.root" \
$TitasEOS"ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1.root" \
$TitasEOS"ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1.root" \
$TitasEOS"ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1.root" \
$TitasEOS"ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1.root" \
$GGNtupleGroupEOSMC"TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8.root" \
$GGNtupleGroupEOSMC"TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8.root" \
$GGNtupleGroupEOSMC"TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8.root" \
$TitasEOS"ZGToLLG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.root" \
$TitasEOS"WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.root" \
$DannyEOS"WW_TuneCUETP8M1_13TeV-pythia8.root" \
$DannyEOS"WZ_TuneCUETP8M1_13TeV-pythia8.root" \
$DannyEOS"ZZ_TuneCUETP8M1_13TeV-pythia8.root" \
$GGNtupleGroupEOSMC"QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8.root" \
$GGNtupleGroupEOSMC"QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8.root" \
$GGNtupleGroupEOSMC"QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8.root" \
$GGNtupleGroupEOSMC"QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8.root" \
$GGNtupleGroupEOSMC"QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8.root" \
$GGNtupleGroupEOSMC"QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8.root" \
$GGNtupleGroupEOSMC"QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8.root" \
$GGNtupleGroupEOSMC"QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8.root" \
$GGNtupleGroupEOSMC"QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8.root" \
$GGNtupleGroupEOSMC"QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8.root" \
$GGNtupleGroupEOSMC"QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8.root" \
$DannyEOS"GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root" \
$DannyEOS"GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root" \
$DannyEOS"GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root" \
$DannyEOS"GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root" \
$DannyEOS"GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root" \
$GGNtupleGroupEOSData"job_SingleMu_Run2016B_FebReminiAOD.root" \
$GGNtupleGroupEOSData"job_SingleMu_Run2016C_FebReminiAOD.root" \
$GGNtupleGroupEOSData"job_SingleMu_Run2016D_FebReminiAOD.root" \
$GGNtupleGroupEOSData"job_SingleMu_Run2016E_FebReminiAOD.root" \
$GGNtupleGroupEOSData"job_SingleMu_Run2016F_FebReminiAOD.root" \
$GGNtupleGroupEOSData"job_SingleMu_Run2016G_FebReminiAOD.root" \
$GGNtupleGroupEOSData"job_SingleMu_Run2016H_FebReminiAODv2.root "$GGNtupleGroupEOSData"job_SingleMu_Run2016H_FebReminiAODv3.root")





sampleType=("TTbarPowheg" \
"TTGamma_SingleLeptFromTbar" \
"TTGamma_SingleLeptFromT" \
"TTGamma_Dilepton" \
"TTGamma_Hadronic" \
"TTbarPowheg1" \
"TTbarPowheg2" \
"TTbarPowheg3" \
"TTbarPowheg4" \
"TGJets" \
"W1jets" \
"W2jets" \
"W3jets" \
"W4jets" \
"DYjetsM10to50_MLM" \
"DYjetsM50_MLM" 
"ST_s-channel" \
"ST_t-channel" \
"ST_tbar-channel" \
"ST_tW-channel" \
"ST_tbarW-channel" \
"TTWtoQQ" \
"TTWtoLNu" \
"TTZtoLL" \
"ZGamma_01J_5f" \
"WGamma_01J_5f" \
"WW" \
"WZ" \
"ZZ" \
"QCD_Pt20to30_Mu" \
"QCD_Pt30to50_Mu" \
"QCD_Pt50to80_Mu" \
"QCD_Pt80to120_Mu" \
"QCD_Pt120to170_Mu" \
"QCD_Pt170to300_Mu" \
"QCD_Pt300to470_Mu" \
"QCD_Pt470to600_Mu" \
"QCD_Pt600to800_Mu" \
"QCD_Pt800to1000_Mu" \
"QCD_Pt1000toInf_Mu" \
"GJets_HT-40To100" \
"GJets_HT-100To200" \
"GJets_HT-200To400" \
"GJets_HT-400To600" \
"GJets_HT-600ToInf" \
"Data_SingleMu_b" \
"Data_SingleMu_c" \
"Data_SingleMu_d" \
"Data_SingleMu_e" \
"Data_SingleMu_f" \
"Data_SingleMu_g" \
"Data_SingleMu_h")


echo "AnalysisNtuple/makeSkim ${channel} ${sampleType[job]}_skim.root  `${inputfiles[job]} |grep ".root"` "  ##${inputfiles[job]}"
AnalysisNtuple/makeSkim ${channel} ${sampleType[job]}_skim.root  `${inputfiles[job]} |grep ".root"`   ##${inputfiles[job]}

#echo "AnalysisNtuple/makeAnalysisNtuple ${sampleType[job]}${tupleExtraName2} . ${outputdir}skims/${channelDir}/V08_00_26_07/${sampleType[job]}_skim.root"
#AnalysisNtuple/makeAnalysisNtuple ${sampleType[job]}${tupleExtraName2} . ${outputdir}skims/${channelDir}/V08_00_26_07/${sampleType[job]}_skim.root


#echo "AnalysisNtuple/makeCutflows_gen2 ${channel} ${sampleType[job]}_gen_skim.root ${inputfiles[job]}"
#AnalysisNtuple/makeCutflows_gen2 ${channel} ${sampleType[job]}_gen_skim.root ${inputfiles[job]}

#echo "AnalysisNtuple/makeAnalysisNtuple ${sampleType[job]}${tupleExtraName2} . ${sampleType[job]}_skim.root"
#AnalysisNtuple/makeAnalysisNtuple ${sampleType[job]}${tupleExtraName2} . ${sampleType[job]}_skim.root


#echo "xrdcp -f ${sampleType[job]}_gen_skim.root ${outputdir}skims/${channelDir}/V08_00_26_07/"
#xrdcp -f ${sampleType[job]}_gen_skim.root ${outputdir}skims/${channelDir}/V08_00_26_07/



echo "xrdcp -f ${sampleType[job]}_skim.root ${outputdir}skims/${channelDir}/V08_00_26_07/"
xrdcp -f ${sampleType[job]}_skim.root ${outputdir}skims/${channelDir}/V08_00_26_07/

#echo "xrdcp -f ${tupleExtraName1}${sampleType[job]}_AnalysisNtuple.root ${outputdir}AnalysisNtuples_new/${channelDir}/V08_00_26_07/"
#xrdcp -f ${tupleExtraName1}${sampleType[job]}_AnalysisNtuple.root ${outputdir}AnalysisNtuples_new/${channelDir}/V08_00_26_07/


