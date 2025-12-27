#!/bin/bash
docker build -t 5noptiinstudentie .
xhost  +local:docker
docker run --rm -it \
  --device /dev/snd \
  -e SDL_AUDIODRIVER=alsa \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  5noptiinstudentie
xhost -local:docker
