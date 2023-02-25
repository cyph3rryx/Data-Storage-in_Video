import os
from PIL import Image

# Define the size of each frame
FRAME_WIDTH = 1920
FRAME_HEIGHT = 1080

# Define the output directory for the frames
OUTPUT_DIR = 'frames/'

def convert_file_to_frames(input_file_path):
    # Open the input file and read its contents as bytes
    with open(input_file_path, 'rb') as input_file:
        file_bytes = input_file.read()

    # Convert the file bytes to a binary string representation
    binary_string = ''.join(format(byte, '08b') for byte in file_bytes)

    # Calculate the total number of frames needed to represent the binary string
    num_frames = (len(binary_string) // (FRAME_WIDTH * FRAME_HEIGHT)) + 1

    # Iterate over the binary string and create a new frame for each group of bits
    for i in range(num_frames):
        # Create a new blank image frame
        frame = Image.new('1', (FRAME_WIDTH, FRAME_HEIGHT))

        # Determine the starting and ending index for this frame's bits
        start_idx = i * FRAME_WIDTH * FRAME_HEIGHT
        end_idx = min(start_idx + FRAME_WIDTH * FRAME_HEIGHT, len(binary_string))

        # Iterate over the bits in this frame's range and set the corresponding pixels in the frame
        for j, bit in enumerate(binary_string[start_idx:end_idx]):
            x = j % FRAME_WIDTH
            y = j // FRAME_WIDTH
            pixel_value = 0 if bit == '0' else 255
            frame.putpixel((x, y), pixel_value)

        # Save the frame as a PNG file
        frame.save(os.path.join(OUTPUT_DIR, f'frame_{i:06d}.png'))
