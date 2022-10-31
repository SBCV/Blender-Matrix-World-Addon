import bpy
from matrix_world.operators.utility import set_transformation_matrix_to_editor

class GetTransformationMatrixOperator(bpy.types.Operator):
    bl_idname = "text.get_matrix_operator"
    bl_label = "Get Transformation Matrix from Selected Object"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        matrix_world = context.active_object.matrix_world
        set_transformation_matrix_to_editor(matrix_world)

        return {'FINISHED'}
