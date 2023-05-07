"""Image Utils

This script provides plenty of useful functions to process images related to creating a card.

This file can also be imported as a module and contains the following
functions:

    * load_font - loads a font
    * convert_card_dimensions_to_pixels - sets the card dimensions in pixels (using 300 dpi)
    * convert_image_to_rgba - if necessary, a loaded image will get converted to RGBA
    * create_mask_with_rounded_corners - creates a mask image with rounded corners
    * apply_rounded_corners_to_card - applies a mask with rounded corners to a card image
    * load_card_image_frame - loads the frame for a card image
"""

from PIL import Image, ImageDraw, ImageFont


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


def convert_card_dimensions_to_pixels():
    """Sets card dimensions in pixels (converts mm to pixels using 300 dpi)

    Returns
    -------
    int, int
        width and height in pixels
    """
    return int(63.5 * 300 / 25.4), int(88 * 300 / 25.4)


def convert_image_to_rgba(image):
    """Converts a loaded image to RGBA if necessary

    Parameters
    ----------
    image : Image
        The image that will be converted to RGBA

    Returns
    -------
    Image
        the image, possibly converted to RGBA
    """
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    return image


def create_mask_with_rounded_corners(width, height):
    """Creates a mask image with rounded corners

    Parameters
    ----------
    width : int
        The width that the mask must have
    height : int
        The height that the mask must have

    Returns
    -------
    Image
        the image mask with rounded corners
    """

    radius = 30
    mask = Image.new("L", (width, height), 0)
    mask_draw = ImageDraw.Draw(mask)

    mask_draw.ellipse((0, 0, 2 * radius, 2 * radius), fill=255)  # Upper-left
    mask_draw.ellipse(
        (width - 2 * radius, 0, width, 2 * radius), fill=255
    )  # Upper-right
    mask_draw.ellipse(
        (0, height - 2 * radius, 2 * radius, height), fill=255
    )  # Lower-left
    mask_draw.ellipse(
        (width - 2 * radius, height - 2 * radius, width, height), fill=255
    )  # Lower-right

    mask_draw.rectangle((radius, 0, width - radius, height), fill=255)
    mask_draw.rectangle((0, radius, width, height - radius), fill=255)

    return mask


def apply_rounded_corners_to_card(card):
    """Applies a mask with rounded corners to the card image

    Parameters
    ----------
    card : Image
        The card that will be made to have rounded corners
    width : int
        The width of the card
    height : int
        The height of the card

    """
    card.putalpha(create_mask_with_rounded_corners(card.width, card.height))


def load_card_image_frame(card_image_frame_path, width):
    """Loads the frame for the card image

    Parameters
    ----------
    card_image_frame_path : str
        The path to the card image frame PNG
    width : int
        The width of the canvas to drawn on

    Returns
    -------
    Image
        the loaded card image frame
    """

    card_image_frame = Image.open(card_image_frame_path)

    card_image_frame = convert_image_to_rgba(card_image_frame)

    card_image_frame_height = int(
        width * card_image_frame.height / card_image_frame.width
    )

    card_image_frame = card_image_frame.resize(
        (width, card_image_frame_height), Image.ANTIALIAS
    )

    return card_image_frame
