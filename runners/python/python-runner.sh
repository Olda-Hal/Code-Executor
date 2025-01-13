#!/bin/bash

echo "$CODE" > script.py
output=$(python script.py "$INPUT")
echo "$output"