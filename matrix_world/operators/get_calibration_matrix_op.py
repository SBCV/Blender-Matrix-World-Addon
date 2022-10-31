import numpy as np
import bpy
from matrix_world.operators.utility import set_transformation_matrix_to_editor

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
