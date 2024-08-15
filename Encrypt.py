from PIL import Image

def to_bin(data):
    return ''.join(format(ord(i), '08b') for i in data)

def encode_image(image, message):
    encoded_image = image.copy()
    width, height = image.size
    message += "EOF"
    binary_message = to_bin(message)
    binary_message += '0' * (width * height * 3 - len(binary_message))
    data_index = 0
    for y in range(height):
        for x in range(width):
            if data_index < len(binary_message):
                pixel = list(encoded_image.getpixel((x, y)))
                for n in range(3):  
                    if data_index < len(binary_message):
                        pixel[n] = pixel[n] & 0b11111110 | int(binary_message[data_index])
                        data_index += 1
                encoded_image.putpixel((x, y), tuple(pixel))
    return encoded_image
