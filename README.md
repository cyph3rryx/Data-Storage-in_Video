# Data-Storage in Video

- A program that converts any type of file eg. zip, exe, jpg,etc...into frames into images where every part of the frame that is black represents zero and every part of frame that is white represents one. Because all the data on this world is zero and one and we just want to represent it as black and white.

- A converter that actually converts any file into a frame of youtube video where every frame is composed of blacks and whites. So in every seconds there are 24 frames that we are going to encode which means that every hour on youtube can store a 45GB of data.

## Steps to do so:

1. Read the input file as a stream of bytes.
2. Convert each byte into its binary representation (a sequence of 0's and 1's).
3. Divide the binary representation into groups of 8 bits (bytes).
4. Create a blank image frame with the desired size (e.g., 1080p).
5. Iterate over the groups of 8 bits and set the corresponding pixels on the image frame to black or white (0 or 255).
6. Repeat steps 4 and 5 until all the bytes in the input file have been processed.
7. Save each image frame as a JPEG or PNG file.
8. Use a video editing software to combine the image frames into a video file.
9. Upload the video file to YouTube.

> Note : Please keep in mind that converting any file into a video file with this method may result in extremely large file sizes, which may not be feasible for uploading to YouTube.
>
