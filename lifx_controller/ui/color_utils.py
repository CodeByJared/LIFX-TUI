import colorsys

def hex_to_hsbk(hex_color):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    hsv = colorsys.rgb_to_hsv(rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0)
    return [
        int(hsv[0] * 65535),  # hue
        int(hsv[1] * 65535),  # saturation
        int(hsv[2] * 65535),  # brightness
        3500                   # kelvin
    ]

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_256(r, g, b):
    if r == g == b:
        if r < 8: return 16
        if r > 248: return 231
        return round(((r - 8) / 247) * 24) + 232

    r_index = round(r / 255 * 5)
    g_index = round(g / 255 * 5)
    b_index = round(b / 255 * 5)
    
    return 16 + (36 * r_index) + (6 * g_index) + b_index
