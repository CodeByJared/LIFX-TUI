from pytermgui import Terminal, Color, tim
import asyncio

class SceneViewer:
    def __init__(self):
        self.terminal = Terminal()
        self.padding = 2
        self.box_width = 20
        self.box_height = 3
        self.terminal.subscribe(Terminal.RESIZE, self.on_resize)
        
    def on_resize(self, new_size):
        """Handle terminal resize events by redrawing"""
        self.draw()
        
    def draw_color_box(self, x, y, color_hex, label):
        """Draw a colored box with a label"""
        color = Color.parse(color_hex, background=True)
        
        # Draw the colored box
        for i in range(self.box_height):
            colored_spaces = f"{color.sequence}{' ' * self.box_width}\x1b[0m"
            self.terminal.write(colored_spaces, pos=(x, y + i))
        
        # Draw the label with style
        label_text = tim.parse(f"[bold]{label}[/]")
        label_x = x + (self.box_width - len(label)) // 2
        self.terminal.write(label_text, pos=(label_x, y + self.box_height))
        
        # Draw the hex value with style
        hex_value = tim.parse(f"[italic]#{color_hex}[/]")
        hex_x = x + (self.box_width - len(color_hex) - 1) // 2
        self.terminal.write(hex_value, pos=(hex_x, y + self.box_height + 1))

    def draw_scene(self, scene_name, scene_data, start_y):
        """Draw a complete scene with its title and color boxes"""
        if start_y is None or start_y >= self.terminal.height:
            return None
            
        title_text = f" {scene_name.upper()} "
        box_width = len(title_text) + 4
        
        # Get the first color from the scene for the title
        title_color = f"#{list(scene_data.values())[0]['color']}"
        
        # Create box with scene's color and bold text
        box = [
            tim.parse(f"[bold {title_color}]╔{'═' * (box_width-2)}╗[/]"),
            tim.parse(f"[bold {title_color}]║[/]  [italic {title_color}]{scene_name.upper()}[/]  [bold {title_color}]║[/]"),
            tim.parse(f"[bold {title_color}]╚{'═' * (box_width-2)}╝[/]")
        ]
        
        # Calculate center position
        title_x = (self.terminal.width - box_width) // 2
        
        # Draw box
        for i, line in enumerate(box):
            if start_y + i >= self.terminal.height:
                return None
            self.terminal.write(line, pos=(title_x, start_y + i))
            
        # Adjust starting Y for the boxes
        box_start_y = start_y + 4
        
        # Draw color boxes
        total_width = (self.box_width + self.padding) * 3
        start_x = (self.terminal.width - total_width) // 2
        
        for i, (light_name, light_data) in enumerate(scene_data.items()):
            x = start_x + (self.box_width + self.padding) * i
            y = box_start_y
            if y + self.box_height + 2 < self.terminal.height:
                self.draw_color_box(x, y, light_data['color'], light_name)
        
        return box_start_y + self.box_height + 4


    def draw(self):
        """Draw all scenes"""
        self.terminal.clear_stream()
        
        current_y = 1
        for scene_name, scene_data in SCENES.items():
            next_y = self.draw_scene(scene_name, scene_data, current_y)
            if next_y is None:
                break
            current_y = next_y
            
        self.terminal.flush()

    async def run(self):
        """Run the viewer with scrolling"""
        try:
            self.draw()
            while True:
                # Use asyncio.get_event_loop().run_in_executor for blocking operations
                cmd = await asyncio.get_event_loop().run_in_executor(None, input)
                
                if cmd.lower() == 'q':
                    break
                elif cmd.lower() == 'j':  # Scroll down
                    self.scroll_offset += self.box_height + 4
                    self.draw()
                elif cmd.lower() == 'k':  # Scroll up
                    self.scroll_offset = max(0, self.scroll_offset - (self.box_height + 4))
                    self.draw()
        finally:
            self.terminal.clear_stream()
            self.terminal.flush()

async def main():
    viewer = SceneViewer()
    await viewer.run()

if __name__ == "__main__":
    asyncio.run(main())
    viewer = SceneViewer()
    viewer.run()