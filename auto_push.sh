#!/bin/bash

# Navigate to the repository directory
cd /home/isuru/Desktop/RM

# Read the GitHub token from the file
GITHUB_TOKEN=$(cat /home/isuru/Desktop/RM/github_token.txt)

# Get the current date and time for the commit message
CURRENT_TIME=$(date +"%Y-%m-%d %H:%M:%S")

# Stage all changes, commit them with a timestamp, and push to GitHub
git add .
git commit -m "Automated commit at $CURRENT_TIME"
git push https://Tape-head-3d:${GITHUB_TOKEN}@github.com/Tape-head-3d/runtime-measuring-module-production.git
