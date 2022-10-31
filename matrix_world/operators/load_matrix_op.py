import os
import numpy as np
import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from matrix_world.operators.utility import set_transformation_matrix_to_editor


class LoadMatrixOperator(bpy.types.Operator, ImportHelper):
    bl_idname = "text.load_matrix_operator"
    bl_label = "Load Matrix from Disc (.npy, .txt)"
    
    filter_glob : StringProperty(
        default="*.npy;*.txt",
        options={'HIDDEN'},
        )
    
    @classmethod
    def poll(cls, context): 
        return True

    def execute(self, context):
        self.report({'INFO'}, 'Input File Path: ' + str(self.filepath))
        if os.path.splitext(self.filepath)[1] == '.npy':
            mat = np.load(self.filepath)
        elif os.path.splitext(self.filepath)[1] == '.txt':
            mat = np.loadtxt(self.filepath)
        else:
            return {'FINISHED'}
        set_transformation_matrix_to_editor(mat)
        return {'FINISHED'}
