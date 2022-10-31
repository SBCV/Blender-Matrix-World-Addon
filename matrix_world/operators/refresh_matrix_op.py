import bpy


class RefreshMatrixOperator(bpy.types.Operator):
    bl_idname = "text.refresh_matrix_operator"
    bl_label = "Refresh Editor Matrix after Editing"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        return {"FINISHED"}
