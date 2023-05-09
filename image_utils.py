"""Image Utils

This script provides plenty of useful functions to process images related to creating a card.

This file can also be imported as a module and contains the following
functions:

    * convert_image_to_rgba - if necessary, a loaded image will get converted to RGBA
    * create_mask_with_rounded_corners - creates a mask image with rounded corners
    * apply_rounded_corners_to_card - applies a mask with rounded corners to a card image
    * load_card_image_frame - loads the frame for a card image
"""

from PIL import Image, ImageDraw


ROUNDED_CORNER_RADIUS = 30


def convert_image_to_rgba(image):
    """Converts a loaded image to RGBA if necessary

    Parameters
    ----------
    image : Image
        The image that will be converted to RGBA

    Returns
    -------
    Image
        the image, possibly converted to RGBA
    """
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    return image


def create_mask_with_rounded_corners(width, height):
    """Creates a mask image with rounded corners

    Parameters
    ----------
    width : int
        The width that the mask must have
    height : int
        The height that the mask must have

    Returns
    -------
    Image
        the image mask with rounded corners
    """

    mask = Image.new("L", (width, height), 0)
    mask_draw = ImageDraw.Draw(mask)

    mask_draw.ellipse(
        (0, 0, 2 * ROUNDED_CORNER_RADIUS, 2 * ROUNDED_CORNER_RADIUS), fill=255
    )  # Upper-left
    mask_draw.ellipse(
        (width - 2 * ROUNDED_CORNER_RADIUS, 0, width, 2 * ROUNDED_CORNER_RADIUS),
        fill=255,
    )  # Upper-right
    mask_draw.ellipse(
        (0, height - 2 * ROUNDED_CORNER_RADIUS, 2 * ROUNDED_CORNER_RADIUS, height),
        fill=255,
    )  # Lower-left
    mask_draw.ellipse(
        (
            width - 2 * ROUNDED_CORNER_RADIUS,
            height - 2 * ROUNDED_CORNER_RADIUS,
            width,
            height,
        ),
        fill=255,
    )  # Lower-right

    mask_draw.rectangle(
        (ROUNDED_CORNER_RADIUS, 0, width - ROUNDED_CORNER_RADIUS, height), fill=255
    )
    mask_draw.rectangle(
        (0, ROUNDED_CORNER_RADIUS, width, height - ROUNDED_CORNER_RADIUS), fill=255
    )

    return mask


def apply_rounded_corners_to_card(card):
    """Applies a mask with rounded corners to the card image

    Parameters
    ----------
    card : Image
        The card that will be made to have rounded corners

    """
    card.putalpha(create_mask_with_rounded_corners(card.width, card.height))


def calculate_new_image_dimensions_respecting_aspect_ratio(
    image, canvas_width, canvas_height
):
    bg_width, bg_height = image.size

    scale_factor_w = canvas_width / bg_width
    scale_factor_h = canvas_height / bg_height
    scale_factor = max(scale_factor_w, scale_factor_h)
    new_width = int(bg_width * scale_factor)
    new_height = int(bg_height * scale_factor)

    return new_width, new_height


def calculate_centered_x(image_width, canvas_width):
    return (canvas_width - image_width) // 2


def crop_image(card_image, canvas_width, calculated_card_image_width, crop_margin):
    card_image = crop_outer_boundaries_of_image(card_image, crop_margin)

    calculated_card_image_x = calculate_centered_x(
        calculated_card_image_width, canvas_width
    )

    calculated_card_image_x = recalculate_card_x_after_cropping(
        card_image, calculated_card_image_x, calculated_card_image_width
    )

    return card_image, calculated_card_image_x


def crop_image_to_fit_canvas_dimensions(image, canvas_width, canvas_height):
    left = (image.width - canvas_width) / 2
    top = (image.height - canvas_height) / 2
    right = (image.width + canvas_width) / 2
    bottom = (image.height + canvas_height) / 2

    return image.crop((left, top, right, bottom))


def crop_outer_boundaries_of_image(image, crop_margin):
    crop_x0 = int(image.width * crop_margin)
    crop_y0 = int(image.height * crop_margin)
    crop_x1 = image.width - crop_x0
    crop_y1 = image.height - crop_y0

    return image.crop((crop_x0, crop_y0, crop_x1, crop_y1))


def recalculate_card_x_after_cropping(
    card, calculated_card_x, calculated_card_image_width
):
    card_image_width_after_crop, _ = card.size
    width_difference = calculated_card_image_width - card_image_width_after_crop

    return calculated_card_x + width_difference // 2


def resize_image(image, canvas_width, margin):
    # Calculate the size and position of the card_image with added margin
    calculated_card_image_width = calculate_width_of_image_for_canvas(
        canvas_width, margin
    )
    calculated_card_image_height = calculate_height_of_image_according_to_width(
        image, calculated_card_image_width
    )

    # Resize and position the card_image
    image = image.resize(
        (calculated_card_image_width, calculated_card_image_height), Image.LANCZOS
    )

    return image, calculated_card_image_width


def calculate_width_of_image_for_canvas(canvas_width, margin):
    return canvas_width - 2 * margin


def calculate_height_of_image_according_to_width(image, width):
    return int(width * image.height / image.width)
