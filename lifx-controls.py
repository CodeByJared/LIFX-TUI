from lifxlan import Light
from time import sleep
import sys
import colorsys
import curses
import os
import json

CONFIG_FILE = "lights_config.json"

def save_lights_config():
    """Save lights configuration to JSON file."""
    config = {}
    for light_id, light in LIGHTS.items():
        config[light_id] = {
            'mac_addr': light.mac_addr,
            'ip_addr': light.ip_addr
        }
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def load_lights_config():
    """Load lights configuration from JSON file."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        
        for light_id, light_info in config.items():
            LIGHTS[light_id] = Light(light_info['mac_addr'], light_info['ip_addr'])
            
def add_new_light(stdscr):
    """Display form to add a new light."""
    stdscr.clear()
    curses.echo()  # Enable echo of typed characters
    curses.curs_set(1)  # Show cursor
    
    # Draw form
    stdscr.addstr(1, 2, "Add New Light")
    stdscr.addstr(2, 2, "Press ESC at any time to cancel")
    stdscr.addstr(4, 2, "Light ID (e.g., light4): ")
    stdscr.addstr(5, 2, "MAC Address (e.g., d0:73:d5:xx:xx:xx): ")
    stdscr.addstr(6, 2, "IP Address (e.g., 192.168.1.xxx): ")
    
    # Get Light ID
    stdscr.move(4, 25)
    light_id = ""
    while True:
        stdscr.refresh()
        ch = stdscr.getch()
        if ch == 27:  # ESC key
            curses.noecho()
            curses.curs_set(0)
            return
        elif ch == 10:  # Enter key
            if light_id.strip():  # Only proceed if not empty
                break
        elif ch == curses.KEY_BACKSPACE or ch == 127:  # Backspace
            if light_id:
                light_id = light_id[:-1]
                stdscr.addstr(4, 25, " " * 20)  # Clear the line
                stdscr.addstr(4, 25, light_id)
        else:
            light_id += chr(ch)
    
    # Get MAC Address
    stdscr.move(5, 40)
    mac_addr = ""
    while True:
        stdscr.refresh()
        ch = stdscr.getch()
        if ch == 27:  # ESC key
            curses.noecho()
            curses.curs_set(0)
            return
        elif ch == 10:  # Enter key
            if mac_addr.strip():  # Only proceed if not empty
                break
        elif ch == curses.KEY_BACKSPACE or ch == 127:  # Backspace
            if mac_addr:
                mac_addr = mac_addr[:-1]
                stdscr.addstr(5, 40, " " * 20)  # Clear the line
                stdscr.addstr(5, 40, mac_addr)
        else:
            mac_addr += chr(ch)
    
    # Get IP Address
    stdscr.move(6, 35)
    ip_addr = ""
    while True:
        stdscr.refresh()
        ch = stdscr.getch()
        if ch == 27:  # ESC key
            curses.noecho()
            curses.curs_set(0)
            return
        elif ch == 10:  # Enter key
            if ip_addr.strip():  # Only proceed if not empty
                break
        elif ch == curses.KEY_BACKSPACE or ch == 127:  # Backspace
            if ip_addr:
                ip_addr = ip_addr[:-1]
                stdscr.addstr(6, 35, " " * 20)  # Clear the line
                stdscr.addstr(6, 35, ip_addr)
        else:
            ip_addr += chr(ch)
    
    curses.noecho()
    curses.curs_set(0)
    
    try:
        # Create new light
        new_light = Light(mac_addr.strip(), ip_addr.strip())
        
        # Test connection
        new_light.get_label()
        
        # Add to LIGHTS dictionary
        LIGHTS[light_id.strip()] = new_light
        
        # Save configuration
        save_lights_config()
        
        stdscr.addstr(8, 2, "Light added successfully! Press any key to continue...")
    except Exception as e:
        stdscr.addstr(8, 2, f"Error adding light: {str(e)}")
        stdscr.addstr(9, 2, "Press any key to continue...")
    
    stdscr.refresh()
    stdscr.getch()


def hex_to_hsbk(hex_color):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    hsv = colorsys.rgb_to_hsv(rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0)
    hue = int(hsv[0] * 65535)
    saturation = int(hsv[1] * 65535)
    brightness = int(hsv[2] * 65535)
    kelvin = 3500
    return [hue, saturation, brightness, kelvin]

# Dictionary of all lights
LIGHTS = {}

# Dictionary of scenes
SCENES = {
    'nature': {
        'light1': {'color': '474A2C', 'brightness': 65535},  # Drab dark brown
        'light2': {'color': '636940', 'brightness': 65535},  # Dark moss green
        'light3': {'color': '59A96A', 'brightness': 65535}   # Jade
    },
    'ocean': {
        'light1': {'color': '1A936F', 'brightness': 65535},  # Sea green
        'light2': {'color': '88D498', 'brightness': 65535},  # CeladonJasmine
        'light3': {'color': 'ffffff', 'brightness': 65535}   # Bright White
    },
    'sunset' : {
        'light1': {'color': 'CE4993', 'brightness': 65535},  # Mulberry
        'light2': {'color': 'FB9062', 'brightness': 65535},  # Atomic Tangerine
        'light3': {'color': 'EEAF61', 'brightness': 65535}   # Earth Yellow
    },
    'movie': {
        'light1': {'color': '1a1a1a', 'brightness': 20000},  # Eerie black
        'light2': {'color': '000000', 'brightness': 0},      # Off
        'light3': {'color': '1a1a1a', 'brightness': 20000}   # Eerie black
    },
    'lime' : {
        'light1': {'color': 'D7FFF1', 'brightness': 65535},  # Mint green
        'light2': {'color': 'AAFCB8', 'brightness': 65535},  # Light green
        'light3': {'color': '8CD790', 'brightness': 65535}   # Light green 2
    },
    'game' : {
        'light1': {'color': '1D2F6F', 'brightness': 65535},  # Delft Blue
        'light2': {'color': '8390FA', 'brightness': 65535},  # Vista Blue
        'light3': {'color': 'FAC748', 'brightness': 65535}   # Saffron
    },
    'night': {
        'light1': {'color': '1a1a1a', 'brightness': 20000},  # Eerie black
        'light2': {'color': '1a1a1a', 'brightness': 20000},  # Eerie black
        'light3': {'color': '1a1a1a', 'brightness': 20000}   # Eerie black
    }
}

def turn_lights_on():
    print("\nTurning on lights with bright white...")
    for light_id, light in LIGHTS.items():
        try:
            print(f"Processing {light_id} ({light.get_label()})")
            light.set_power(True)
            # Set to bright white
            light.set_color([0, 0, 65535, 5500])  # Full brightness, 5500K white
        except Exception as e:
            print(f"Failed to process {light_id}: {str(e)}")
    sleep(1)
    print("All lights have been turned on to bright white.")

def set_scene(scene_name):
    if scene_name not in SCENES:
        print(f"Scene '{scene_name}' not found. Available scenes: {', '.join(SCENES.keys())}")
        return False

    scene = SCENES[scene_name]
    print(f"\nSetting scene: {scene_name}")

    for light_id, settings in scene.items():
        if light_id in LIGHTS:
            light = LIGHTS[light_id]
            try:
                print(f"Processing {light_id} ({light.get_label()})")
                light.set_power(True)
                
                # Convert hex color to HSBK
                hsbk_color = hex_to_hsbk(settings['color'])
                # Override brightness with scene-specific brightness
                hsbk_color[2] = settings['brightness']
                
                light.set_color(hsbk_color)
            except Exception as e:
                print(f"Failed to process {light_id}: {str(e)}")

    return True

def turn_lights_off():
    for light_id, light in LIGHTS.items():
        try:
            print(f"\nProcessing {light_id} ({light.get_label()})")
            print("Turning off the light...")
            light.set_power(False)
        except Exception as e:
            print(f"Failed to process light: {str(e)}")

    sleep(1)
    print("All lights have been turned off.")
    
def rgb_to_256(r, g, b):
    """Convert RGB values to the closest xterm-256 color code."""
    if r == g == b:
        if r < 8:
            return 16
        if r > 248:
            return 231
        return round(((r - 8) / 247) * 24) + 232

    r_index = round(r / 255 * 5)
    g_index = round(g / 255 * 5)
    b_index = round(b / 255 * 5)
    
    return 16 + (36 * r_index) + (6 * g_index) + b_index

def hex_to_rgb(hex_color):
    """Convert hex color string to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def draw_color_box(window, y, x, width, height, color_hex):
    """Draw a colored box using block characters with 256 colors."""
    try:
        # Convert hex to RGB
        r, g, b = hex_to_rgb(color_hex)
        
        # Get the closest 256 color
        color_number = rgb_to_256(r, g, b)
        
        # Create a new color pair for this color
        pair_number = color_number + 1  # avoid pair 0
        curses.init_pair(pair_number, color_number, color_number)
        
        # Draw the color box
        for i in range(height):
            window.addstr(y + i, x, "█" * width, curses.color_pair(pair_number))
            
    except Exception as e:
        # Fallback if color initialization fails
        for i in range(height):
            window.addstr(y + i, x, "■" * width, curses.A_NORMAL)

def init_colors():
    """Initialize terminal for 256 color support"""
    curses.start_color()
    curses.use_default_colors()
    
    # Check if terminal supports 256 colors
    if curses.COLORS < 256:
        raise Exception("Your terminal doesn't support 256 colors")

def draw_scene_preview(window, scene_name, y_pos):
    """Draw a preview of a scene with its three light colors."""
    scene = SCENES[scene_name]
    
    # Calculate proper spacing
    name_width = 15  # Width for scene name
    color_width = 8  # Width for each color box
    color_spacing = 2  # Spacing between color boxes
    
    # Draw scene name
    window.addstr(y_pos, 2, f"{scene_name.capitalize():<{name_width}}")
    
    # Draw three color boxes for each light
    for i, light in enumerate(['light1', 'light2', 'light3']):
        color = scene[light]['color']
        x_pos = name_width + 2 + (i * (color_width + color_spacing))
        draw_color_box(window, y_pos, x_pos, color_width, 2, color)

def draw_menu(stdscr, selected_idx):
    """Draw the main menu with scenes and options."""
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    
    # Draw title
    title = "LIFX Light Controller"
    stdscr.addstr(1, (width - len(title)) // 2, title, curses.A_BOLD)
    
    # Draw instructions
    stdscr.addstr(3, 2, "↑/↓: Navigate | Enter: Select | q: Quit | a: Add New Light")
    
    # Draw scenes
    for idx, scene in enumerate(SCENES.keys()):
        if idx == selected_idx:
            stdscr.attron(curses.A_REVERSE)
        draw_scene_preview(stdscr, scene, 5 + idx * 3)
        if idx == selected_idx:
            stdscr.attroff(curses.A_REVERSE)
    
    # Draw current lights
    stdscr.addstr(5 + len(SCENES) * 3, 2, "Connected Lights:", curses.A_BOLD)
    for i, (light_id, light) in enumerate(LIGHTS.items()):
        try:
            label = light.get_label()
            stdscr.addstr(6 + len(SCENES) * 3 + i, 4, 
                         f"{light_id}: {label} ({light.ip_addr})")
        except:
            stdscr.addstr(6 + len(SCENES) * 3 + i, 4, 
                         f"{light_id}: Disconnected ({light.ip_addr})")
    
    stdscr.refresh()

def tui_main(stdscr):
    """Main TUI function."""
    # Load saved lights configuration
    load_lights_config()
    
    # Initialize colors
    init_colors()
    
    # Hide cursor
    curses.curs_set(0)
    
    # Enable keypad input
    stdscr.keypad(True)
    
    current_selection = 0
    scenes_list = list(SCENES.keys())
    
    while True:
        draw_menu(stdscr, current_selection)
        key = stdscr.getch()
        
        if key == ord('q'):
            break
        elif key == ord('a'):
            add_new_light(stdscr)
        elif key == curses.KEY_UP and current_selection > 0:
            current_selection -= 1
        elif key == curses.KEY_DOWN and current_selection < len(scenes_list) - 1:
            current_selection += 1
        elif key == 10:  # Enter key

            selected_scene = scenes_list[current_selection]
            stdscr.clear()
            stdscr.addstr(1, 2, f"Applying scene: {selected_scene}")
            stdscr.refresh()
            set_scene(selected_scene)
            stdscr.addstr(3, 2, "Press any key to continue...")
            stdscr.refresh()
            stdscr.getch()

def main():
    if len(sys.argv) > 1:
        # Handle command line arguments as before
        if len(sys.argv) == 2:
            command = sys.argv[1].lower()
            if command == "on":
                turn_lights_on()
            elif command == "off":
                turn_lights_off()
            else:
                print("Invalid command. Use 'on' or 'off'")
                sys.exit(1)
        elif len(sys.argv) == 3:
            scene = sys.argv[1].lower()
            command = sys.argv[2].lower()
            
            if command == "on" and scene in SCENES:
                set_scene(scene)
            else:
                print(f"Invalid command or scene. Available scenes: {', '.join(SCENES.keys())}")
                sys.exit(1)
    else:
        # Launch TUI if no arguments provided
        curses.wrapper(tui_main)

if __name__ == "__main__":
    main()