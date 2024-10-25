from config.scenes import SCENES
from ui.color_utils import hex_to_hsbk

class SceneController:
    def __init__(self):
        self.scenes = SCENES

    def apply_scene(self, scene_name, light_controller):
        if scene_name not in self.scenes:
            return False

        scene = self.scenes[scene_name]
        for light_id, settings in scene.items():
            if light_id in light_controller.lights:
                light = light_controller.lights[light_id]
                try:
                    light.set_power(True)
                    hsbk_color = hex_to_hsbk(settings['color'])
                    hsbk_color[2] = settings['brightness']
                    light.set_color(hsbk_color)
                except Exception as e:
                    print(f"Failed to process {light_id}: {str(e)}")
        return True
