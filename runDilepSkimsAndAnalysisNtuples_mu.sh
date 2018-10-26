#!/bin/bash

job=$1

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


outputdir="root://cmseos.fnal.gov//store/user/lpctop/TTGamma/13TeV_"


files=("TTGamma_SingleLeptFromTbar_" \
"TTGamma_SingleLeptFromT_" \
"TTGamma_Dilepton_" \
"TTGamma_Hadronic_" \
"TTbarPowheg1_" \
"TTbarPowheg2_" \
"TTbarPowheg3_" \
"TTbarPowheg4_" \
"TGJets_" \
"W1jets_" \
"W2jets_" \
"W3jets_" \
"W4jets_" \
"DYjetsM10to50_" \
"DYjetsM50_" \
"DYjetsM10to50_MLM_" \
"DYjetsM50_MLM_" \
"ST_s-channel_" \
"ST_t-channel_" \
"ST_tbar-channel_" \
"ST_tW-channel_" \
"ST_tbarW-channel_" \
"TTWtoQQ_" \
"TTWtoLNu_" \
"TTZtoLL_" \
"ZGamma_01J_5f_" \
"WGamma_01J_5f_" \
"WW_" \
"WZ_" \
"ZZ_" \
"QCD_Pt20to30_Mu_" \
"QCD_Pt30to50_Mu_" \
"QCD_Pt50to80_Mu_" \
"QCD_Pt80to120_Mu_" \
"QCD_Pt120to170_Mu_" \
"QCD_Pt170to300_Mu_" \
"QCD_Pt300to470_Mu_" \
"QCD_Pt470to600_Mu_" \
"QCD_Pt600to800_Mu_" \
"QCD_Pt800to1000_Mu_" \
"QCD_Pt1000toInf_Mu_" \
"Data_SingleMu_b_" \
"Data_SingleMu_c_" \
"Data_SingleMu_d_" \
"Data_SingleMu_e_" \
"Data_SingleMu_f_" \
"Data_SingleMu_g_" \
"Data_SingleMu_h_")

DannyEOS="root://cmseos.fnal.gov//store/user/dnoonan/13TeV_ggNTuples/V08_00_26_07/"
GGNtupleGroupEOSMC="root://cmseos.fnal.gov//store/user/lpcggntuples/ggNtuples/13TeV/mc/V08_00_26_07/"
TitasEOS="root://cmseos.fnal.gov//store/user/troy2012/13TeV_ggNTuples/V08_00_26_07/"
GGNtupleGroupEOSData="root://cmseos.fnal.gov//store/user/lpcggntuples/ggNtuples/13TeV/data/V08_00_26_07/"
GroupLPCEOS="root://cmseos.fnal.gov//store/user/lpctop/TTGamma/13TeV_ggNTuples/V08_00_26_07/"

inputfiles=($DannyEOS"TTGamma_SingleLeptFromTbar_TuneCUETP8M2T4_13TeV-amcatnlo-pythia8.root" \
$DannyEOS"TTGamma_SingleLeptFromT_TuneCUETP8M2T4_13TeV-amcatnlo-pythia8.root" \
$DannyEOS"TTGamma_Dilept_TuneCUETP8M2T4_13TeV-amcatnlo-pythia8.root" \
$DannyEOS"TTGamma_Hadronic_TuneCUETP8M2T4_13TeV-amcatnlo-pythia8.root" \
$GroupLPCEOS"TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_newGenParticleList_1.root" \
$GroupLPCEOS"TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_newGenParticleList_2.root" \
$GroupLPCEOS"TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_newGenParticleList_3.root" \
$GroupLPCEOS"TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_newGenParticleList_4.root" \
$DannyEOS"TGJets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8.root" \
$GroupLPCEOS"W1JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_newGenParticleList.root" \
$GroupLPCEOS"W2JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_newGenParticleList.root" \
$GroupLPCEOS"W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_newGenParticleList.root" \
$GroupLPCEOS"W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_newGenParticleList.root" \
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
$GGNtupleGroupEOSData"job_SingleMu_Run2016B_FebReminiAOD.root" \
$GGNtupleGroupEOSData"job_SingleMu_Run2016C_FebReminiAOD.root" \
$GGNtupleGroupEOSData"job_SingleMu_Run2016D_FebReminiAOD.root" \
$GGNtupleGroupEOSData"job_SingleMu_Run2016E_FebReminiAOD.root" \
$GGNtupleGroupEOSData"job_SingleMu_Run2016F_FebReminiAOD.root" \
$GGNtupleGroupEOSData"job_SingleMu_Run2016G_FebReminiAOD.root" \
$GGNtupleGroupEOSData"job_SingleMu_Run2016H_FebReminiAODv2.root "$GGNtupleGroupEOSData"job_SingleMu_Run2016H_FebReminiAODv3.root")





sampleType=("TTGamma_SingleLeptFromTbar" \
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
"ZGamma_01J_5f" \
"WGamma_01J_5f" \
"WW" \
"WZ" \
"ZZ") 
#"QCD_Pt20to30_Mu" \
#"QCD_Pt30to50_Mu" \
#"QCD_Pt50to80_Mu" \
#"QCD_Pt80to120_Mu" \
#"QCD_Pt120to170_Mu" \
#"QCD_Pt170to300_Mu" \
#"QCD_Pt300to470_Mu" \
#"QCD_Pt470to600_Mu" \
#"QCD_Pt600to800_Mu" \
#"QCD_Pt800to1000_Mu" \
#"QCD_Pt1000toInf_Mu" \
#"Data_SingleMu_b" \
#"Data_SingleMu_c" \
#"Data_SingleMu_d" \
#"Data_SingleMu_e" \
#"Data_SingleMu_f" \
#"Data_SingleMu_g" \
#"Data_SingleMu_h")



#echo "AnalysisNtuple/makeSkim dimu ${files[job]}skim.root ${inputfiles[job]}"
#AnalysisNtuple/makeSkim dimu ${files[job]}skim.root ${inputfiles[job]}

echo "AnalysisNtuple/makeAnalysisNtuple ${sampleType[job]}__Dilep . ${outputdir}skims/dimuons/V08_00_26_07/${files[job]}skim.root"
AnalysisNtuple/makeAnalysisNtuple ${sampleType[job]}__Dilep . ${outputdir}skims/dimuons/V08_00_26_07/${files[job]}skim.root


#echo "xrdcp -f ${files[job]}skim.root ${outputdir}skims/dimuons/V08_00_26_07/."
#xrdcp -f ${files[job]}skim.root ${outputdir}skims/dimuons/V08_00_26_07/.

echo "xrdcp -f Dilep_${files[job]}AnalysisNtuple.root ${outputdir}AnalysisNtuples_new/dimuons/V08_00_26_07/."
xrdcp -f Dilep_${files[job]}AnalysisNtuple.root ${outputdir}AnalysisNtuples_new/dimuons/V08_00_26_07/.


