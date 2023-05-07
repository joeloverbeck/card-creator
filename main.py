from card_creation import create_card

RAW_IMAGES_DIRECTORY = "raw_images"


def main():
    title = "Sample Card"
    background_image_path = RAW_IMAGES_DIRECTORY + "/background_image.png"
    card_image_path = RAW_IMAGES_DIRECTORY + "/card_image.png"
    card_image_mask_path = RAW_IMAGES_DIRECTORY + "/card_image_mask_FINAL.png"
    text = "Card description goes here."
    icon_paths = [
        RAW_IMAGES_DIRECTORY + "/icon1.png",
        RAW_IMAGES_DIRECTORY + "/icon2.png",
    ]
    create_card(title, background_image_path, card_image_path, card_image_mask_path, text, icon_paths)


if __name__ == "__main__":
    main()
