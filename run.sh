#!/bin/bash
python3 prepare.py
nohup socat  tcp-l:$1,fork system:"python3 ./main.py" &