import argparse
from card_elements import MissingTitleYCoordinateError

from card_generation import create_biome_card, create_encounter_card

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
            create_encounter_card()
        elif args.type_of_card == "biome":
            create_biome_card()
        else:
            print(f"Not implemented for type of card '{args.type_of_card}'")
            return
    except MissingTitleYCoordinateError as exception:
        print(f"Failed to create a card from main. Error: {exception}")
        return


if __name__ == "__main__":
    main()
