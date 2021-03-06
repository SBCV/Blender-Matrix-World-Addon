import bpy
from mathutils import Vector, Matrix
import os
import numpy as np

from bpy.props import (CollectionProperty,
                       StringProperty,
                       BoolProperty,
                       EnumProperty,
                       FloatProperty,
                       IntProperty,
                       )

from bpy_extras.io_utils import (ImportHelper,
                                 ExportHelper,
                                 axis_conversion)

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


def convert_matrix_to_string(some_matrix):

    matrix_str = ''
    for row in some_matrix:
        row_str = ''
        for entry in row:
            row_str += str(entry) + ' '
        # remove last space char
        row_str = row_str.rstrip()
        matrix_str += row_str + '\n'
    # remove last linesep char
    matrix_str = matrix_str.rstrip('\n')
    return matrix_str

def get_transformation_matrix_from_editor():
    textbox = bpy.data.texts.get("TransformationMatrix")

    rows = []
    for line in textbox.lines:
        line_as_floats = [float(num_str) for num_str in line.body.split()]
        row = Vector(line_as_floats)
        rows.append(row)
        
    mat = Matrix(rows)
    return mat

def set_transformation_matrix_to_editor(transformation_matrix):
    matrix_world_str = convert_matrix_to_string(transformation_matrix)
    textbox = bpy.data.texts.get("TransformationMatrix")
    textbox.from_string(matrix_world_str)


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
    
class GetCalibrationMatrixOperator(bpy.types.Operator):
    bl_idname = "text.get_calibration_matrix_operator"
    bl_label = "Get Calibration Matrix from Selected Camera"
    
    def compute_calibration_mat(self, focal_length, cx, cy):
        return np.array([[focal_length, 0, cx],
                        [0, focal_length, cy],
                        [0, 0, 1]], dtype=float)
    
    def get_calibration_mat(self, blender_camera):
        scene = bpy.context.scene
        render_resolution_width = scene.render.resolution_x
        render_resolution_height = scene.render.resolution_y
        focal_length_in_mm = float(blender_camera.data.lens)
        sensor_width_in_mm = float(blender_camera.data.sensor_width)
        focal_length_in_pixel = \
            float(max(scene.render.resolution_x, scene.render.resolution_y)) * \
            focal_length_in_mm / sensor_width_in_mm
            
        max_extent = max(render_resolution_width, render_resolution_height)
        p_x = render_resolution_width / 2.0 - blender_camera.data.shift_x * max_extent
        p_y = render_resolution_height / 2.0 - blender_camera.data.shift_y * max_extent

        calibration_mat = self.compute_calibration_mat(
            focal_length_in_pixel, cx=p_x, cy=p_y)

        return calibration_mat

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        # TODO assert is camera
        calib_mat = self.get_calibration_mat(context.active_object)
        set_transformation_matrix_to_editor(calib_mat)

        return {'FINISHED'}

class RefreshMatrixOperator(bpy.types.Operator):
    bl_idname = "text.refresh_matrix_operator"
    bl_label = "Refresh Editor Matrix after Editing"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        return {'FINISHED'}

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

        return {'FINISHED'}

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

class SaveMatrixOperator(bpy.types.Operator, ExportHelper):
    bl_idname = "text.save_matrix_operator"
    bl_label = "Save Current Matrix to Disc (.npy, .txt)"
    
    filename_ext : StringProperty(default=".txt")
    
    @classmethod
    def poll(cls, context): 
        #return context.active_object is not None
        return True

    def execute(self, context):
        self.report({'INFO'}, 'Output File Path: ' + str(self.filepath))
        mat = get_transformation_matrix_from_editor()
        mat_np = np.array(mat)
        with open(self.filepath, "wb") as f:
            if os.path.splitext(self.filepath)[1] == '.npy':
                np.save(f, mat_np)
            elif os.path.splitext(self.filepath)[1] == '.txt':
                np.savetxt(f, mat_np)
        
        return {'FINISHED'}


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
    bpy.types.Text.open_in_info_window = bpy.props.BoolProperty("Open in INFO window", default=False, update=openInInfoWin)
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
