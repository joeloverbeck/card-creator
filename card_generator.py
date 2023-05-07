"""Card Generator

This script creates a PNG file with a composite card given the paths to images
as well as the texts given.

This file can also be imported as a module and contains the following
functions:

    * save_card_as_png - saves the card as a PNG image given a title and the drawn card
    * create_card - creates a card given a title, the image paths, and a description text
"""

from PIL import Image

from card_elements import (
    convert_image_to_rgba,
    draw_base_card,
    draw_card_image,
    draw_title,
    draw_icons,
    draw_card_description,
)
from image_utils import (
    get_default_card_dimensions,
    load_card_image_frame,
    apply_rounded_corners_to_card,
)

OUTPUT_DIRECTORY = "output"


def save_card_as_png(title, card):
    """Saves the card image as a PNG file

    Parameters
    ----------
    title : str
        The title of the card, to use as part of the filename
    card : Image
        The image that will get saved to a PNG file
    """

    card.save(f"{OUTPUT_DIRECTORY}/{title}_card.png")


def create_card(title, text, image_paths):
    """Creates a card given the passed title, the text, and the image paths.
    It also handles saving the created card to a PNG file.

    Parameters
    ----------
    title : str
        The title of the card that will be created
    text : str
        The text that will be written on the card, other than the title.
    image_paths : dict
        All the paths to the images that will be drawn on the card
    """

    width, height = get_default_card_dimensions()

    card, draw = draw_base_card(image_paths["background_image_path"], width, height)

    # Load the card image and convert to RGBA mode if necessary
    draw_card_image(
        card, convert_image_to_rgba(Image.open(image_paths["card_image_path"])), width
    )

    card_image_frame = load_card_image_frame(
        image_paths["card_image_frame_path"], width
    )

    card_image_frame_x = 0
    card_image_frame_y = 0

    card.paste(
        card_image_frame, (card_image_frame_x, card_image_frame_y), card_image_frame
    )

    draw_title(title, width, draw)

    draw_card_description(text, draw)

    draw_icons(image_paths["icon_paths"], card, height)

    apply_rounded_corners_to_card(card)

    save_card_as_png(title, card)
