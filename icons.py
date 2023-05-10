from PIL import Image, ImageDraw

from image_utils import calculate_centered_x, convert_image_to_rgba, create_shadow_mask

BIOME_TYPE_ICON_SIZE_IN_BIOME_CARD = 200
BIOME_TYPE_ICON_SIZE_IN_ENCOUNTER_CARD = 100
STRUGGLE_ICON_SIZE = 100
STRUGGLE_ICON_DISTANCE_FROM_BOTTOM = 220
BIOME_TYPE_ICON_DISTANCE_FROM_BOTTOM_IN_BIOME_CARD = 350
BIOME_TYPE_ICON_DISTANCE_FROM_BOTTOM_IN_ENCOUNTER_CARD = 425


def draw_shadow_for_icon(icon, starting_x, icons_y, card):
    # Define the shadow parameters
    shadow_offset = 2
    shadow_opacity = 80  # Lower value for more subtle effect (0-255)

    # Create the shadow mask
    shadow_mask = create_shadow_mask(icon, shadow_offset, shadow_opacity)

    # Draw the shadow
    card.paste(shadow_mask, (starting_x + shadow_offset, icons_y + shadow_offset), shadow_mask)


def draw_row_of_icons(icon_paths, icon_size, starting_x, icons_y, card, gap=5):
    for icon_path in icon_paths:
        icon = Image.open(icon_path).resize((icon_size, icon_size), Image.LANCZOS)

        icon = convert_image_to_rgba(icon)

        draw_shadow_for_icon(icon, starting_x, icons_y, card)

        # Paste the icon on the card
        card.paste(icon, (starting_x, icons_y), icon)

        starting_x += icon.width + gap


def calculate_total_width_of_icons_and_gap(icon_paths, icon_size, gap=5):
    total_icons_width = 0

    # Calculate the total width of the icons and the gaps
    for icon_path in icon_paths:
        icon = Image.open(icon_path).resize((icon_size, icon_size), Image.LANCZOS)
        total_icons_width += icon.width + gap

    total_icons_width -= gap  # Remove the gap after the last icon

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

    total_icons_width = calculate_total_width_of_icons_and_gap(icon_paths, icon_size)

    # Calculate the starting x-coordinate for the first icon
    starting_x = calculate_centered_x(total_icons_width, canvas_width)

    draw_row_of_icons(icon_paths, icon_size, starting_x, icons_y, card)
