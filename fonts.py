from PIL import ImageFont


def load_font(font_path, size):
    """Loads a font

    Parameters
    ----------
    font_path : str
        The path to the font. Could be ex. 'Arial.ttf', if it's a system font.
    size : int
        The size that the font will be drawn at

    Returns
    -------
    FreeTypeFont
        the loaded font
    """
    return ImageFont.truetype(font_path, size)


BIOME_TITLE_FONT = load_font("fonts/Roboto-Bold.ttf", 60)
ENCOUNTER_TITLE_FONT = load_font("fonts/Roboto-Bold.ttf", 42)
