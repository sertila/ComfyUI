#!/bin/bash

# ComfyUI Update and Restart Script
# This script updates ComfyUI, custom nodes, and dependencies, then offers to restart

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "======================================"
echo "ComfyUI Update and Restart Utility"
echo "======================================"
echo ""

# Run the Python update script
echo "Running update script..."
python3 update_comfyui.py

UPDATE_EXIT_CODE=$?

if [ $UPDATE_EXIT_CODE -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "Update completed successfully!"
    echo "======================================"
    echo ""
    
    # Check if ComfyUI is currently running
    if pgrep -f "python.*main.py" > /dev/null; then
        echo "ComfyUI appears to be running."
        echo ""
        read -p "Would you like to restart ComfyUI now? (y/n) " -n 1 -r
        echo ""
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "Stopping ComfyUI..."
            pkill -f "python.*main.py" || true
            sleep 2
            
            echo "Starting ComfyUI..."
            python3 main.py &
            
            echo ""
            echo "ComfyUI has been restarted!"
            echo "Check the logs to ensure it started correctly."
        else
            echo "Restart cancelled. Please restart ComfyUI manually when ready."
        fi
    else
        echo "ComfyUI does not appear to be running."
        echo ""
        read -p "Would you like to start ComfyUI now? (y/n) " -n 1 -r
        echo ""
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "Starting ComfyUI..."
            python3 main.py &
            
            echo ""
            echo "ComfyUI has been started!"
        else
            echo "You can start ComfyUI manually by running: python3 main.py"
        fi
    fi
else
    echo ""
    echo "======================================"
    echo "Update failed with errors!"
    echo "======================================"
    echo "Please check the error messages above and resolve any issues."
    exit 1
fi

echo ""
echo "Done!"
