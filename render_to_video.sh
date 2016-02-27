#!/bin/sh

rm *.png

flam3-render < test.flam3 && ffmpeg -y -framerate 30 -i %05d.png -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4 && open out.mp4
