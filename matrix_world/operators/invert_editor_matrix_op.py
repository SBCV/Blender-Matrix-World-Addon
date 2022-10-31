import bpy
from matrix_world.operators.utility import (
    get_transformation_matrix_from_editor,
    set_transformation_matrix_to_editor,
)


class InvertEditorMatrixOperator(bpy.types.Operator):
    bl_idname = "text.invert_editor_matrix_operator"
    bl_label = "Invert Editor Matrix"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        transformation_matrix = get_transformation_matrix_from_editor()
        inverse = transformation_matrix.inverted()
        set_transformation_matrix_to_editor(inverse)
        return {"FINISHED"}
