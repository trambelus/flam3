#!/bin/sh

rm *.png

flam3-render < test.flam3 && \
ffmpeg -y -framerate 30 -i %05d.png -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4 && \
ffmpeg -y -i out.mp4 -r 30 -filter:v "setpts=0.57142857142*PTS" faster.mp4 && \
ffmpeg -y -i ~/playground/waves.mp3 -i faster.mp4 -acodec aac -strict -2 -vcodec libx264 -shortest with_audio.mp4 && \
open with_audio.mp4
