#!/bin/bash

python3 -m venv myenv && source myenv/bin/activate && \
python -m pip install pygame==2.6.1 opencv-python==4.12.0.88 && \
python3 src/main.py