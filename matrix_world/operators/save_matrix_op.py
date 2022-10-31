import os
import numpy as np
import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty
from matrix_world.operators.utility import (
    get_transformation_matrix_from_editor,
)


class SaveMatrixOperator(bpy.types.Operator, ExportHelper):
    bl_idname = "text.save_matrix_operator"
    bl_label = "Save Current Matrix to Disc (.npy, .txt)"

    filename_ext: StringProperty(default=".txt")

    @classmethod
    def poll(cls, context):
        # return context.active_object is not None
        return True

    def execute(self, context):
        self.report({"INFO"}, "Output File Path: " + str(self.filepath))
        mat = get_transformation_matrix_from_editor()
        mat_np = np.array(mat)
        with open(self.filepath, "wb") as f:
            if os.path.splitext(self.filepath)[1] == ".npy":
                np.save(f, mat_np)
            elif os.path.splitext(self.filepath)[1] == ".txt":
                np.savetxt(f, mat_np)

        return {"FINISHED"}
