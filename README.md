# topas-merge-simulations

## Python script to combine the statistical results of a TOPAS simulation that was split up into multiple batches

## At the top of the script, specify:

<img src="https://user-images.githubusercontent.com/87897942/147073837-7a2aff53-27af-454d-a530-6531a9c13001.png" width=426 height=279>

- the name of the output file
- the input files in a list
- the number of histories used for each file (in order)

### Assumes a ".csv" input file format from a TOPAS Scorer with the following header format:



\# TOPAS Version: {...}  
\# Parameter File: {...}.txt  
\# Results for scorer {...}  
\# Scored in component: {...}  
\# X in {...} bin of {...} cm  
\# Y in 1 {...} of {...} cm  
\# Z in {...} bins of {...} cm  
\# DoseToMedium ( Gy ) : {Sum/Mean}   Standard_Deviation     
Voxel Coordinate X, Voxel Coordinate Y, Voxel Coordinate Z, {Sum/Mean} Value, Standard_Deviation Value   
                 .   
                 .   
                 .   
  
  
Works using Python3, but written without any external dependencies. 
