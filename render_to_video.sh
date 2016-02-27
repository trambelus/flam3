#!/bin/sh

# assuming you just generated a bunch of frames with the filenames 00000.png, 00001.png, 00002.png etc.
ffmpeg -y -framerate 30 -i %05d.png -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4 && open out.mp4
