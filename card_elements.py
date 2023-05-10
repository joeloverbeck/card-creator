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
    calculate_centered_x,
    calculate_height_of_image_according_to_width,
    calculate_new_image_dimensions_respecting_aspect_ratio,
    convert_image_to_rgba,
    crop_image,
    crop_image_to_fit_canvas_dimensions,
    resize_image,
)
from text_utils import draw_text_with_shadow

TEXT_BANNER_PADDING = 30
CROP_MARGIN = 0.07
CARD_IMAGE_MARGIN = 100
CARD_IMAGE_DISTANCE_FROM_TOP = 140

BIOME_TITLE_Y = 30
ENCOUNTER_TITLE_Y = 60


def get_default_card_dimensions():
    """Sets card dimensions in pixels (converts mm to pixels using 300 dpi)

    Returns
    -------
    int, int
        width and height in pixels
    """
    return int(63.5 * 300 / 25.4), int(88 * 300 / 25.4)


def draw_base_card(background_image_path, canvas_width, canvas_height):
    """Loads and resizes the background image

    Parameters
    ----------
    background_image_path : str
        The path to the background image
    canvas_width : int
        The width of the canvas to draw on
    canvas_height : int
        The height of the canvas to draw on

    Returns
    -------
    card
        the base card on which all other elements will be drawn
    draw
        the draw instance that provides draw methods
    """

    background_image = Image.open(background_image_path)

    new_width, new_height = calculate_new_image_dimensions_respecting_aspect_ratio(
        background_image, canvas_width, canvas_height
    )

    background_image = background_image.resize((new_width, new_height), Image.LANCZOS)

    card = crop_image_to_fit_canvas_dimensions(
        background_image, canvas_width, canvas_height
    )

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
    canvas_width : int
        The width of the canvas to drawn on
    """

    card_image = convert_image_to_rgba(card_image)

    card_image, calculated_card_image_width = resize_image(
        card_image, canvas_width, CARD_IMAGE_MARGIN
    )

    card_image, calculated_card_image_x = crop_image(
        card_image, canvas_width, calculated_card_image_width, CROP_MARGIN
    )

    card.paste(
        card_image, (calculated_card_image_x, CARD_IMAGE_DISTANCE_FROM_TOP), card_image
    )


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

    card_image_frame_height = calculate_height_of_image_according_to_width(
        card_image_frame, width
    )

    card_image_frame = card_image_frame.resize(
        (width, card_image_frame_height), Image.LANCZOS
    )

    return card_image_frame


def draw_card_frame(card_image_frame_path, card, canvas_width):
    """Draws the frame of a card around the card image

    Parameters
    ----------
    card_image_frame_path : str
        The path to the frame that will be drawn around the card image
    card : Image
        The card where the frame will be drawn
    height : int
        The height of the canvas
    width : int
        The width of the canvas
    """
    card_image_frame = load_card_image_frame(card_image_frame_path, canvas_width)

    card_image_frame_x = 0
    card_image_frame_y = 0

    card.paste(
        card_image_frame, (card_image_frame_x, card_image_frame_y), card_image_frame
    )


def resize_text_banner(banner_image, title_width, title_height):
    """Resizes the text banner according to the title's dimensions

    Parameters
    ----------
    banner_image : Image
        The image of the title banner
    title_width : int
        The width of the title
    title_height : int
        The height of the title
    """

    banner_width = title_width + 2 * TEXT_BANNER_PADDING
    banner_height = title_height + 2 * TEXT_BANNER_PADDING

    return banner_image.resize((banner_width, banner_height), Image.LANCZOS)


def draw_title_banner(
    title_banner_path, title_x, title_y, title_width, title_height, card
):
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


class MissingTitleYCoordinateError(Exception):
    "Raised when 'draw_title' has been called with a dictionary of values that doesn't contain 'title_y'"
    pass


def draw_title(draw_title_parameters):
    """Draws the title of the card

    Parameters
    ----------
    draw_title_parameters : dict
        A dictionary with all the necessary arguments to draw the title
    """

    # Add title text
    title_width, title_height = draw_title_parameters["draw"].textsize(
        draw_title_parameters["title"], draw_title_parameters["font"]
    )
    title_x = calculate_centered_x(title_width, draw_title_parameters["canvas_width"])

    if "title_y" not in draw_title_parameters:
        raise MissingTitleYCoordinateError(
            "The dictionary passed to 'draw_title' doesn't contain the key 'title_y'."
        )

    if draw_title_parameters["title_banner_path"] is not None:
        draw_title_banner(
            draw_title_parameters["title_banner_path"],
            title_x,
            draw_title_parameters["title_y"],
            title_width,
            title_height,
            draw_title_parameters["card"],
        )

    draw_text_with_shadow(
        draw_title_parameters["draw"],
        draw_title_parameters["title"],
        (title_x, draw_title_parameters["title_y"]),
        draw_title_parameters["font"],
        fill="white",
        shadow_offset=2,
        shadow_opacity=128,
    )
