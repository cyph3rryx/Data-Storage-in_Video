import os
import math
import threading
from PIL import Image
import imageio

# Define the size of each frame
FRAME_WIDTH = 1920
FRAME_HEIGHT = 1080

# Define the output directory for the frames
OUTPUT_DIR = 'frames/'

# Define the maximum number of threads to use for frame generation
MAX_THREADS = 8

def compress_data(file_bytes):
    # Compress the input file bytes by using a simple run-length encoding algorithm
    compressed_bytes = []
    curr_bit = file_bytes[0]
    count = 1
    for bit in file_bytes[1:]:
        if bit == curr_bit:
            count += 1
        else:
            compressed_bytes.extend([curr_bit] * count)
            curr_bit = bit
            count = 1
    compressed_bytes.extend([curr_bit] * count)
    return compressed_bytes

def convert_file_to_frames(input_file_path, output_file_path):
    # Open the input file and read its contents as bytes
    with open(input_file_path, 'rb') as input_file:
        file_bytes = input_file.read()

    # Compress the file bytes using a simple run-length encoding algorithm
    compressed_bytes = compress_data(file_bytes)

    # Calculate the total number of frames needed to represent the compressed binary data
    num_frames = math.ceil(len(compressed_bytes) / (FRAME_WIDTH * FRAME_HEIGHT))

    # Use multi-threading to generate frames in parallel
    num_threads = min(num_frames, MAX_THREADS)
    frames_per_thread = num_frames // num_threads
    threads = []
    for i in range(num_threads):
        start_frame = i * frames_per_thread
        end_frame = start_frame + frames_per_thread
        if i == num_threads - 1:
            end_frame = num_frames
        thread = threading.Thread(target=generate_frames, args=(compressed_bytes, start_frame, end_frame))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

    # Combine the generated frames into a video using imageio
    image_files = sorted(os.listdir(OUTPUT_DIR))
    images = [imageio.imread(os.path.join(OUTPUT_DIR, filename)) for filename in image_files]
    fps = 24
    video_codec = 'h264'
    output_path = f'{output_file_path}.{video_codec}'
    imageio.mimsave(output_path, images, fps=fps, codec=video_codec)

def generate_frames(compressed_bytes, start_frame, end_frame):
    # Iterate over the specified range of frames and generate an image for each one
    for frame_num in range(start_frame, end_frame):
        # Calculate the start and end indices of the compressed binary data for this frame
        start_index = frame_num * FRAME_WIDTH * FRAME_HEIGHT
        end_index = start_index + FRAME_WIDTH * FRAME_HEIGHT

        # Create a new image with the desired dimensions
        image = Image.new('1', (FRAME_WIDTH, FRAME_HEIGHT))

        # Set each pixel in the image based on the corresponding bit in the compressed binary data
        for i in range(start_index, end_index):
            x = (i - start_index) % FRAME_WIDTH
            y = (i - start_index) // FRAME_WIDTH
            bit = compressed_bytes[i]
            color = 255 if bit == 1 else 0
            image.putpixel((x, y), color)

        # Save the image as a BMP file in the output directory
        frame_filename = f'{frame_num:06d}.bmp'
        frame_path = os.path.join(OUTPUT_DIR, frame_filename)
        image.save(frame_path)
        
if __name__ == '__main__':
    # Get the path of the input file from the user
    input_file_path = input('Enter the path of the input file: ').strip()

    # Get the desired output file name from the user
    output_file_path = input('Enter the desired name of the output file (without extension): ').strip()

    # Convert the input file to frames and save them in the output directory
    convert_file_to_frames(input_file_path, output_file_path)

    print('Done.')
