import ROOT
from ROOT import kBlack,kWhite,kGray,kRed,kPink,kMagenta,kViolet,kBlue,kAzure,kCyan,kTeal,kGreen,kSpring,kYellow,kOrange,kDashed,kSolid,kDotted
from ROOT import gSystem, gROOT, TCanvas, TGraphErrors, TF1, gStyle, kRed, kBlue, kGray, TFile, TTree, TPad, gPad, TLorentzVector
import math
from array import array
from math import sqrt
import numpy as np
import re
from os.path import exists
from optparse import OptionParser


parser = OptionParser()
parser.add_option('--model', help='model: ALP-W, ALP-photon', type=str, default="ALP-W")
(options, args) = parser.parse_args()

modelname = options.model


path = "/home/findjake/code/photon_identification_FASER/data/signal_test/post-bdt/"

if modelname == "ALP-W":
    masses = np.logspace(-1.5,0.3,15)
    couplings = np.logspace(-7,-2,21)
elif modelname == "ALP-photon":
    masses = np.logspace(-2,-0.3,20+1)
    couplings = np.logspace(-6,-2,17) 
#elif modelname == "UpPhilic":
#    masses = np.logspace(-2,-0.3,18)
#    couplings = np.logspace(-10,-2,17)
elif modelname == "UpPhilic":
    masses = np.logspace(-1,-0.3,23)
    couplings = np.logspace(-10,-2,17)
elif modelname == "U1B":
    masses = np.logspace(-1,0,21)
    couplings = np.logspace(-8,-2,19)
else:
    print('Model not found')



selection = "(bdt_score > 0.9)*"

bins = 1
xmin = 0
xmax = 1e12

# fill the file array with the names of the files
signal_yields = []
for mass in masses:
    # integer_part, decimal_part = str(mass).split(".") # works for ALP-W
    integer_part, decimal_part = str(round(mass,3)).split(".")
    smass = integer_part + "p" + decimal_part
    signal_yields_tmp = []
    for icoup,coup in enumerate(couplings):
        scoup_tmp = '{:5.1e}'.format(coup)
        integer, decimal = str(scoup_tmp).split(".")
        scoup = integer + "p" + decimal
        fileName = modelname+"_m"+smass+"_eps"+scoup
        print(fileName+".root")
        
        # now we also want to find the weight associated with this sample. It is stored in the hepMC file
        # read the hepMC file and extract the weight
        # Open the file and read its contents
        file_exists = exists('/home/findjake/code/photon_identification_FASER/data/hepmc/'+modelname+'/'+fileName+'.hepmc')
        if not file_exists:
            # append a 0 yield to this sample if it does not exist
            signal_yields_tmp.append(0)
            continue
        with open('/home/findjake/code/photon_identification_FASER/data/hepmc/'+modelname+'/'+fileName+'.hepmc', 'r') as file:
            contents = file.read()
        
        # Use regular expressions to find the number after 'C'
        pattern = r'C (\S+)'
        match = re.search(pattern, contents)

        # Check if a match is found and extract the number
        if match:
            weight = float(match.group(1))
            #print('weight',weight)
        else:
            print("No match found.")

        # We already have the weight and the sample, not we just have to apply the signal selection on count events
        file_exists = exists(path+"faser_1_"+fileName+"_bdt.root")
        # append 0 yield to this sample if it does not exist
        if not file_exists:
            signal_yields_tmp.append(0)
            continue
        f = ROOT.TFile(path+"faser_1_"+fileName+"_bdt.root","READ")
        eventTree = f.Get("myTree")
        histo= ROOT.TH1F("histo"+str(icoup), "histo"+str(icoup), bins, xmin ,xmax)
        # apply selection and weight
        eventTree.Draw("1 >> histo"+str(icoup),selection+str(weight),"")
        yields=histo.Integral()
        print('yields',yields)
        signal_yields_tmp.append(yields)

    
    # save for each mass an array of all the signal yields for each coupling
    # we do it this way so we can use directly Felix's scripts to plot the reach
    signal_yields.append(signal_yields_tmp)
    #signal_yields = np.array(signal_yields_tmp, dtype=object)


#np.save("results/"+modelname+"_yields.npy",[masses,couplings,signal_yields])
#np.save(modelname+"_cutyields.npy",[masses,couplings,signal_yields])
np.save(modelname + "_cutyields_bdt.npy", np.array([masses, couplings, signal_yields], dtype=object))


