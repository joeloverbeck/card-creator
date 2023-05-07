from card_generator import create_card

RAW_IMAGES_DIRECTORY = "raw_images"


def main():
    title = "Sample Card"
    text = "Card description goes here."

    image_paths = {
        "background_image_path": RAW_IMAGES_DIRECTORY + "/background_image.png",
        "card_image_path": RAW_IMAGES_DIRECTORY + "/card_image.png",
        "card_image_frame_path": RAW_IMAGES_DIRECTORY + "/card_image_frame_FINAL.png",
        "icon_paths": [
            RAW_IMAGES_DIRECTORY + "/icon1.png",
            RAW_IMAGES_DIRECTORY + "/icon2.png",
        ],
    }

    create_card(
        title,
        text,
        image_paths,
    )


if __name__ == "__main__":
    main()
