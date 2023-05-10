import argparse
from card_elements import MissingTitleYCoordinateError

from card_setups import (
    FailedToCreateCardException,
    setup_biome_card,
    setup_biome_back_card,
    setup_encounter_card,
    setup_exploration_zone_card,
    setup_exploration_zone_back_card,
)
from file_utils import IncorrectImagePathException

RAW_IMAGES_DIRECTORY = "raw_images"


def main():
    parser = argparse.ArgumentParser(description="Card Generator")
    parser.add_argument(
        "type_of_card",
        help="Name of the type of card. The options are 'encounter', 'biome', 'exploration_zone'.",
    )

    args = parser.parse_args()

    if not args.type_of_card:
        print("Error: The name of the type of card to create can't be empty")
        return

    try:
        if args.type_of_card == "encounter":
            setup_encounter_card()
        elif args.type_of_card == "biome":
            setup_biome_card()
        elif args.type_of_card == "biome_back":
            setup_biome_back_card()
        elif args.type_of_card == "exploration_zone":
            setup_exploration_zone_card()
        elif args.type_of_card == "exploration_zone_back":
            setup_exploration_zone_back_card()
        else:
            print(f"Not implemented for type of card '{args.type_of_card}'")
            return
    except FailedToCreateCardException as exception:
        print(f"Failed to create a card from main.\nError: {exception}")
        return
    except IncorrectImagePathException as exception:
        print(
            f"Failed to create a card from main because some image path doesn't lead to an actual file.\nError: {exception}"
        )
        return


if __name__ == "__main__":
    main()
