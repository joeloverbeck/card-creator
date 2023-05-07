from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIRECTORY = "output"

def create_card(title, background_image_path, card_image_path, card_image_mask_path, text, icon_paths):
    # Set card dimensions in pixels (convert mm to pixels using 300 dpi)
    width, height = int(63.5 * 300 / 25.4), int(88 * 300 / 25.4)

    # Load and resize the background image
    card = Image.open(background_image_path).resize((width, height), Image.ANTIALIAS)
    draw = ImageDraw.Draw(card)

    

    # Load the card image and convert to RGBA mode if necessary
    card_image = Image.open(card_image_path)
    if card_image.mode != "RGBA":
        card_image = card_image.convert("RGBA")

    # Calculate the size and position of the card_image
    card_image_width = width
    card_image_height = int(card_image_width * card_image.height / card_image.width)
    card_image_x = 0
    card_image_y = 0

    # Resize and position the card_image
    card_image = card_image.resize((card_image_width, card_image_height), Image.ANTIALIAS)

    # Load the card image mask and resize it to match the card_image dimensions
    card_image_mask = Image.open(card_image_mask_path).resize(card_image.size)
    
    card.paste(card_image, (card_image_x, card_image_y), card_image)

    # Add title text
    title_font = ImageFont.truetype("arial.ttf", 24)
    title_width, _ = draw.textsize(title, font=title_font)
    title_x = (width - title_width) // 2
    draw.text((title_x, 10), title, font=title_font, fill="black")


    # Add card text
    text_font = ImageFont.truetype("arial.ttf", 18)
    draw.text((10, card_image_y + card_image_height + 10), text, font=text_font, fill="black")

    # Add icons
    icon_x = 10
    icon_y = height - 50
    for icon_path in icon_paths:
        icon = Image.open(icon_path).resize((40, 40), Image.ANTIALIAS)

        if icon.mode != "RGBA":
            icon = icon.convert("RGBA")
            
        card.paste(icon, (icon_x, icon_y), icon)
        icon_x += 50

    # Create a mask with rounded corners
    radius = 30
    mask = Image.new("L", (width, height), 0)
    mask_draw = ImageDraw.Draw(mask)
    
    mask_draw.ellipse((0, 0, 2 * radius, 2 * radius), fill=255)  # Upper-left
    mask_draw.ellipse((width - 2 * radius, 0, width, 2 * radius), fill=255)  # Upper-right
    mask_draw.ellipse((0, height - 2 * radius, 2 * radius, height), fill=255)  # Lower-left
    mask_draw.ellipse((width - 2 * radius, height - 2 * radius, width, height), fill=255)  # Lower-right
    
    mask_draw.rectangle((radius, 0, width - radius, height), fill=255)
    mask_draw.rectangle((0, radius, width, height - radius), fill=255)

    # Apply the mask to the card
    card.putalpha(mask)

    # Save the card as a PNG image
    card.save(f"{OUTPUT_DIRECTORY}/{title}_card.png")