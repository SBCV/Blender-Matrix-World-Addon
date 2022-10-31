# Blender-Matrix-World-Addon
This Blender add-on allows to set and apply matrix world transformations to objects using Blender's GUI

## Overview
The matrix is stored inside Blender's text editor (which can be used to edit the matrix)

Functionality
- Loading Matrices
- Storing Matrices
- Getting transformation matrix of selected object
- Getting camera matrix of selected camera 
- Inverting the editor matrix 
- Multiplying editor matrix with transformation matrix of selected object (allows to combine transformations)
- Setting the matrix in the editor to the selected object


## Installation
Option 1:
Download the zip file (Blender-Matrix-World-Addon-master.zip) and install it using Blender's "Install Add-on from File..." option.   


Option 2:
Clone the add-on with 
```
git clone https://github.com/SBCV/Blender-Matrix-World-Addon.git
```
and compress the folder to "Blender-Matrix-World-Addon" to a zip archive. 
The final structure must look as follows:
- Blender-Matrix-World-Addon.zip /  
	- Blender-Matrix-World-Addon/
		- \_\_init\_\_.py
		
Use Blender's "Install Add-on from File..." option to install the add-on.

## Menu Overview
![alt text](https://github.com/SBCV/Blender-Matrix-World-Addon/blob/master/images/menu_annotations.JPG)
