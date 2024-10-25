import curses
from ui.color_utils import hex_to_rgb, rgb_to_256

class TUI:
    def __init__(self, light_controller, scene_controller):
        self.light_controller = light_controller
        self.scene_controller = scene_controller
        self.current_selection = 0

    def center_text(self, stdscr, text, y_position):
        """Helper function to center text horizontally."""
        height, width = stdscr.getmaxyx()
        x_position = (width - len(text)) // 2
        stdscr.addstr(y_position, x_position, text)

    def draw_color_box(self, window, y, x, width, height, color_hex):
        """Draw a colored box using block characters with 256 colors."""
        try:
            r, g, b = hex_to_rgb(color_hex)
            color_number = rgb_to_256(r, g, b)
            pair_number = color_number + 1  # avoid pair 0
            curses.init_pair(pair_number, color_number, color_number)
            
            for i in range(height):
                window.addstr(y + i, x, "█" * width, curses.color_pair(pair_number))
        except Exception as e:
            for i in range(height):
                window.addstr(y + i, x, "■" * width, curses.A_NORMAL)

    def draw_scene_preview(self, window, scene_name, y_pos):
        """Draw a preview of a scene with its three light colors."""
        height, width = window.getmaxyx()
        scene = self.scene_controller.scenes[scene_name]
        
        # Calculate proper spacing
        name_width = 15
        color_width = 8
        color_spacing = 2
        total_width = name_width + (3 * (color_width + color_spacing))
        
        # Calculate starting x position to center the entire preview
        start_x = (width - total_width) // 2
        
        # Draw scene name
        window.addstr(y_pos, start_x, f"{scene_name.capitalize():<{name_width}}")
        
        # Draw three color boxes for each light
        for i, light in enumerate(['light1', 'light2', 'light3']):
            if light in scene:
                color = scene[light]['color']
                x_pos = start_x + name_width + (i * (color_width + color_spacing))
                self.draw_color_box(window, y_pos, x_pos, color_width, 2, color)

    def draw_menu(self, stdscr):
        """Draw the main menu with scenes and options."""
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Draw title
        title = "LIFX Light Controller"
        self.center_text(stdscr, title, 1)
        
        # Draw instructions
        instructions = "↑/↓: Navigate | Enter: Select | q: Quit | a: Add New Light | r: Remove Light"
        self.center_text(stdscr, instructions, 3)
        
        # Draw scenes
        scenes_list = list(self.scene_controller.scenes.keys())
        start_y = 5
        for idx, scene in enumerate(scenes_list):
            if idx == self.current_selection:
                stdscr.attron(curses.A_REVERSE)
            self.draw_scene_preview(stdscr, scene, start_y + idx * 3)
            if idx == self.current_selection:
                stdscr.attroff(curses.A_REVERSE)
        
        # Draw connected lights section
        lights_y = start_y + len(scenes_list) * 3 + 2
        self.center_text(stdscr, "Connected Lights:", lights_y)
        
        # Get and display light information
        lights_info = self.light_controller.get_all_lights()
        for i, (light_id, info) in enumerate(lights_info.items()):
            status = "Connected" if info.get('power') else "Off"
            light_text = f"{light_id}: {info.get('label', 'Unknown')} ({status})"
            self.center_text(stdscr, light_text, lights_y + i + 1)
        
        stdscr.refresh()

    def add_new_light(self, stdscr):
        """Display form to add a new light."""
        height, width = stdscr.getmaxyx()
        stdscr.clear()
        curses.echo()
        curses.curs_set(1)
        
        # Center form elements
        form_y = height // 4
        self.center_text(stdscr, "Add New Light", form_y)
        self.center_text(stdscr, "Press ESC at any time to cancel", form_y + 1)
        
        # Form fields
        fields = [
            ("Light ID (e.g., light4): ", "", 20),
            ("MAC Address (e.g., d0:73:d5:xx:xx:xx): ", "", 17),
            ("IP Address (e.g., 192.168.1.xxx): ", "", 15)
        ]
        
        values = []
        for i, (prompt, _, max_len) in enumerate(fields):
            field_y = form_y + 3 + i
            self.center_text(stdscr, prompt, field_y)
            
            # Calculate input position
            prompt_x = (width - len(prompt)) // 2 + len(prompt)
            stdscr.move(field_y, prompt_x)
            
            # Get input
            value = ""
            while True:
                ch = stdscr.getch()
                if ch == 27:  # ESC
                    curses.noecho()
                    curses.curs_set(0)
                    return
                elif ch == 10:  # Enter
                    if value.strip():
                        values.append(value)
                        break
                elif ch in (curses.KEY_BACKSPACE, 127):  # Backspace
                    if value:
                        value = value[:-1]
                        stdscr.addstr(field_y, prompt_x, " " * max_len)
                        stdscr.addstr(field_y, prompt_x, value)
                elif len(value) < max_len:
                    value += chr(ch)
                    stdscr.addstr(field_y, prompt_x + len(value) - 1, chr(ch))
                
                stdscr.refresh()
        
        curses.noecho()
        curses.curs_set(0)
        
        if len(values) == 3:
            success, message = self.light_controller.add_light(*values)
            self.center_text(stdscr, message, form_y + 7)
            self.center_text(stdscr, "Press any key to continue...", form_y + 9)
            stdscr.refresh()
            stdscr.getch()

    def remove_light(self, stdscr):
        """Display interface to remove a light."""
        height, width = stdscr.getmaxyx()
        stdscr.clear()
        
        lights = self.light_controller.get_all_lights()
        if not lights:
            self.center_text(stdscr, "No lights available to remove", height // 2)
            self.center_text(stdscr, "Press any key to continue...", height // 2 + 2)
            stdscr.refresh()
            stdscr.getch()
            return
        
        self.center_text(stdscr, "Select light to remove:", 2)
        self.center_text(stdscr, "Use arrow keys to select, Enter to confirm, ESC to cancel", 4)
        
        current_selection = 0
        light_ids = list(lights.keys())
        
        while True:
            for i, light_id in enumerate(light_ids):
                if i == current_selection:
                    stdscr.attron(curses.A_REVERSE)
                self.center_text(stdscr, light_id, 6 + i)
                if i == current_selection:
                    stdscr.attroff(curses.A_REVERSE)
            
            stdscr.refresh()
            key = stdscr.getch()
            
            if key == 27:  # ESC
                break
            elif key == curses.KEY_UP and current_selection > 0:
                current_selection -= 1
            elif key == curses.KEY_DOWN and current_selection < len(light_ids) - 1:
                current_selection += 1
            elif key == 10:  # Enter
                success, message = self.light_controller.remove_light(light_ids[current_selection])
                self.center_text(stdscr, message, height - 4)
                self.center_text(stdscr, "Press any key to continue...", height - 2)
                stdscr.refresh()
                stdscr.getch()
                break

    def apply_scene(self, stdscr, scene_name):
        """Apply selected scene with visual feedback."""
        height, width = stdscr.getmaxyx()
        stdscr.clear()
        
        # Show applying message
        self.center_text(stdscr, f"Applying scene: {scene_name}", height // 3)
        stdscr.refresh()
        
        # Apply the scene
        success = self.scene_controller.apply_scene(scene_name, self.light_controller)
        
        # Show result
        if success:
            self.center_text(stdscr, "Scene applied successfully!", height // 2)
        else:
            self.center_text(stdscr, "Failed to apply scene", height // 2)
        
        self.center_text(stdscr, "Press any key to continue...", height // 2 + 2)
        stdscr.refresh()
        stdscr.getch()

    def run(self, stdscr):
        """Main TUI loop."""
        # Initialize colors
        curses.start_color()
        curses.use_default_colors()
        if curses.COLORS < 256:
            raise Exception("Your terminal doesn't support 256 colors")
        
        curses.curs_set(0)
        stdscr.keypad(True)
        
        while True:
            self.draw_menu(stdscr)
            key = stdscr.getch()
            
            if key == ord('q'):
                break
            elif key == ord('a'):
                self.add_new_light(stdscr)
            elif key == ord('r'):
                self.remove_light(stdscr)
            elif key == curses.KEY_UP and self.current_selection > 0:
                self.current_selection -= 1
            elif key == curses.KEY_DOWN:
                scenes_list = list(self.scene_controller.scenes.keys())
                if self.current_selection < len(scenes_list) - 1:
                    self.current_selection += 1
            elif key == 10:  # Enter
                scenes_list = list(self.scene_controller.scenes.keys())
                selected_scene = scenes_list[self.current_selection]
                self.apply_scene(stdscr, selected_scene)