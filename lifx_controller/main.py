from controllers.light_controller import LightController
from controllers.scene_controller import SceneController
from ui.tui import TUI
import curses
import sys

def main():
    light_controller = LightController()
    scene_controller = SceneController()
    tui = TUI(light_controller, scene_controller)

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == "on":
            light_controller.turn_all_on()
        elif command == "off":
            light_controller.turn_all_off()
        elif len(sys.argv) == 3 and sys.argv[2].lower() == "on":
            scene_controller.apply_scene(command, light_controller)
        else:
            print("Invalid command")
    else:
        curses.wrapper(tui.run)

if __name__ == "__main__":
    main()