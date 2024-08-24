import ROOT
import numpy as np
import xgboost as xgb
import pandas as pd
from array import array


masses = np.logspace(-1.5,0.3,15)
couplings = np.logspace(-7,-2,21)


modelname = "ALP-W"
#path="/eos/project/f/faser-preshower/simulations/analysis/"+modelname+"/"
path="/home/sabaterj/code/faser/photon-reco-py/scripts/discriminating_variables/output/signal/"
for mass in masses:
    # integer_part, decimal_part = str(mass).split(".") # works for ALP-W
    integer_part, decimal_part = str(round(mass,3)).split(".")
    smass = integer_part + "p" + decimal_part
    signal_yields_tmp = []
    for icoup,coup in enumerate(couplings):
        scoup_tmp = '{:5.1e}'.format(coup)
        integer, decimal = str(scoup_tmp).split(".")
        scoup = integer + "p" + decimal
        file_name = "faser_1_"+modelname+"_m"+smass+"_eps"+scoup

        print('Opening',file_name)
        # Open the original ROOT file
        input_file = ROOT.TFile.Open(path+file_name+".root", "READ")
        tree = input_file.Get("myTree")

        # Load the trained XGBoost model
        model = xgb.XGBClassifier()
        model.load_model("model.json")

        # Create a new ROOT file and clone the original TTree
        output_file = ROOT.TFile("output/"+file_name+"_bdt.root", "RECREATE")
        new_tree = tree.CloneTree(0)  # Clone the tree structure, but not the content

        # Create a new branch for the prediction scores
        #bdt_score = np.zeros(1, dtype=float)
        bdt_score = array('f', [0])
        branch = new_tree.Branch("bdt_score", bdt_score, "bdt_score/F")

        # Get the list of branches (variables) in the TTree
        #branches = [branch.GetName() for branch in tree.GetListOfBranches()]
        branches = ["n_hits","qdmax","n_layers"]

        # Loop over the entries, calculate the prediction scores, and fill the new tree
        for entry in range(tree.GetEntries()):
            tree.GetEntry(entry)

            # Prepare the data for prediction
            #data = np.array([[getattr(tree, branch) for branch in branches]])
            data = [getattr(tree, v) for v in branches]
            # Get the prediction probabilities
            prediction = model.predict_proba([data])[0][1]
            
            # Assuming binary classification, take the probability for the positive class
            bdt_score[0] = prediction
            # Fill the new tree with the current entry and the prediction score
            new_tree.Fill()

        # Write the updated TTree into the new file and close both files
        new_tree.Write()
        output_file.Close()
        input_file.Close()
