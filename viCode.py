# Python program to read the reports from a json file from VI db and make plots

import json
import sys
import os
import ast
from urllib.request import urlopen
import urllib.request
from requests.auth import HTTPBasicAuth
import matplotlib.pyplot as plt
import numpy as np
import csv
import re
from matplotlib import interactive


class viAnalysis:

    def __init__(self, hybridtype):
    
        self.hybridtype  = hybridtype
        
    def AccessJSON(self, inputJson):
    
        freports    = open(inputJson, "r")
        jsonContent = freports.read()
        data        = json.loads(jsonContent)
        
        return data
    
    def fillNInspector(self):
    
        data = self.AccessJSON("reports_202304171045.json")
    
        NInspected = []
        NAccepted  = []
        Inspector  = ["Alan","Alessandro","Imtiaz", "Mohsin", "Mojtaba"]
        AcceptedPercent = []
        n_imtiaz = 0
        n_mohsin = 0
        n_alan = 0
        n_mojtaba = 0
        n_rosa    = 0

        n_imtiaz_acc = 0
        n_mohsin_acc = 0
        n_alan_acc = 0
        n_mojtaba_acc = 0
        n_rosa_acc = 0
    
        nTotalHyb = 0
    
        for rr in data['reports']:

            typehb = rr['serial_number']

            if typehb[:5] == self.hybridtype:
                nTotalHyb+=1

                if rr['name'] == "Imtiaz Ahmed":
                    n_imtiaz+=1
                    if(rr['hybrid_status'] == "Accepted"):
                        n_imtiaz_acc+=1
                if rr['name'] == "Mohsin Abbas" :
                    n_mohsin+=1
                    if(rr['hybrid_status'] == "Accepted"):
                        n_mohsin_acc+=1
                if rr['name'] == "Alan Honma":
                    n_alan+=1
                    if(rr['hybrid_status'] == "Accepted"):
                        n_alan_acc+=1
 
                if rr['name'] == "Alessandro La Rosa":
                    n_rosa+=1
                    if(rr['hybrid_status'] == "Accepted"):
                        n_rosa_acc+=1
                
                if rr['name'] == "Mojtaba Mohammadi Najafabadi":
                    n_mojtaba+=1
                    if(rr['hybrid_status'] == "Accepted"):
                        n_mojtaba_acc+=1

        if n_imtiaz > 0:
            acc_frac_imtiaz = n_imtiaz_acc/n_imtiaz
        else:
            acc_frac_imtiaz = 0
        if n_mohsin > 0:
            acc_frac_mohsin = n_mohsin_acc/n_mohsin
        else:
            acc_frac_mohsin = 0
        if n_alan > 0:
            acc_frac_alan = n_alan_acc/n_alan
        else:
            acc_frac_alan = 0
        if n_rosa > 0:
            acc_frac_rosa = n_rosa_acc/n_rosa
        else:
            acc_frac_rosa = 0
        if n_mojtaba > 0:
            acc_frac_mojtaba = n_mojtaba_acc/n_mojtaba
        else:
            acc_frac_mojtaba = 0

        NInspected = [n_alan,n_rosa,n_imtiaz,n_mohsin,n_mojtaba]
        NAccepted  = [n_alan_acc,n_rosa_acc,n_imtiaz_acc,n_mohsin_acc,n_mojtaba_acc]
        AcceptedPercent = [acc_frac_alan,acc_frac_rosa,acc_frac_imtiaz,acc_frac_mohsin,acc_frac_mojtaba]

        return Inspector, NInspected, NAccepted, AcceptedPercent
    
    def fillParameters(self):
    
        data = self.AccessJSON("reports_202304171045.json")

        nTotal = 0
        nAcc4Production = 0
        nAcc4Prototype = 0
        nAcc = 0
        nBC_acc = 0
        nSolderingQuality_acc = 0
        nAlignment_acc = 0
        nAdhesiveFlexCF_acc = 0
        nAdhesiveCFComp_acc = 0
        nComp2Comp_acc = 0
        nCleanlinessCircuit_acc = 0
        nDamageFlex_acc = 0
        nGlobalFlatness_acc = 0
        nUnderFill_acc = 0
        nFoldOverAccuracy_acc = 0
        nCleanlinessBP_acc = 0
        nLocalFlatnessFlex_acc = 0


        for rr in data['reports']:
    
            typehb = rr['serial_number']
            if typehb[:5] == self.hybridtype:
                nTotal+=1

            if rr['module_usability'] == "Accepted":
                nAcc4Production+=1
            if rr['prototype_usability'] == "Accepted":
                nAcc4Prototype+=1
            if rr['hybrid_status'] == "Accepted":
                nAcc+=1

            parameters_with_removed_escape_chars = json.loads(rr["parameters"]) 
            parameters_in_dict_format = json.loads(parameters_with_removed_escape_chars) 

       
            for ikey, ival in parameters_in_dict_format.items():
               # print(ikey,":" ,ival[0])

                if (ikey == "Barcode" or ikey == "Barcode OK?") and ival[0] == "ACCEPTED":
                    nBC_acc+=1
                if ikey == 'Component soldering quality and correctness' and ival[0] == "ACCEPTED":
                    nSolderingQuality_acc+=1
                if ikey == 'Alignment of components' and ival[0] == "ACCEPTED":
                    nAlignment_acc+=1   
                if ikey == 'Adhesive aspect of flex to CF stiffener' and ival[0] == "ACCEPTED":
                    nAdhesiveFlexCF_acc+=1   
                if ikey == 'Adhesive aspect of CF stiffener to compensator' and ival[0] == "ACCEPTED":
                    nAdhesiveCFComp_acc+=1   
                if ikey == 'Adhesive aspect of compensator to compensator (1.8mm variant) or compensator to Al-N spacer (4.0mm variant)' and ival[0] == "ACCEPTED":
                    nComp2Comp_acc+=1   
                if ikey == 'Cleanliness of circuit, esp. connectors' and ival[0] == "ACCEPTED":
                    nCleanlinessCircuit_acc+=1   
                if ikey == 'Damage to flex, stiffeners, compensators or ASICs' and ival[0] == "ACCEPTED":
                    nDamageFlex_acc+=1   
                if ikey == 'Global flatness of hybrid (bow)' and ival[0] == "ACCEPTED":
                    nGlobalFlatness_acc+=1   
                if ikey == 'Underfill quality' and ival[0] == "ACCEPTED":
                    nUnderFill_acc+=1   
                if ikey == 'Fold-over accuracy' and ival[0] == "ACCEPTED":
                    nFoldOverAccuracy_acc+=1   
                if ikey == 'Cleanliness and quality of bond pads' and ival[0] == "ACCEPTED":
                    nCleanlinessBP_acc+=1   
                if ikey == 'Local flatness of flex' and ival[0] == "ACCEPTED":
                    nLocalFlatnessFlex_acc+=1   

        parameters_names = ['Total', 'HybridOK','Accepted4Prototype','Accepted4Production','Barcode','Soldering quality','Alignment of components','AdhesiveFlex2CF']
        ValuesParams=[nTotal,nAcc,nAcc4Prototype,nAcc4Production,nBC_acc,nSolderingQuality_acc,nAlignment_acc,nAdhesiveFlexCF_acc]
    
        return parameters_names, ValuesParams
    
    def plotNInspectors(self):
    
        Inspector, NInspected, NAccepted, AcceptedPercent = self.fillNInspector()
    
        width = 0.4       # the width of the bars
#        fig1 = plt.figure(1)
        plt.figure(figsize=(9, 6))
    
        plt.bar( Inspector, NInspected, width,label="Total Number")
        plt.bar( Inspector, NAccepted, width, label="Accepted Number")
        
        plt.text("Alan", 10, "{:.0%}".format(AcceptedPercent[0],".2f"), fontsize=10)
        plt.text("Alessandro", 10, "{:.0%}".format(AcceptedPercent[1],".2f"), fontsize=10)
        plt.text("Imtiaz", 10, "{:.0%}".format(AcceptedPercent[2],".2f"), fontsize=10)
        plt.text("Mohsin", 10, "{:.0%}".format(AcceptedPercent[3],".2f"), fontsize=10)
        plt.text("Mojtaba", 10, "{:.0%}".format(AcceptedPercent[4],".2f"), fontsize=10)
        plt.legend(loc="upper left")
        
        plt.suptitle('Number of Inspected Hybrids')
        outplot = "Number_Inspector_"+self.hybridtype+".pdf"
        plt.savefig(outplot)

        plt.show()
 #       plt.close(fig1)
        

    def plotParameters(self):
    
        parameters_hybrid, ValuesParam_hybrid = self.fillParameters()
 #   fig2 = plt.figure(2)
        width = 0.4

        plt.bar( parameters_hybrid, ValuesParam_hybrid, width,label="Parameter Info")
        plt.xticks(parameters_hybrid, parameters_hybrid, rotation =30, fontsize=6)
        
        outputplot = "parameters_"+self.hybridtype+".pdf"
        plt.savefig(outputplot)

        plt.show()
#    plt.close(fig2)



p1 = viAnalysis("2SFEH")
p1.fillNInspector()
p1.fillParameters()
p1.plotNInspectors()
p1.plotParameters()
del p1

p2 = viAnalysis("PSFEH")
p2.fillNInspector()
p2.fillParameters()
p2.plotNInspectors()
p2.plotParameters()
del p2

