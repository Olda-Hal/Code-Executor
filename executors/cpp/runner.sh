#!/bin/bash
echo "$CODE" > /app/program.cpp
g++ -o /app/program /app/program.cpp

if [ $? -eq 0 ]; then
    if [ ! -z "$INPUT" ]; then
        echo "$INPUT" | /app/program
    else
        /app/program
    fi
else
    echo "Compilation error"
    exit 1
fi