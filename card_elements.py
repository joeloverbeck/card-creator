"""Card Elements

This script allows the user to draw the various elements of a card, such
as the base card, the image, the title, etc.

This file can also be imported as a module and contains the following
functions:

    * draw_base_card - draws the base card and returns that card and the draw instance
    * draw_card_image - draws the card image on top of a base card
    * draw_title - draws the title of the card
    * draw_card_description - draws the description of the card
    * draw_icons - draws the icons of the card
"""

from PIL import Image, ImageDraw

from image_utils import convert_image_to_rgba, load_font

TEXT_BANNER_PADDING = 30

title_font = load_font("arial.ttf", 30)
text_font = load_font("arial.ttf", 18)


def draw_base_card(background_image_path, width, height):
    """Loads and resizes the background image

    Parameters
    ----------
    background_image_path : str
        The path to the background image
    width : int
        The width of the canvas to draw on
    height : int
        The height of the canvas to draw on

    Returns
    -------
    card
        the base card on which all other elements will be drawn
    draw
        the draw instance that provides draw methods
    """
    card = Image.open(background_image_path).resize((width, height), Image.LANCZOS)

    draw = ImageDraw.Draw(card)

    return card, draw


def draw_card_image(card, card_image, width):
    """Draws the image of the card onto the base card

    Parameters
    ----------
    card : Image
        The base card
    card_image : Image
        The card image that will get drawn on the base card
    width : int
        The width of the canvas to drawn on
    """

    card_image = convert_image_to_rgba(card_image)

    # Calculate the size and position of the card_image
    card_image_width = width
    card_image_height = int(card_image_width * card_image.height / card_image.width)
    card_image_x = (width - card_image_width) // 2  # Center the card_image horizontally

    # Resize and position the card_image
    card_image = card_image.resize((width, card_image_height), Image.LANCZOS)

    crop_margin = 0.07
    crop_x0 = int(card_image.width * crop_margin)
    crop_y0 = int(card_image.height * crop_margin)
    crop_x1 = card_image.width - crop_x0
    crop_y1 = card_image.height - crop_y0
    card_image = card_image.crop((crop_x0, crop_y0, crop_x1, crop_y1))

    # Recalculate the position of the card image after cropping
    card_image_width, card_image_height = card_image.size
    card_image_x = (width - card_image_width) // 2

    card_image_y = 60

    card.paste(card_image, (card_image_x, card_image_y), card_image)


def resize_text_banner(title_width, title_height):
    """Resizes the text banner according to the title's dimensions

    Parameters
    ----------
    title_width : int
        The width of the title
    title_height : int
        The height of the title
    """

    banner_width = title_width + 2 * TEXT_BANNER_PADDING
    banner_height = title_height + 2 * TEXT_BANNER_PADDING
    banner_image = banner_image.resize((banner_width, banner_height), Image.LANCZOS)

def draw_title(title, title_banner_path, width, card, draw):
    """Draws the title of the card

    Parameters
    ----------
    title : str
        The title of the card
    title_banner_path : str
        The path to the banner that will be drawn behind the title
    width : int
        The width of the canvas where the title will be drawn
    card : Image
        The card where the banner will be drawn
    draw : ImageDraw
        Offers methods related to drawing
    """

    # Add title text
    title_width, title_height = draw.textsize(title, font=title_font)
    title_x = (width - title_width) // 2
    title_y = 30

    # Load the banner image
    banner_image = Image.open(title_banner_path)
    banner_image = convert_image_to_rgba(banner_image)

    # Resize the banner image based on the width of the title text
    resize_text_banner(title_width, title_height)

    # Calculate the position of the banner image
    banner_x = title_x - TEXT_BANNER_PADDING
    banner_y = title_y - TEXT_BANNER_PADDING

    # Draw the banner image
    card.paste(banner_image, (banner_x, banner_y), banner_image)

    draw.text((title_x, title_y), title, font=title_font, fill="white")


def draw_card_description(text, draw):
    """Draws the card description

    Parameters
    ----------
    text : str
        The text that will get drawn
    draw : ImageDraw
        Offers methods related to drawing
    """

    card_description_y = 800
    draw.text((10, card_description_y), text, font=text_font, fill="black")


def draw_icons(icon_paths, card, height):
    """Draws the icons of the card

    Parameters
    ----------
    icon_paths : list
        Contains the paths to all the icons that will need to get drawn
    card : Image
        The base card upon which the icons will be drawn
    height : int
        The height of the canvas where the title will be drawn
    """

    icon_x = 10
    icon_y = height - 50

    for icon_path in icon_paths:
        icon = Image.open(icon_path).resize((40, 40), Image.LANCZOS)

        icon = convert_image_to_rgba(icon)

        card.paste(icon, (icon_x, icon_y), icon)
        icon_x += 50
