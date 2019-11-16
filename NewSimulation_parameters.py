# File: NewSimulation_paramters.py
# Date: 7.9.2018
# Created By: Pauli Tikka
# Comments: These are the base parameters
#
# Parameters:  these are NOT expected to change during the simulation

# Randomize the cell types after loading the PIF file, 0=No, 1=Yes
randomizeCells=1

# Number of MCS steps to do (jps)
mcs=1001  # 1001 use 11 for testing

#Adhesion Energy Difference (AED) between NPCells and ACells
AED=13

#Chemotaxis Lambda (CL)
CL=100

#Secretion Rate (SR) of Chemotacting Substance 
SR=3

#GlobalDiffusionConstant (GDC)
GDC=1

#GlobalDecayConstant (just decay)
decay=0.0000001