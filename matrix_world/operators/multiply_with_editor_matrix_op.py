import bpy
from matrix_world.operators.utility import (
    get_transformation_matrix_from_editor,
    set_transformation_matrix_to_editor,
)

class MultiplyWithEditorMatrixOperator(bpy.types.Operator):
    bl_idname = "text.multiply_with_editor_matrix_operator"
    bl_label = "Multiply Transformation Matrix of Object With Editor Matrix"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        transformation_matrix = context.active_object.matrix_world
        multiply_matrix = get_transformation_matrix_from_editor()
        result = multiply_matrix @ transformation_matrix 				# apply the new matrix (multiplication from left side) 
        set_transformation_matrix_to_editor(result)

        return {'FINISHED'}
