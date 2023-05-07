import os
import unittest
from PIL import Image, ImageDraw
from card_elements import draw_base_card, draw_card_image
from main import RAW_IMAGES_DIRECTORY


class TestDrawCardImage(unittest.TestCase):
    def setUp(self):
        self.valid_background_image_path = (
            RAW_IMAGES_DIRECTORY + "/background_image.png"
        )
        self.invalid_background_image_path = "path/to/invalid/background_image.jpg"
        self.valid_card_image_path = RAW_IMAGES_DIRECTORY + "/card_image.png"
        self.invalid_card_image_path = "path/to/invalid/card_image.jpg"
        self.width = 300
        self.height = 500

    def test_valid_base_card_valid_card_image(self):
        base_card, _ = draw_base_card(
            self.valid_background_image_path, self.width, self.height
        )
        card_image = Image.open(self.valid_card_image_path)

        try:
            draw_card_image(base_card, card_image, self.width)
        except Exception as e:
            self.fail(f"Error: {e}")

    def test_valid_base_card_invalid_card_image(self):
        base_card, _ = draw_base_card(
            self.valid_background_image_path, self.width, self.height
        )

        with self.assertRaises(FileNotFoundError):
            card_image = Image.open(self.invalid_card_image_path)

    def test_invalid_base_card_valid_card_image(self):
        with self.assertRaises(FileNotFoundError):
            base_card, _ = draw_base_card(
                self.invalid_background_image_path, self.width, self.height
            )

    def test_invalid_base_card_invalid_card_image(self):
        with self.assertRaises(FileNotFoundError):
            base_card, _ = draw_base_card(
                self.invalid_background_image_path, self.width, self.height
            )

        with self.assertRaises(FileNotFoundError):
            card_image = Image.open(self.invalid_card_image_path)


if __name__ == "__main__":
    unittest.main()
