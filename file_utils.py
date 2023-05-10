import os

from errors import UnhandledCardTypeException

OUTPUT_DIRECTORY = "output"


class IncorrectImagePathException(Exception):
    pass


def check_file_exists(path):
    return os.path.exists(path)


def ensure_all_image_paths_exist(image_paths):
    for key, value in image_paths.items():
        if not isinstance(value, list):
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




def save_card_as_png(title, card, card_type):
    """Saves the card image as a PNG file

    Parameters
    ----------
    title : str
        The title of the card, to use as part of the filename
    card : Image
        The image that will get saved to a PNG file
    """

    if card_type == "biome" or card_type == "biome_back":
        card_type_directory = "biomes"
    elif card_type == "encounter":
        card_type_directory = "encounters"
    elif card_type == "exploration_zone" or card_type == "exploration_zone_back":
        card_type_directory = "exploration_zones"
    else:
        raise UnhandledCardTypeException(
            f"Failed to save a card to a file: can't handle card type '{card_type}'"
        )

    full_path = format(f"{OUTPUT_DIRECTORY}/{card_type_directory}")

    if not os.path.exists(full_path):
        os.makedirs(full_path)

    filename = f"{full_path}/{title}_card.png"

    card.save(filename)

    print(f"Card '{filename}' saved successfully.")
