from PySteppables import *
import CompuCell
import CompuCellSetup
import sys
import random
import numpy as nps
from math import *
from XMLUtils import dictionaryToMapStrStr as d2mss
from PySteppablesExamples import MitosisSteppableBase
import NewSimulation_parameters as p

class ConstraintInitializerSteppable(SteppableBasePy):
    def __init__(self,_simulator,_frequency=1):
        SteppableBasePy.__init__(self,_simulator,_frequency)
    def start(self):
        NPCell_count = 0
        ACell_count  = 0
        for cell in self.cellList: 
            cell.targetVolume=375
            cell.lambdaVolume=20
            #speculation about the amount of lambdaVolume:
            #62.5too high?? --> yes, we want to give emphasize on sorting&chemot
            #20 ok for ub models, but around 40 for np models???
            cell.targetSurface=312
           #the amount of TargetSurface, comes with the form: 
            # (5+1)*375^(2/3) = 312(;390) ->260m maybe -2,5 or -1better ??
#          #higher for np model?? e.g. 350, 260 ok for ub model
            cell.lambdaSurface=0.1 
            #speculation about the amount of lambdaSurface:
            #400/15~27 ->30 , in as per 30/2, 30 too much?? ->3 better, 0.1 yes
            #this should be less for np models, e.g. 0.001; 0.1 ok for ub models, but let it be this..
            #no surface targets for NP models??, creates too much of an tail??
            if cell.type == 1:
                NPCell_count +=1
            elif cell.type == 2:
                ACell_count += 1
        # jps: randomly reassign the cell types (NP and A cells) to give a random starting 
        # configuration, make sure though that the total number of NP cells stays the same
        #     controlled by a parameter in the parameters file
        if p.randomizeCells == 1:  # 1=yes, 0=no
            print "\n\nRandomizing cell types.\nNumber of NPCell and ACell intitally =",NPCell_count,ACell_count
            for cell in self.cellListByType(self.NPCELLS, self.ACELLS):  
                if random.random() < float(NPCell_count)/(NPCell_count+ACell_count):
                    cell.type = self.NPCELLS
                    NPCell_count -= 1
                else:
                    cell.type = self.ACELLS    
                    ACell_count -= 1
            print "After reassignment, NPCell and ACell counters:",NPCell_count,ACell_count
            for cell in self.cellListByType(self.NPCELLS, self.ACELLS):  
                if cell.type == self.NPCELLS:
                    NPCell_count += 1
                elif cell.type == self.ACELLS:
                    ACell_count += 1
            print "Double check reassignment, NPCell and ACell counters:",NPCell_count,ACell_count,"\n\n"

class NewSimulationSteppable(SteppableBasePy):
    def __init__(self,_simulator,_frequency=1):
        SteppableBasePy.__init__(self,_simulator,_frequency)
        
    def start(self):
        # atually better to put directly to the analysis folder:
        FileName2 = "distances.csv"

        self.File2,self.fullFileName2=self.openFileInSimulationOutputDirectory(FileName2,"w")  # jps

        #self.File.write("cell_no,time_mcs,x_position_(px),y_position_(px),z_position_(px)\n")
        self.File2.write("cell_no,time_mcs,cell_dist_to_corner,cell_dist_to_tip,x_position_(px),y_position_(px),\
        z_position_(px),cell_field, field_mean\n")

    def step(self,mcs):
         # jps only do this every 10 MCS
        if mcs % 10 == 0:
            field=self.getConcentrationField("Wnt9b")
    #       to get the global mean one needs extra coding; for individual mean: meanValue = np.mean(field[55,55,0])
           
            averVol = 0.0
            numberOfCells = 0
            meanValue =[]
            
            for i in range(110):
                for j in range(110):
                   for k in range (110):
                       meanValue.append(field[i,j,k])

            meanValue_mcs=np.mean(meanValue)
#             meanValuexx=np.mean(meanValuex)
            
#             speed=[]
            
            for cell in self.cellListByType(self.NPCELLS,self.ACELLS): #distances to the static uretic bud is irrelevant
                self.File2.write(str(cell.id)+","+str(mcs)+","+str(self.distance(_from=[20, 40, 50],\
                _to=[cell.xCOM,cell.yCOM,cell.zCOM]))+","+str(self.distance(_from=[40, 50, 50],\
                _to=[cell.xCOM,cell.yCOM,cell.zCOM]))+","+str(cell.xCOM)+","+str(cell.yCOM)+","+str(cell.zCOM)\
                +","+str(field[int(cell.xCOM),int(cell.yCOM),int(cell.zCOM)])+","+str(meanValue_mcs)+"\n")
        if mcs == p.mcs-1:  # do this on the last mcs (maxMCS -1) step (ugly fix for "finish" not working)
            self.File2.close()
            
    def finish(self):
        # apparently also this closing is needed for \
        # getting the total files, in order to 'flush' them from memory buffer or etc.
        self.File2.close()
      #  pass

# class QualityCalc(SteppableBasePy):  # jps
#     # Finish function gets called after the last MCS.
#     # Calculate how good this particular simulation + parameter set was 
#     # and output the quality measure to a file for use by the swarm code
#     def __init__(self,_simulator,_frequency=1):
#         SteppableBasePy.__init__(self,_simulator,_frequency)
        
#     def start(self):
#         # try to open the output file, do it here so if it fails we don't do 
#         # the entire simulation only to have this open fail at the very end.
#         qualFileName="Quality_data.txt"
#         try:                
#             self.fileHandle0,self.fullFileName0=self.openFileInSimulationOutputDirectory("Quality_data.txt","w")
#         except IOError:
#             print "Could not open file for writing the Quality data. "    
#             print qualFileName," in the SimulationOutputDirectory."
#             print fileHandle0,fullFileName0,"\n"
#             self.stopSimulation()
     
#     def step(self,mcs):
#         if mcs == p.mcs-1:  # do this on the last mcs (maxMCS -1) step (ugly fix for "finish" not working)
#             print "\n\nQuality calculation at mcs=",mcs 
#             # Quality is the sum of the contact area between NPCells and Wall
#             # to get the cell's neighbors we need the NeighborTracker plugin            
#             theQuality=0 
#             #for cell in self.cellList:
#             for cell in self.cellListByType(self.NPCELLS):  
#                 neighborList = self.getCellNeighborDataList(cell)
#                 for neighbor, commonSurfaceArea in neighborList:
#                     if neighbor:  # makes sure the neighbor isn't medium
#                         if neighbor.type == self.WALL:  # Wall type = 3
#                             theQuality += commonSurfaceArea 
#             # swarm does a minization but we want to maximize this value, so make it negative
#             theQuality = -theQuality
#             print "theQuality=",theQuality,"\n\n"
#             self.fileHandle0.write(str(theQuality))
#             self.fileHandle0.close()
#         #pass
        
#     def finish(self):   # NOT WORKING
#         pass