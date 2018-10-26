#!/bin/bash

job=$1
jobType=$2

if [ -z ${_CONDOR_SCRATCH_DIR} ] ; then 
	echo "Running Interactively" ; 
else
	echo "Running In Batch"
	cd ${_CONDOR_SCRATCH_DIR}
	echo ${_CONDOR_SCRATCH_DIR}
	echo "xrdcp root://cmseos.fnal.gov//store/user/"${USER}"/CMSSW_8_0_26_patch1.tgz ."
	xrdcp root://cmseos.fnal.gov//store/user/${USER}/CMSSW_8_0_26_patch1.tgz .
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
channel="ele"
channelDir="electrons"
tupleExtraName1=""
tupleExtraName2=""
if [ "$jobType" == "QCD" ] ;	then
	channel="qcdele"
	channelDir="qcdelectrons"
	tupleExtraName1="QCDcr_"
	tupleExtraName2="__QCDcr"
fi
if [ "$jobType" == "Dilep" ] ;	then
	channel="diele"
	channelDir="dielectrons"
	tupleExtraName1="Dilep_"
	tupleExtraName2="__Dilep"
fi

outputdir="root://cmseos.fnal.gov//store/user/lpctop/TTGamma/13TeV_"

DannyEOS="root://cmseos.fnal.gov//store/user/dnoonan/13TeV_ggNTuples/V08_00_26_07/"
GGNtupleGroupEOSMC="root://cmseos.fnal.gov//store/user/lpcggntuples/ggNtuples/13TeV/mc/V08_00_26_07/"
TitasEOS="root://cmseos.fnal.gov//store/user/troy2012/13TeV_ggNTuples/V08_00_26_07/"
GGNtupleGroupEOSData="root://cmseos.fnal.gov//store/user/lpcggntuples/ggNtuples/13TeV/data/V08_00_26_07/"
LPCtop="root://cmseos.fnal.gov//store/user/lpctop/TTGamma/13TeV_ggNTuples/V08_00_26_07/"

inputfiles=($DannyEOS"TTGamma_SingleLeptFromTbar_TuneCUETP8M2T4_13TeV-amcatnlo-pythia8.root" \
$DannyEOS"TTGamma_SingleLeptFromT_TuneCUETP8M2T4_13TeV-amcatnlo-pythia8.root" \
$DannyEOS"TTGamma_Dilept_TuneCUETP8M2T4_13TeV-amcatnlo-pythia8.root" \
$DannyEOS"TTGamma_Hadronic_TuneCUETP8M2T4_13TeV-amcatnlo-pythia8.root" \
$DannyEOS"TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_newGenParticleList_1.root" \
$DannyEOS"TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_newGenParticleList_2.root" \
$DannyEOS"TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_newGenParticleList_3.root" \
$DannyEOS"TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_newGenParticleList_4.root" \
$LPCtop"TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root" \
$LPCtop"TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root" \
$LPCtop"TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root" \
$DannyEOS"TGJets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8.root" \
$LPCtop"TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8-ext1.root" \
$LPCtop"TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root" \
$LPCtop"WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_temp_1of6.root" \
$LPCtop"WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_temp_2of6.root" \
$LPCtop"WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_temp_3of6.root" \
$LPCtop"WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_temp_4of6.root" \
$LPCtop"WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_temp_5of6.root" \
$LPCtop"WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_temp_6of6.root" \
$DannyEOS"W1JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_newGenParticleList.root" \
$DannyEOS"W2JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_newGenParticleList.root" \
$DannyEOS"W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_newGenParticleList.root" \
$DannyEOS"W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_newGenParticleList.root" \
$GGNtupleGroupEOSMC"DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_1.root "$GGNtupleGroupEOSMC"DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_2.root" \
$TitasEOS"DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_2_1of2.root "$TitasEOS"DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_2_1of2.root" \
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
$DannyEOS"WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-ext1.root "$DannyEOS"WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-ext2.root "$DannyEOS"WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-ext3.root" \
$DannyEOS"ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.root "$DannyEOS"ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-ext1.root" \
$TitasEOS"ZGToLLG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.root" \
$TitasEOS"WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.root" \
$DannyEOS"WW_TuneCUETP8M1_13TeV-pythia8.root" \
$DannyEOS"WZ_TuneCUETP8M1_13TeV-pythia8.root" \
$DannyEOS"ZZ_TuneCUETP8M1_13TeV-pythia8.root" \
$TitasEOS"QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8.root" \
$TitasEOS"QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8.root" \
$TitasEOS"QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8.root" \
$TitasEOS"QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8.root" \
$TitasEOS"QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8.root" \
$TitasEOS"QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8.root" \
$TitasEOS"QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8.root" \
$DannyEOS"GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root" \
$DannyEOS"GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root" \
$DannyEOS"GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root" \
$DannyEOS"GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root" \
$DannyEOS"GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root" \
$GGNtupleGroupEOSData"job_SingleElectron_Run2016B_FebReminiAOD.root" \
$GGNtupleGroupEOSData"job_SingleElectron_Run2016C_FebReminiAOD.root" \
$GGNtupleGroupEOSData"job_SingleElectron_Run2016D_FebReminiAOD.root" \
$GGNtupleGroupEOSData"job_SingleElectron_Run2016E_FebReminiAOD.root" \
$GGNtupleGroupEOSData"job_SingleElectron_Run2016F_FebReminiAOD.root" \
$GGNtupleGroupEOSData"job_SingleElectron_Run2016G_FebReminiAOD.root" \
$GGNtupleGroupEOSData"job_SingleElectron_Run2016H_FebReminiAODv2.root "$GGNtupleGroupEOSData"job_SingleElectron_Run2016H_FebReminiAODv3.root")









sampleType=("TTGamma_SingleLeptFromTbar" \
"TTGamma_SingleLeptFromT" \
"TTGamma_Dilepton" \
"TTGamma_Hadronic" \
"TTbarPowheg1" \
"TTbarPowheg2" \
"TTbarPowheg3" \
"TTbarPowheg4" \
"TTbarMadgraph_SingleLeptFromT" \
"TTbarMadgraph_SingleLeptFromTbar" \
"TTbarMadgraph_Dilepton" \
"TGJets" \
"TTGJets" \
"TTbarMadgraph" \
"WjetsInclusive1" \
"WjetsInclusive2" \
"WjetsInclusive3" \
"WjetsInclusive4" \
"WjetsInclusive5" \
"WjetsInclusive6" \
"W1jets" \
"W2jets" \
"W3jets" \
"W4jets" \
"DYjetsM10to50" \
"DYjetsM50" \
"DYjetsM10to50_MLM" \
"DYjetsM50_MLM" \
"ST_s-channel" \
"ST_t-channel" \
"ST_tbar-channel" \
"ST_tW-channel" \
"ST_tbarW-channel" \
"TTWtoQQ" \
"TTWtoLNu" \
"TTZtoLL" \
"WGamma" \
"ZGamma" \
"ZGamma_01J_5f" \
"WGamma_01J_5f" \
"WW" \
"WZ" \
"ZZ" \
"QCD_Pt20to30_Ele" \
"QCD_Pt30to50_Ele" \
"QCD_Pt50to80_Ele" \
"QCD_Pt80to120_Ele" \
"QCD_Pt120to170_Ele" \
"QCD_Pt170to300_Ele" \
"QCD_Pt300toInf_Ele" \
"GJets_HT-40To100" \
"GJets_HT-100To200" \
"GJets_HT-200To400" \
"GJets_HT-400To600" \
"GJets_HT-600ToInf" \
"Data_SingleEle_b" \
"Data_SingleEle_c" \
"Data_SingleEle_d" \
"Data_SingleEle_e" \
"Data_SingleEle_f" \
"Data_SingleEle_g" \
"Data_SingleEle_h")

#echo "AnalysisNtuple/makeSkim ${channel} ${sampleType[job]}_skim.root ${inputfiles[job]}"
#AnalysisNtuple/makeSkim ${channel} ${sampleType[job]}_skim.root ${inputfiles[job]}


#echo "AnalysisNtuple/makeCutflows_gen2 ${channel} ${sampleType[job]}_gen_skim.root ${inputfiles[job]}"
#AnalysisNtuple/makeCutflows_gen2 ${channel} ${sampleType[job]}_gen_skim.root ${inputfiles[job]}

echo "AnalysisNtuple/makeAnalysisNtuple ${sampleType[job]}${tupleExtraName2} . ${outputdir}skims/${channelDir}/V08_00_26_07/${sampleType[job]}_skim.root"
AnalysisNtuple/makeAnalysisNtuple ${sampleType[job]}${tupleExtraName2} . ${outputdir}skims/${channelDir}/V08_00_26_07/${sampleType[job]}_skim.root



#echo "xrdcp -f ${sampleType[job]}_skim.root ${outputdir}skims/${channelDir}/V08_00_26_07/"
#xrdcp -f ${sampleType[job]}_skim.root ${outputdir}skims/${channelDir}/V08_00_26_07/

echo "xrdcp -f ${tupleExtraName1}${sampleType[job]}_AnalysisNtuple.root ${outputdir}AnalysisNtuples_new/${channelDir}/V08_00_26_07/"
xrdcp -f ${tupleExtraName1}${sampleType[job]}_AnalysisNtuple.root ${outputdir}AnalysisNtuples_new/${channelDir}/V08_00_26_07/


