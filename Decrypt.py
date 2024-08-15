from PIL import Image

def decode_image(image_input):
    """Decode a message from an image."""
    # If image_input is a PIL Image object, use it directly
    if isinstance(image_input, Image.Image):
        image = image_input
    else:
        # Otherwise, assume it is a file-like object or path and open it
        image = Image.open(image_input)

    binary_data = ""
    for y in range(image.height):
        for x in range(image.width):
            pixel = list(image.getpixel((x, y)))
            for n in range(3):
                binary_data += bin(pixel[n])[-1]

    binary_message = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded_message = ""
    for byte in binary_message:
        decoded_message += chr(int(byte, 2))
        if decoded_message[-3:] == "EOF":
            break
    return decoded_message[:-3]
