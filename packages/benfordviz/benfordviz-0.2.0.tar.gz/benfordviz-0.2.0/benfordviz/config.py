from benford.constants import COLORS #, dark_colors

COLOR_MODE = "light"

def set_color_mode(mode="light"):
    assert mode in ["light", "dark"], "Color mode must be 'light' or 'dark'."
    global COLOR_MODE
    COLOR_MODE = mode

def get_color_mode():
    if COLOR_MODE == "light":
        return COLORS
    # return dark_colors