def configureSimulation(sim):
    import CompuCellSetup
    from XMLUtils import ElementCC3D
    import NewSimulation_parameters as p
    
    CompuCell3DElmnt=ElementCC3D("CompuCell3D",{"Revision":"20180621","Version":"3.7.8"})
    PottsElmnt=CompuCell3DElmnt.ElementCC3D("Potts")
    PottsElmnt.ElementCC3D("Dimensions",{"x":"111","y":"111","z":"111"})
    PottsElmnt.ElementCC3D("Steps",{},p.mcs)
    PottsElmnt.ElementCC3D("Temperature",{},"20.0")
    PottsElmnt.ElementCC3D("NeighborOrder",{},"3")
    PluginElmnt=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"CellType"},"      !-- Listing all cell types in the simulation -->")
    PluginElmnt.ElementCC3D("CellType",{"TypeId":"0","TypeName":"Medium"})
    PluginElmnt.ElementCC3D("CellType",{"TypeId":"1","TypeName":"NPCells"})
    PluginElmnt.ElementCC3D("CellType",{"TypeId":"2","TypeName":"ACells"})
    PluginElmnt.ElementCC3D("CellType",{"Freeze":"","TypeId":"3","TypeName":"Wall"})
    PluginElmnt_1=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Volume"})
    PluginElmnt_1.ElementCC3D("VolumeEnergyParameters",{"CellType":"NPCells","LambdaVolume":"50.0","TargetVolume":"300"})
    PluginElmnt_1.ElementCC3D("VolumeEnergyParameters",{"CellType":"ACells","LambdaVolume":"50.0","TargetVolume":"300"})
    CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"CenterOfMass"})
    PluginElmnt_2=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Contact"},"       Specification of adhesion energies ")
    PluginElmnt_2.ElementCC3D("Energy",{"Type1":"Medium","Type2":"Medium"},"0.0")
    PluginElmnt_2.ElementCC3D("Energy",{"Type1":"Medium","Type2":"NPCells"},"5.0")
    PluginElmnt_2.ElementCC3D("Energy",{"Type1":"Medium","Type2":"ACells"},"5.0")
    PluginElmnt_2.ElementCC3D("Energy",{"Type1":"NPCells","Type2":"NPCells"},"5.0")
    PluginElmnt_2.ElementCC3D("Energy",{"Type1":"NPCells","Type2":"ACells"},p.AED)
    PluginElmnt_2.ElementCC3D("Energy",{"Type1":"ACells","Type2":"ACells"},"5.0")
    PluginElmnt_2.ElementCC3D("Energy",{"Type1":"Wall","Type2":"Wall"},"5.0")
    PluginElmnt_2.ElementCC3D("Energy",{"Type1":"Wall","Type2":"NPCells"},"5.0")
    PluginElmnt_2.ElementCC3D("Energy",{"Type1":"Wall","Type2":"ACells"},"5.0")
    PluginElmnt_2.ElementCC3D("NeighborOrder",{},"2")
	
	    
#   PluginElmnt_2a=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"CenterOfMass"})     # jps needed to get cell's center of mass
    PluginElmnt_2b=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"NeighborTracker"})  # jps needed to get cell's  neighbors
#   PluginElmnt_2c=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"PixelTracker"})     # jps Module tracking pixels of each cell
#   PluginElmnt_2d=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"BoundaryPixelTracker"})# jps Module tracking boundary pixels of each cell
#   PluginElmnt_2d.ElementCC3D("NeighborOrder",{},"1")
	
    PluginElmnt_3=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Chemotaxis"})
    ChemicalFieldElmnt=PluginElmnt_3.ElementCC3D("ChemicalField",{"Name":"Wnt9b","Source":"DiffusionSolverFE"})
    ChemicalFieldElmnt.ElementCC3D("ChemotaxisByType",{"Lambda":p.CL,"Type":"NPCells"})
    PluginElmnt_4=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Secretion"})
    FieldElmnt=PluginElmnt_4.ElementCC3D("Field",{"Name":"Wnt9b"})
    FieldElmnt.ElementCC3D("Secretion",{"Type":"Wall"},p.SR)
    FieldElmnt.ElementCC3D("Secretion",{"Type":"NPCells"},p.SR)
    SteppableElmnt=CompuCell3DElmnt.ElementCC3D("Steppable",{"Type":"DiffusionSolverFE"})
    DiffusionFieldElmnt=SteppableElmnt.ElementCC3D("DiffusionField",{"Name":"Wnt9b"})
    DiffusionDataElmnt=DiffusionFieldElmnt.ElementCC3D("DiffusionData")
    DiffusionDataElmnt.ElementCC3D("FieldName",{},"Wnt9b")
    DiffusionDataElmnt.ElementCC3D("GlobalDiffusionConstant",{},p.GDC)
    DiffusionDataElmnt.ElementCC3D("GlobalDecayConstant",{},p.decay)
    DiffusionDataElmnt.ElementCC3D("ExtraTimesPerMCS",{},"8")
    DiffusionDataElmnt.ElementCC3D("DoNotDiffuseTo",{},"Wall")
    SteppableElmnt_1=CompuCell3DElmnt.ElementCC3D("Steppable",{"Type":"PIFInitializer"})
    SteppableElmnt_1.ElementCC3D("PIFName",{},"Simulation/all cells uniform3d_v2.piff")

    CompuCellSetup.setSimulationXMLDescription(CompuCell3DElmnt)    
    
import sys
from os import environ
from os import getcwd
import string

sys.path.append(environ["PYTHON_MODULE_PATH"])

import CompuCellSetup

sim,simthread = CompuCellSetup.getCoreSimulationObjects()  

#remember to add this:
configureSimulation(sim)

# add extra attributes here           
CompuCellSetup.initializeSimulationObjects(sim,simthread)
# Definitions of additional Python-managed fields go here
        
#Add Python steppables here
steppableRegistry=CompuCellSetup.getSteppableRegistry()
        
from NewSimulationSteppables import ConstraintInitializerSteppable
ConstraintInitializerSteppableInstance=ConstraintInitializerSteppable(sim,_frequency=1)
steppableRegistry.registerSteppable(ConstraintInitializerSteppableInstance)
       
from NewSimulationSteppables import NewSimulationSteppable
NewSimulationSteppableInstance=NewSimulationSteppable(sim,_frequency=1)
steppableRegistry.registerSteppable(NewSimulationSteppableInstance)        
       
CompuCellSetup.mainLoop(sim,simthread,steppableRegistry)
