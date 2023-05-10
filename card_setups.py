import toml

from card_elements import MissingTitleYCoordinateError
from card_generation import CardCreationFailedException, SavingCardFailedError, create_card
from file_utils import UnhandledCardTypeException, ensure_all_image_paths_exist


class FailedToCreateCardException(Exception):
    pass


def setup_biome_card():
    """Creates a biome card"""
    biome_data = toml.load("toml/biome_card.toml")

    title = biome_data["title"]
    background_image_path = biome_data["paths"]["background_image_path"]
    biome_icon_path = biome_data["paths"]["biome_icon_path"]

    image_paths = {
        "background_image_path": background_image_path,
        "biome_icon_path": biome_icon_path,
    }

    ensure_all_image_paths_exist(image_paths)

    try:
        create_card(title, image_paths, "biome")
    except MissingTitleYCoordinateError as exception:
        raise FailedToCreateCardException(
            f"Failed to create a card from 'setup_biome_card'.\nError: {exception}"
        )
    except SavingCardFailedError as exception:
        raise FailedToCreateCardException(
            f"I was unable to create a card from 'setup_biome_card'.\nError: {exception}"
        )
    except CardCreationFailedException as exception:
        raise FailedToCreateCardException(
            f"I was unable to create a card from 'setup_biome_card'.\nError: {exception}"
        )



def setup_biome_back_card():
    """Creates the back of a biome card"""
    biome_back_data = toml.load("toml/biome_back_card.toml")

    background_image_path = biome_back_data["paths"]["background_image_path"]
    back_icon_path = biome_back_data["paths"]["back_icon_path"]

    image_paths = {
        "background_image_path": background_image_path,
        "back_icon_path": back_icon_path,
    }

    ensure_all_image_paths_exist(image_paths)

    try:
        create_card(None, image_paths, "biome_back")
    except MissingTitleYCoordinateError as exception:
        raise FailedToCreateCardException(
            f"Failed to create a card from 'setup_biome_back_card'.\nError: {exception}"
        )
    except SavingCardFailedError as exception:
        raise FailedToCreateCardException(
            f"I was unable to create a card from 'setup_biome_back_card'.\nError: {exception}"
        )
    except CardCreationFailedException as exception:
        raise FailedToCreateCardException(
            f"I was unable to create a card from 'setup_biome_back_card'.\nError: {exception}"
        )


def setup_encounter_card():
    """Creates an encounter card"""
    # Load the data from the TOML file
    encounter_data = toml.load("toml/encounter_card.toml")

    title = encounter_data["title"]
    background_image_path = encounter_data["paths"]["background_image_path"]
    # title_banner_path = encounter_data["paths"]["title_banner_path"]
    card_image_path = encounter_data["paths"]["card_image_path"]
    card_image_frame_path = encounter_data["paths"]["card_image_frame_path"]
    biome_icon_path = encounter_data["paths"]["biome_icon_path"]
    struggle_icon_paths = [
        icon["value"] for icon in encounter_data["paths"]["struggle_icon_paths"]
    ]

    image_paths = {
        "background_image_path": background_image_path,
        # "title_banner_path": title_banner_path,
        "card_image_path": card_image_path,
        "card_image_frame_path": card_image_frame_path,
        "biome_icon_path": biome_icon_path,
        "struggle_icon_paths": struggle_icon_paths,
    }

    ensure_all_image_paths_exist(image_paths)

    try:
        create_card(title, image_paths, "encounter")
    except MissingTitleYCoordinateError as exception:
        raise FailedToCreateCardException(
            f"Failed to create a card from 'setup_encounter_card'.\nError: {exception}"
        )
    except SavingCardFailedError as exception:
        raise FailedToCreateCardException(
            f"I was unable to create a card from 'setup_encounter_card'.\nError: {exception}"
        )
    except CardCreationFailedException as exception:
        raise FailedToCreateCardException(
            f"I was unable to create a card from 'setup_encounter_card'.\nError: {exception}"
        )


def setup_exploration_zone_card():
    """Setups the necessary data to create an exploration zone card"""
    # Load the data from the TOML file
    exploration_zone_data = toml.load("toml/exploration_zone.toml")

    title = exploration_zone_data["title"]
    background_image_path = exploration_zone_data["paths"]["background_image_path"]

    biome_icon_paths = [
        icon["value"] for icon in exploration_zone_data["paths"]["biome_icon_paths"]
    ]

    image_paths = {
        "background_image_path": background_image_path,
        "biome_icon_paths": biome_icon_paths,
    }

    ensure_all_image_paths_exist(image_paths)

    try:
        create_card(title, image_paths, "exploration_zone")
    except MissingTitleYCoordinateError as exception:
        raise FailedToCreateCardException(
            f"Failed to create a card from 'setup_exploration_zone_card'.\nError: {exception}"
        )
    except SavingCardFailedError as exception:
        raise FailedToCreateCardException(
            f"I was unable to create a card from 'setup_exploration_zone_card'.\nError: {exception}"
        )
    except CardCreationFailedException as exception:
        raise FailedToCreateCardException(
            f"I was unable to create a card from 'setup_exploration_zone_card'.\nError: {exception}"
        )


def setup_exploration_zone_back_card():
    """Creates the back of an exploration zone card"""

    # Load the data from the TOML file
    exploration_zone_back_data = toml.load("toml/exploration_zone_back.toml")

    background_image_path = exploration_zone_back_data["paths"]["background_image_path"]
    back_icon_path = exploration_zone_back_data["paths"]["back_icon_path"]

    image_paths = {
        "background_image_path": background_image_path,
        "back_icon_path": back_icon_path,
    }

    ensure_all_image_paths_exist(image_paths)

    try:
        create_card(None, image_paths, "exploration_zone_back")
    except MissingTitleYCoordinateError as exception:
        raise FailedToCreateCardException(
            f"Failed to create a card from 'setup_exploration_zone_back_card'.\nError: {exception}"
        )
    except SavingCardFailedError as exception:
        raise FailedToCreateCardException(
            f"I was unable to create a card from 'setup_exploration_zone_back_card'.\nError: {exception}"
        )
    except CardCreationFailedException as exception:
        raise FailedToCreateCardException(
            f"I was unable to create a card from 'setup_exploration_zone_back_card'.\nError: {exception}"
        )
