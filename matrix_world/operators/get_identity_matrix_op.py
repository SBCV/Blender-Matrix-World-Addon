import numpy as np
import bpy
from matrix_world.operators.utility import set_transformation_matrix_to_editor

class GetIdentityMatrixOperator(bpy.types.Operator):
    bl_idname = "text.get_identity_matrix_operator"
    bl_label = "Get Identity Matrix"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        matrix_world = np.identity(4, dtype=float)
        set_transformation_matrix_to_editor(matrix_world)
        return {'FINISHED'}
