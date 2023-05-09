import toml

from card_generator import create_card

RAW_IMAGES_DIRECTORY = "raw_images"


def main():
    # Load the data from the TOML file
    encounter_data = toml.load("toml/encounter_card.toml")

    title = encounter_data["title"]
    background_image_path = encounter_data["paths"]["background_image_path"]
    title_banner_path = encounter_data["paths"]["title_banner_path"]
    card_image_path = encounter_data["paths"]["card_image_path"]
    card_image_frame_path = encounter_data["paths"]["card_image_frame_path"]
    icon_paths = [icon["value"] for icon in encounter_data["paths"]["icon_paths"]]

    image_paths = {
        "background_image_path": background_image_path,
        "title_banner_path": title_banner_path,
        "card_image_path": card_image_path,
        "card_image_frame_path": card_image_frame_path,
        "icon_paths": icon_paths,
    }

    create_card(
        title,
        image_paths,
    )


if __name__ == "__main__":
    main()
