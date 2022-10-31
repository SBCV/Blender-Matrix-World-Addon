import bpy
from bpy.props import BoolProperty


from matrix_world.operators.get_identity_matrix_op import (
    GetIdentityMatrixOperator
)
from matrix_world.operators.get_transformation_matrix_op import (
    GetTransformationMatrixOperator
)
from matrix_world.operators.get_calibration_matrix_op import (
    GetCalibrationMatrixOperator
)
from matrix_world.operators.refresh_matrix_op import (
    RefreshMatrixOperator
)
from matrix_world.operators.invert_editor_matrix_op import (
    InvertEditorMatrixOperator
)
from matrix_world.operators.multiply_with_editor_matrix_op import (
     MultiplyWithEditorMatrixOperator
)
from matrix_world.operators.set_transformation_matrix_op import (
     SetTransformationMatrixOperator
)
from matrix_world.operators.load_matrix_op import (
     LoadMatrixOperator
)
from matrix_world.operators.save_matrix_op import (
     SaveMatrixOperator
)


bl_info = {
    "name": "Matrix World",
    "description": "Allows to work directly with Matrix World in the GUI",
    "author": "Sebastian Bullinger",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "View3D",
    "wiki_url": "",
    "category": "Object" }


class TransformationMatrixPanel(bpy.types.Panel):
    bl_label = "Matrix World"
    bl_idname = "OBJECT_PT_Transf"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    # bl_space_type = "PROPERTIES"
    # bl_region_type = "WINDOW"
    # bl_context = "object"

    textblock = None # text area to use for this panel

    @classmethod
    def poll(cls,context):
        return True

    def draw(self, context):
        layout = self.layout

        textblock = bpy.data.texts.get("TransformationMatrix")
        if textblock is None:
            self.textblock = bpy.data.texts.new("TransformationMatrix")

        obj = context.object

        textbox = bpy.data.texts.get("TransformationMatrix")
        row = layout.row()
        if obj is not None:
            obj_name = obj.name
        else:
            obj_name = 'NONE selected'
        row.label(text="Selected object is: " + obj_name)
        get_group_box = layout.box()
        row = get_group_box.row()
        row.operator("text.get_identity_matrix_operator")
        row = get_group_box.row()
        row.operator("text.get_matrix_operator")
        row = get_group_box.row()
        row.operator("text.get_calibration_matrix_operator")

        matrix_group_box = layout.box()
        row = matrix_group_box.row()
        row.label(text="Current Editor Matrix: ")
        row.operator("text.refresh_matrix_operator")
        matrix_box = matrix_group_box.box()
        for line in textbox.lines:
            row = matrix_box.row()
            row.label(text=line.body)

        edit_group = layout.box()
        row = edit_group.row()
        row.operator("text.invert_editor_matrix_operator")
        row = edit_group.row()
        row.operator("text.multiply_with_editor_matrix_operator")

        set_group = layout.box()
        row = set_group.row()
        row.operator("text.set_matrix_operator")

        load_save_group = layout.box()
        row = load_save_group.row()
        row.operator("text.load_matrix_operator")
        row = load_save_group.row()
        row.operator("text.save_matrix_operator")

        box = layout.box()
        box.prop(textbox, "open_in_info_window", text="Show Editor in Info Panel")


def openInInfoWin(self,context):
    if self.open_in_info_window:
        for area in context.screen.areas:
            if area.type == 'INFO':
                area.type = 'TEXT_EDITOR'
                area.spaces[0].text = TransformationMatrixPanel.textblock
                break
    else:
        for area in context.screen.areas:
            if area.type == 'TEXT_EDITOR':
                area.type = 'INFO'
                break
        return None

def register():
    bpy.types.Text.open_in_info_window = bpy.props.BoolProperty(
        "Open in INFO window", default=False, update=openInInfoWin
    )
    bpy.utils.register_class(LoadMatrixOperator)
    bpy.utils.register_class(TransformationMatrixPanel)
    bpy.utils.register_class(GetIdentityMatrixOperator)
    bpy.utils.register_class(GetTransformationMatrixOperator)
    bpy.utils.register_class(GetCalibrationMatrixOperator)
    bpy.utils.register_class(RefreshMatrixOperator)
    bpy.utils.register_class(InvertEditorMatrixOperator)
    bpy.utils.register_class(MultiplyWithEditorMatrixOperator)
    bpy.utils.register_class(SetTransformationMatrixOperator)
    bpy.utils.register_class(SaveMatrixOperator)
    

def unregister():
    bpy.utils.unregister_class(LoadMatrixOperator)
    bpy.utils.unregister_class(TransformationMatrixPanel)
    bpy.utils.unregister_class(GetIdentityMatrixOperator)
    bpy.utils.unregister_class(GetTransformationMatrixOperator)
    bpy.utils.unregister_class(GetCalibrationMatrixOperator)
    bpy.utils.unregister_class(RefreshMatrixOperator)
    bpy.utils.unregister_class(InvertEditorMatrixOperator)
    bpy.utils.unregister_class(MultiplyWithEditorMatrixOperator)
    bpy.utils.unregister_class(SetTransformationMatrixOperator)
    bpy.utils.unregister_class(SaveMatrixOperator)
    

if __name__ in ["__main__","textbox"]:
    register()
