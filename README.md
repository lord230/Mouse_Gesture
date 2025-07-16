# Hand Gesture Controlled Mouse for the Differently Abled

This project enables users to control their computer mouse and scrolling functionality using hand gestures detected via webcam. It is especially designed to help individuals with physical disabilities interact with computers more easily and independently.

## Features

- Move the mouse cursor using your index finger
- Perform a mouse click by bringing the thumb and index finger together
- Scroll up by raising 4 fingers
- Scroll down by folding all 4 fingers

## How It Works

The system uses a webcam to capture hand landmarks through MediaPipe. Based on the finger positions and gestures, the mouse pointer is moved, clicked, or scrolling actions are triggered using PyAutoGUI.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/lord230/hand_v_3.py.git
cd hand-gesture-mouse

```

## Requirements
-Python 3.7 to 3.10
- Webcam
- Windows, Linux, or macOS

## Future Improvements
- Right-click gesture
- Drag-and-drop gesture
- On-screen gesture overlay
