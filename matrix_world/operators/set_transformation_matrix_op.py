import bpy
from matrix_world.operators.utility import get_transformation_matrix_from_editor

class SetTransformationMatrixOperator(bpy.types.Operator):
    bl_idname = "text.set_matrix_operator"
    bl_label = "Set Current Matrix as Transformation Matrix of Selected Object"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        mat = get_transformation_matrix_from_editor()
        context.active_object.matrix_world = mat
        
        return {'FINISHED'}
