from lifxlan import Light
import json
import os
from time import sleep

class LightController:
    def __init__(self):
        self.lights = {}
        self.config_file = "lights_config.json"
        self.load_lights_config()

    def load_lights_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            for light_id, light_info in config.items():
                self.lights[light_id] = Light(light_info['mac_addr'], 
                                            light_info['ip_addr'])

    def save_lights_config(self):
        config = {}
        for light_id, light in self.lights.items():
            config[light_id] = {
                'mac_addr': light.mac_addr,
                'ip_addr': light.ip_addr
            }
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)

    def add_light(self, light_id, mac_addr, ip_addr):
        """Add a new light to the controller."""
        try:
            new_light = Light(mac_addr.strip(), ip_addr.strip())
            # Test connection by getting label
            new_light.get_label()
            self.lights[light_id.strip()] = new_light
            self.save_lights_config()
            return True, "Light added successfully!"
        except Exception as e:
            return False, f"Error adding light: {str(e)}"

    def remove_light(self, light_id):
        """Remove a light from the controller."""
        try:
            if light_id in self.lights:
                del self.lights[light_id]
                self.save_lights_config()
                return True, f"Light {light_id} removed successfully!"
            return False, f"Light {light_id} not found."
        except Exception as e:
            return False, f"Error removing light: {str(e)}"

    def get_light_info(self, light_id):
        """Get information about a specific light."""
        try:
            if light_id in self.lights:
                light = self.lights[light_id]
                return {
                    'id': light_id,
                    'label': light.get_label(),
                    'power': light.get_power(),
                    'ip_addr': light.ip_addr,
                    'mac_addr': light.mac_addr
                }
            return None
        except Exception as e:
            print(f"Error getting light info: {str(e)}")
            return None

    def turn_all_on(self):
        """Turn on all lights with bright white."""
        results = []
        for light_id, light in self.lights.items():
            try:
                light.set_power(True)
                light.set_color([0, 0, 65535, 5500])  # Full brightness, 5500K white
                results.append((True, f"Successfully turned on {light_id}"))
            except Exception as e:
                results.append((False, f"Failed to turn on {light_id}: {str(e)}"))
        return results

    def turn_all_off(self):
        """Turn off all lights."""
        results = []
        for light_id, light in self.lights.items():
            try:
                light.set_power(False)
                results.append((True, f"Successfully turned off {light_id}"))
            except Exception as e:
                results.append((False, f"Failed to turn off {light_id}: {str(e)}"))
        return results

    def set_light_color(self, light_id, hsbk):
        """Set color for a specific light."""
        try:
            if light_id in self.lights:
                light = self.lights[light_id]
                light.set_color(hsbk)
                return True, f"Color set for {light_id}"
            return False, f"Light {light_id} not found"
        except Exception as e:
            return False, f"Error setting color for {light_id}: {str(e)}"

    def set_light_brightness(self, light_id, brightness):
        """Set brightness for a specific light."""
        try:
            if light_id in self.lights:
                light = self.lights[light_id]
                current_color = light.get_color()
                current_color[2] = brightness  # Update brightness
                light.set_color(current_color)
                return True, f"Brightness set for {light_id}"
            return False, f"Light {light_id} not found"
        except Exception as e:
            return False, f"Error setting brightness for {light_id}: {str(e)}"

    def get_all_lights(self):
        """Get information about all lights."""
        lights_info = {}
        for light_id in self.lights:
            info = self.get_light_info(light_id)
            if info:
                lights_info[light_id] = info
        return lights_info

    def toggle_light(self, light_id):
        """Toggle a specific light on/off."""
        try:
            if light_id in self.lights:
                light = self.lights[light_id]
                current_power = light.get_power()
                light.set_power(not current_power)
                state = "on" if not current_power else "off"
                return True, f"Toggled {light_id} {state}"
            return False, f"Light {light_id} not found"
        except Exception as e:
            return False, f"Error toggling {light_id}: {str(e)}"

    def set_light_power(self, light_id, power_state):
        """Set power state for a specific light."""
        try:
            if light_id in self.lights:
                light = self.lights[light_id]
                light.set_power(power_state)
                state = "on" if power_state else "off"
                return True, f"Turned {light_id} {state}"
            return False, f"Light {light_id} not found"
        except Exception as e:
            return False, f"Error setting power for {light_id}: {str(e)}"