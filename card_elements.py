"""Card Elements

This script allows the user to draw the various elements of a card, such
as the base card, the image, the title, etc.

This file can also be imported as a module and contains the following
functions:

    * draw_base_card - draws the base card and returns that card and the draw instance
    * draw_card_image - draws the card image on top of a base card
    * draw_title - draws the title of the card
    * draw_icons - draws the icons of the card
"""

from PIL import Image, ImageDraw

from image_utils import (
    convert_image_to_rgba,
    crop_outer_boundaries_of_image,
    load_card_image_frame,
    load_font,
    recalculate_card_x_after_cropping,
    resize_image,
)
from text_utils import draw_text_with_shadow

TEXT_BANNER_PADDING = 30
CROP_MARGIN = 0.07
CARD_IMAGE_MARGIN = 100
CARD_IMAGE_DISTANCE_FROM_TOP = 140

TITLE_FONT = load_font("fonts/Roboto-Bold.ttf", 42)


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


def draw_card_image(card, card_image, canvas_width):
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

    card_image, calculated_card_image_width = resize_image(
        card_image, canvas_width, CARD_IMAGE_MARGIN
    )

    card_image = crop_outer_boundaries_of_image(card_image, CROP_MARGIN)

    calculated_card_image_x = (
        canvas_width - calculated_card_image_width
    ) // 2  # Center the card_image horizontally

    calculated_card_image_x = recalculate_card_x_after_cropping(
        card_image, calculated_card_image_x, calculated_card_image_width
    )

    card.paste(
        card_image, (calculated_card_image_x, CARD_IMAGE_DISTANCE_FROM_TOP), card_image
    )


def draw_card_frame(card_image_frame_path, card, height, width):
    card_image_frame = load_card_image_frame(card_image_frame_path, height, width)

    card_image_frame_x = 0
    card_image_frame_y = 0

    card.paste(
        card_image_frame, (card_image_frame_x, card_image_frame_y), card_image_frame
    )


def resize_text_banner(banner_image, title_width, title_height):
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

    return banner_image.resize((banner_width, banner_height), Image.LANCZOS)


def draw_title(title, title_banner_path, canvas_width, card, draw):
    """Draws the title of the card

    Parameters
    ----------
    title : str
        The title of the card
    title_banner_path : str
        The path to the banner that will be drawn behind the title
    canvas_width : int
        The width of the canvas where the title will be drawn
    card : Image
        The card where the banner will be drawn
    draw : ImageDraw
        Offers methods related to drawing
    """

    # Add title text
    title_width, title_height = draw.textsize(title, font=TITLE_FONT)
    title_x = (canvas_width - title_width) // 2
    title_y = 30

    # Load the banner image
    banner_image = Image.open(title_banner_path)
    banner_image = convert_image_to_rgba(banner_image)

    # Resize the banner image based on the width of the title text
    banner_image = resize_text_banner(banner_image, title_width, title_height)

    # Calculate the position of the banner image
    banner_x = title_x - TEXT_BANNER_PADDING
    banner_y = title_y - TEXT_BANNER_PADDING

    # Draw the banner image
    card.paste(banner_image, (banner_x, banner_y), banner_image)

    draw_text_with_shadow(draw, title, (title_x, title_y), TITLE_FONT, fill="white", shadow_offset=2, shadow_opacity=128)
