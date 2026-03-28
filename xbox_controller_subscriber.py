#!/usr/bin/env python3
"""
Xbox Controller Subscriber for ROS3

This script subscribes to the Xbox controller topic and prints the received inputs.
"""

import ros3 as rose
import sys
import os

# Add the ros3 Python module to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ros3', 'lang', 'python'))

def main():
    """
    Main function to create a ROS3 subscriber for Xbox controller inputs.
    """
    # Initialize the ROS3 node
    node = rose.Node("xbox_controller_subscriber")
    
    # Create a subscriber for the Xbox controller topic
    subscriber = node.subscriber("/xbox/controller")
    
    print("Xbox Controller Subscriber Started")
    print("Waiting for messages on /xbox/controller...")
    
    # Main loop
    while node.ok():
        # Read messages from the subscriber
        for message in subscriber:
            print(f"Received: {message}")
        
        # Sleep to reduce CPU usage
        rose.sleep(0.01)
    
    # Shutdown the node
    node.shutdown()

if __name__ == "__main__":
    main()
