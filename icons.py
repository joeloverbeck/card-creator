from PIL import Image

from image_utils import calculate_centered_x, convert_image_to_rgba, create_shadow_mask

BACK_ICON_SIZE = 300
BIOME_ICON_SIZE_IN_BIOME_CARD = 200
BIOME_ICON_SIZE_IN_ENCOUNTER_CARD = 100
BIOME_ICON_SIZE_IN_EXPLORATION_ZONE_CARD = 100
STRUGGLE_ICON_SIZE = 100

STRUGGLE_ICON_DISTANCE_FROM_BOTTOM = 220
BIOME_ICON_DISTANCE_FROM_BOTTOM_IN_BIOME_CARD = 350
BIOME_ICON_DISTANCE_FROM_BOTTOM_IN_ENCOUNTER_CARD = 425
BIOME_ICONS_DISTANCE_FROM_BOTTOM_IN_EXPLORATION_ZONE_CARD = 700

SHADOW_OFFSET = 1
SHADOW_OPACITY = 50

GAP_BETWEEN_ICONS = 10


def draw_shadow_for_icon(icon, starting_x, icons_y, card):
    # Create the shadow mask
    shadow_mask = create_shadow_mask(icon, SHADOW_OFFSET, SHADOW_OPACITY)

    # Draw the shadow
    card.paste(
        shadow_mask, (starting_x + SHADOW_OFFSET, icons_y + SHADOW_OFFSET), shadow_mask
    )


def draw_row_of_icons(icon_paths, icon_size, starting_x, icons_y, card):
    for icon_path in icon_paths:
        icon = Image.open(icon_path).resize((icon_size, icon_size), Image.LANCZOS)

        icon = convert_image_to_rgba(icon)

        draw_shadow_for_icon(icon, starting_x, icons_y, card)

        # Paste the icon on the card
        card.paste(icon, (starting_x, icons_y), icon)

        starting_x += icon.width + GAP_BETWEEN_ICONS


def calculate_total_width_of_icons(icon_paths, icon_size):
    total_icons_width = 0

    # Calculate the total width of the icons and the gaps
    for icon_path in icon_paths:
        icon = Image.open(icon_path).resize((icon_size, icon_size), Image.LANCZOS)
        total_icons_width += icon.width + GAP_BETWEEN_ICONS

    total_icons_width -= GAP_BETWEEN_ICONS  # Remove the gap after the last icon

    return total_icons_width


def draw_icons(icon_paths, card, icon_size, icons_y, canvas_height, canvas_width):
    """Draws the icons of the card

    Parameters
    ----------
    icon_paths : list
        Contains the paths to all the icons that will need to get drawn
    card : Image
        The base card upon which the icons will be drawn
    icons_y : int
        The y position where the icons will be drawn
    canvas_height : int
        The height of the canvas where the icons will be drawn
    canvas_width : int
        The width of the canvas where the icons will be drawn
    """

    total_icons_width = calculate_total_width_of_icons(icon_paths, icon_size)

    # Calculate the starting x-coordinate for the first icon
    starting_x = calculate_centered_x(total_icons_width, canvas_width)

    draw_row_of_icons(icon_paths, icon_size, starting_x, icons_y, card)


def draw_icon_in_absolute_center(
    icon_path, card, icon_size, canvas_height, canvas_width
):
    # Load the icon image
    icon = Image.open(icon_path).resize((icon_size, icon_size), Image.LANCZOS)

    # Calculate the center of the canvas
    canvas_center_x = canvas_width // 2
    canvas_center_y = canvas_height // 2

    # Calculate the top-left coordinates of the icon to place it in the center
    icon_x = canvas_center_x - (icon.width // 2)
    icon_y = canvas_center_y - (icon.height // 2)

    # Convert the icon to RGBA mode if necessary
    icon = convert_image_to_rgba(icon)

    draw_shadow_for_icon(icon, icon_x, icon_y, card)

    # Paste the icon onto the card at the calculated coordinates
    card.paste(icon, (icon_x, icon_y), icon)
