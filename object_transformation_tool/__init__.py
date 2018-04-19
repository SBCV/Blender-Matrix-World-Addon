import bpy
from mathutils import Vector, Matrix

bl_info = {
    "name": "Matrix World",
    "description": "Allows to work directly with Matrix World in the GUI",
    "author": "Your Name",
    "version": (0, 0, 1),
    "blender": (2, 79, 0),
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
        row.label(text="Text Block", icon='WORLD_DATA')
        row = layout.row()
        box = row.box()
        box.prop(textbox,"open_in_info_window",text="OPEN TEXT IN INFO WINDOW")
        
        row = layout.row()
        row.label(text="Active object is: " + obj.name)
        row = layout.row()
        row.operator("text.get_matrix_operator")
        row = layout.row()
        row.operator("text.invert_editor_matrix_operator")
        row = layout.row()
        row.operator("text.multiply_with_editor_matrix_operator")
        row = layout.row()
        row.operator("text.set_matrix_operator")

        for line in textbox.lines:
            row = layout.row()
            row.label(text=line.body)


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

class GetTransformationMatrixOperator(bpy.types.Operator):
    bl_idname = "text.get_matrix_operator"
    bl_label = "Get Transformation Matrix"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        matrix_world = context.active_object.matrix_world
        set_transformation_matrix_to_editor(matrix_world)

        return {'FINISHED'}

class SetTransformationMatrixOperator(bpy.types.Operator):
    bl_idname = "text.set_matrix_operator"
    bl_label = "Set Transformation Matrix"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        mat = get_transformation_matrix_from_editor()
        context.active_object.matrix_world = mat
        
        return {'FINISHED'}

class InvertEditorMatrixOperator(bpy.types.Operator):
    bl_idname = "text.invert_editor_matrix_operator"
    bl_label = "Invert Editor Transformation Matrix"

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
    bl_label = "Multiply Transformation Matrix With Editor Matrix"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        transformation_matrix = context.active_object.matrix_world
        multiply_matrix = get_transformation_matrix_from_editor()
        result = multiply_matrix * transformation_matrix 				# apply the new matrix (multiplication from left side) 
        set_transformation_matrix_to_editor(result)

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

    bpy.utils.register_class(TransformationMatrixPanel)
    bpy.utils.register_class(GetTransformationMatrixOperator)
    bpy.utils.register_class(InvertEditorMatrixOperator)
    bpy.utils.register_class(SetTransformationMatrixOperator)
    bpy.utils.register_class(MultiplyWithEditorMatrixOperator)

def unregister():
    bpy.utils.unregister_class(TransformationMatrixPanel)
    bpy.utils.unregister_class(GetTransformationMatrixOperator)
    bpy.utils.unregister_class(InvertEditorMatrixOperator)
    bpy.utils.unregister_class(SetTransformationMatrixOperator)
    bpy.utils.unregister_class(MultiplyWithEditorMatrixOperator)

if __name__ in ["__main__","textbox"]:
    register()