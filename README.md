✊ Gesture Shutdown
Not quite my tempo.

Control your computer with nothing but a gesture.

This project uses computer vision and real-time hand tracking to detect when you close your fist. When the gesture is detected consistently, the system executes a shutdown command instantly.

No buttons.
No clicks.
Just precision and timing.

Like a conductor stopping the orchestra — one motion ends the performance.

🎬 Concept

In music, a conductor controls an entire orchestra with a flick of the wrist.

In this project, a single gesture controls your computer.

When the system detects a closed fist, it interprets it as the signal to end the session — triggering a system shutdown.

Gesture → Detection → Confirmation → Command.

Everything happens in real time.

⚡ Features

🎥 Real-time webcam tracking

✋ Hand landmark detection using MediaPipe

✊ Fist gesture recognition

🧠 Temporal smoothing to avoid false triggers

💻 Automatic system shutdown

🌍 Cross-platform support (Windows / macOS / Linux)

🧠 How It Works

The system analyzes hand landmarks detected by MediaPipe.

Each finger is evaluated using two conditions:

Vertical position check
If the fingertip is below its joint, it is considered folded.

Distance check
If the fingertip is closer to the wrist than the finger base, it is considered folded.

If multiple fingers are folded, the system interprets the hand as a fist.

To prevent accidental triggers, detections are smoothed across several frames before executing the shutdown command.

🪄 Gesture Logic
Camera Frame
      ↓
Hand Detection (MediaPipe)
      ↓
Landmark Analysis
      ↓
Finger Fold Detection
      ↓
Fist Classification
      ↓
Frame Smoothing Filter
      ↓
System Shutdown

Precision matters.

Just like tempo.
