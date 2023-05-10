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
    BIOME_TITLE_Y,
    ENCOUNTER_TITLE_Y,
    MissingTitleYCoordinateError,
    convert_image_to_rgba,
    draw_base_card,
    draw_card_frame,
    draw_card_image,
    draw_title,
    get_default_card_dimensions,
)
from file_utils import save_card_as_png
from fonts import BIOME_TITLE_FONT, ENCOUNTER_TITLE_FONT
from image_utils import (
    apply_rounded_corners_to_card,
)
from icons import (
    BACK_ICON_SIZE,
    BIOME_ICONS_DISTANCE_FROM_BOTTOM_IN_EXPLORATION_ZONE_CARD,
    BIOME_TYPE_ICON_DISTANCE_FROM_BOTTOM_IN_BIOME_CARD,
    BIOME_TYPE_ICON_DISTANCE_FROM_BOTTOM_IN_ENCOUNTER_CARD,
    BIOME_TYPE_ICON_SIZE_IN_BIOME_CARD,
    BIOME_TYPE_ICON_SIZE_IN_ENCOUNTER_CARD,
    BIOME_TYPE_ICON_SIZE_IN_EXPLORATION_ZONE_CARD,
    STRUGGLE_ICON_DISTANCE_FROM_BOTTOM,
    STRUGGLE_ICON_SIZE,
    draw_icon_in_absolute_center,
    draw_icons,
)






def prepare_to_draw_title(
    title, title_banner_path, font, title_y, canvas_width, card, draw
):
    draw_title_parameters = {
        "title": title,
        "title_banner_path": title_banner_path,
        "font": font,
        "canvas_width": canvas_width,
        "card": card,
        "draw": draw,
        "title_y": title_y,
    }

    try:
        draw_title(draw_title_parameters)
    except MissingTitleYCoordinateError as exception:
        raise MissingTitleYCoordinateError(
            f"Failed to draw the title of the card from 'prepare_to_draw_title'. Error: {exception}"
        )


def create_card(title, image_paths, card_type):
    """Creates a card given the passed title and the image paths.
    It also handles saving the created card to a PNG file.

    Parameters
    ----------
    title : str
        The title of the card that will be created. It can be None, as in the case of card backs
    image_paths : dict
        All the paths to the images that will be drawn on the card
    """

    canvas_width, canvas_height = get_default_card_dimensions()

    card, draw = draw_base_card(
        image_paths["background_image_path"], canvas_width, canvas_height
    )

    if "card_image_path" in image_paths.keys():
        draw_card_image(
            card,
            convert_image_to_rgba(Image.open(image_paths["card_image_path"])),
            canvas_width,
        )

    if "card_image_frame_path" in image_paths.keys():
        draw_card_frame(image_paths["card_image_frame_path"], card, canvas_width)

    if card_type == "encounter":
        card_type_data = {
            "font": ENCOUNTER_TITLE_FONT,
            "title_y": ENCOUNTER_TITLE_Y,
            "biome_type_icon_distance_from_bottom": BIOME_TYPE_ICON_DISTANCE_FROM_BOTTOM_IN_ENCOUNTER_CARD,
            "biome_type_icon_size": BIOME_TYPE_ICON_SIZE_IN_ENCOUNTER_CARD
        }
    elif card_type == "biome":
        card_type_data = {
            "font": BIOME_TITLE_FONT,
            "title_y": BIOME_TITLE_Y,
            "biome_type_icon_distance_from_bottom": BIOME_TYPE_ICON_DISTANCE_FROM_BOTTOM_IN_BIOME_CARD,
            "biome_type_icon_size": BIOME_TYPE_ICON_SIZE_IN_BIOME_CARD
        }
    elif card_type == "exploration_zone":
        card_type_data = {
            "font": ENCOUNTER_TITLE_FONT,
            "title_y": BIOME_TITLE_Y
        }

    title_banner_path = None

    if "title_banner_path" in image_paths.keys():
        title_banner_path = image_paths["title_banner_path"]

    if title is not None:
        prepare_to_draw_title(
            title, title_banner_path, card_type_data["font"], card_type_data["title_y"], canvas_width, card, draw
        )

    if "biome_type_path" in image_paths.keys():
        draw_icons(
            [image_paths["biome_type_path"]],
            card,
            card_type_data["biome_type_icon_size"],
            canvas_height - card_type_data["biome_type_icon_distance_from_bottom"],
            canvas_height,
            canvas_width,
        )

    if "struggle_icon_paths" in image_paths.keys():
        draw_icons(
            image_paths["struggle_icon_paths"],
            card,
            STRUGGLE_ICON_SIZE,
            canvas_height - STRUGGLE_ICON_DISTANCE_FROM_BOTTOM,
            canvas_height,
            canvas_width,
        )

    if "biome_icon_paths" in image_paths.keys():
        draw_icons(
            image_paths["biome_icon_paths"],
            card,
            BIOME_TYPE_ICON_SIZE_IN_EXPLORATION_ZONE_CARD,
            canvas_height - BIOME_ICONS_DISTANCE_FROM_BOTTOM_IN_EXPLORATION_ZONE_CARD,
            canvas_height,
            canvas_width,            
        )

    if "back_icon_path" in image_paths.keys():
        # Must draw the centered icon that should appear on the backs of each type of card.
        draw_icon_in_absolute_center(
            image_paths["back_icon_path"],
            card,
            BACK_ICON_SIZE,
            canvas_height,
            canvas_width,
        )

    apply_rounded_corners_to_card(card)

    save_card_as_png(title, card, card_type)
