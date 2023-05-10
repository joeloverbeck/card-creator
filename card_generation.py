"""Card Generator

This script creates a PNG file with a composite card given the paths to images
as well as the texts given.

This file can also be imported as a module and contains the following
functions:

    * save_card_as_png - saves the card as a PNG image given a title and the drawn card
    * create_card - creates a card given a title, the image paths, and a description text
"""


import os
import toml

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
from file_utils import check_file_exists
from fonts import BIOME_TITLE_FONT, ENCOUNTER_TITLE_FONT
from image_utils import (
    apply_rounded_corners_to_card,
)
from icons import (
    BIOME_TYPE_ICON_DISTANCE_FROM_BOTTOM_IN_BIOME_CARD,
    BIOME_TYPE_ICON_DISTANCE_FROM_BOTTOM_IN_ENCOUNTER_CARD,
    BIOME_TYPE_ICON_SIZE_IN_BIOME_CARD,
    BIOME_TYPE_ICON_SIZE_IN_ENCOUNTER_CARD,
    STRUGGLE_ICON_DISTANCE_FROM_BOTTOM,
    STRUGGLE_ICON_SIZE,
    draw_icons,
)

OUTPUT_DIRECTORY = "output"


def save_card_as_png(title, card, card_type):
    """Saves the card image as a PNG file

    Parameters
    ----------
    title : str
        The title of the card, to use as part of the filename
    card : Image
        The image that will get saved to a PNG file
    """

    if card_type == "biome":
        card_type_directory = "biomes"
    elif card_type == "encounter":
        card_type_directory = "encounters"
    else:
        print(f"Failed to save a card to a file: can't handle card type '{card_type}'")
        return

    full_path = format(f"{OUTPUT_DIRECTORY}/{card_type_directory}")

    if not os.path.exists(full_path):
        os.makedirs(full_path)

    card.save(f"{full_path}/{title}_card.png")


def create_biome_card():
    """Creates a biome card"""
    biome_data = toml.load("toml/biome_card.toml")

    title = biome_data["title"]
    background_image_path = biome_data["paths"]["background_image_path"]
    biome_type_path = biome_data["paths"]["biome_type_path"]

    image_paths = {
        "background_image_path": background_image_path,
        "biome_type_path": biome_type_path,
    }

    try:
        create_card(title, image_paths, "biome")
    except MissingTitleYCoordinateError as exception:
        raise MissingTitleYCoordinateError(
            f"Failed to create a card from 'create_biome_card'. Error: {exception}"
        )


class IncorrectImagePathException(Exception):
    pass


def create_encounter_card():
    """Creates an encounter card"""
    # Load the data from the TOML file
    encounter_data = toml.load("toml/encounter_card.toml")

    title = encounter_data["title"]
    background_image_path = encounter_data["paths"]["background_image_path"]
    # title_banner_path = encounter_data["paths"]["title_banner_path"]
    card_image_path = encounter_data["paths"]["card_image_path"]
    card_image_frame_path = encounter_data["paths"]["card_image_frame_path"]
    biome_type_path = encounter_data["paths"]["biome_type_path"]
    struggle_icon_paths = [
        icon["value"] for icon in encounter_data["paths"]["struggle_icon_paths"]
    ]

    image_paths = {
        "background_image_path": background_image_path,
        # "title_banner_path": title_banner_path,
        "card_image_path": card_image_path,
        "card_image_frame_path": card_image_frame_path,
        "biome_type_path": biome_type_path,
        "struggle_icon_paths": struggle_icon_paths,
    }

    for key, value in image_paths.items():
        if key != "struggle_icon_paths":
            if not check_file_exists(value):
                raise IncorrectImagePathException(
                    f"The file for '{key}' does not exist. Path: {value}"
                )
        else:
            for index, icon_path in enumerate(value):
                if not check_file_exists(icon_path):
                    raise IncorrectImagePathException(
                        f"The file for '{key}' at index {index} does not exist. Path: {icon_path}"
                    )

    try:
        create_card(title, image_paths, "encounter")
    except MissingTitleYCoordinateError as exception:
        raise MissingTitleYCoordinateError(
            f"Failed to create a card from 'create_encounter_card'. Error: {exception}"
        )


def create_card(title, image_paths, card_type):
    """Creates a card given the passed title and the image paths.
    It also handles saving the created card to a PNG file.

    Parameters
    ----------
    title : str
        The title of the card that will be created
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
        font = ENCOUNTER_TITLE_FONT
        title_y = ENCOUNTER_TITLE_Y
        biome_type_icon_distance_from_bottom = (
            BIOME_TYPE_ICON_DISTANCE_FROM_BOTTOM_IN_ENCOUNTER_CARD
        )
        biome_type_icon_size = BIOME_TYPE_ICON_SIZE_IN_ENCOUNTER_CARD
    elif card_type == "biome":
        font = BIOME_TITLE_FONT
        title_y = BIOME_TITLE_Y
        biome_type_icon_distance_from_bottom = (
            BIOME_TYPE_ICON_DISTANCE_FROM_BOTTOM_IN_BIOME_CARD
        )
        biome_type_icon_size = BIOME_TYPE_ICON_SIZE_IN_BIOME_CARD

    title_banner_path = None

    if "title_banner_path" in image_paths.keys():
        title_banner_path = image_paths["title_banner_path"]

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
            f"Failed to draw the title of the card from 'create_card'. Error: {exception}"
        )

    if "biome_type_path" in image_paths.keys():
        draw_icons(
            [image_paths["biome_type_path"]],
            card,
            biome_type_icon_size,
            canvas_height - biome_type_icon_distance_from_bottom,
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

    apply_rounded_corners_to_card(card)

    save_card_as_png(title, card, card_type)
