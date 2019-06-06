import FWCore.ParameterSet.Config as cms

# link to card:
# https://github.com/cms-sw/genproductions/blob/master/bin/Powheg/production/2017/13TeV/VBF_H_NNPDF31_13TeV/VBF_H_NNPDF31_13TeV_template.input

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/VBF_H_NNPDF31_13TeV_M125/v1/VBF_H_NNPDF31_13TeV_M125_slc6_amd64_gcc630_CMSSW_9_3_0.tgz'),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)

import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.Pythia8PowhegEmissionVetoSettings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
                         maxEventsToPrint = cms.untracked.int32(1),
                         pythiaPylistVerbosity = cms.untracked.int32(1),
                         filterEfficiency = cms.untracked.double(1.0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(13000.),
                         PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PowhegEmissionVetoSettingsBlock,      
        processParameters = cms.vstring(
            'POWHEG:nFinal = 3',
            '25:onMode = off', # turn OFF all H decays
            '25:onIfMatch = 15 -15', # turn ON H->tautau      
            '25:m0 = 125.0'
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'pythia8PowhegEmissionVetoSettings',
                                    'processParameters'
                                    )
        )
                         )

myGenerator = cms.EDProducer("GenParticles2HepMCConverter",
   genParticles = cms.InputTag("genParticles"),
   genEventInfo = cms.InputTag("generator"),
   signalParticlePdgIds = cms.vint32(25),
)

rivetProducerHTXS = cms.EDProducer('HTXSRivetProducer',
  HepMCCollection = cms.InputTag('myGenerator','unsmeared'),
  LHERunInfo = cms.InputTag('externalLHEProducer'),
  ProductionMode = cms.string('AUTO'),
)

HTXSFilter = cms.EDFilter("HTXSFilter",
    htxs_flags = cms.untracked.vint32(206),
)

filter_step = cms.Path(myGenerator*rivetProducerHTXS*HTXSFilter)

