#!/bin/bash
python3 ./scripts/prepare.py
nohup socat  tcp-l:$1,fork system:"python3 ./scripts/main.py" &
