import bpy
from mathutils import Vector, Matrix


def get_transformation_matrix_from_editor():
    textbox = bpy.data.texts.get("TransformationMatrix")
    rows = []
    for line in textbox.lines:
        line_as_floats = [float(num_str) for num_str in line.body.split()]
        row = Vector(line_as_floats)
        rows.append(row)
    mat = Matrix(rows)
    return mat


def _convert_matrix_to_string(some_matrix):
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


def set_transformation_matrix_to_editor(transformation_matrix):
    matrix_world_str = _convert_matrix_to_string(transformation_matrix)
    textbox = bpy.data.texts.get("TransformationMatrix")
    textbox.from_string(matrix_world_str)

