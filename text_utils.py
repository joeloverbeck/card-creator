from PIL import ImageColor


def draw_text_with_shadow(
    draw, text, position, font, fill, shadow_offset, shadow_opacity
):
    shadow_x, shadow_y = position
    shadow_x += shadow_offset
    shadow_y += shadow_offset

    if isinstance(fill, str) and fill == "white":
        shadow_fill = ImageColor.getcolor("black", "RGBA")

    # Convert fill to an RGBA tuple if it's a string color name
    if isinstance(fill, str):
        fill = ImageColor.getcolor(fill, "RGBA")

    shadow_color = (
        *shadow_fill[:-1],
        shadow_opacity,
    )  # Keep the same RGB values, change the alpha value

    # Draw the shadow text
    draw.text((shadow_x, shadow_y), text, font=font, fill=shadow_color)

    # Draw the main text
    draw.text(position, text, font=font, fill=fill)
