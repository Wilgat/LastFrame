#!/usr/bin/env python
from __future__ import print_function, unicode_literals

from ChronicleLogger import ChronicleLogger
import sys
import cv2
import os
import glob

def get_last_frame(video_path, output_path):
    """Extract the last frame from video and save it."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Cannot open video file.")
        return False

    # Method 1: Try by frame count (most accurate)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames > 1:
        cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(output_path, frame)
            cap.release()
            print(f"Success: Last frame saved as '{output_path}'")
            return True

    # Method 2: Fallback - seek to 99% of video
    cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0.99)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(output_path, frame)
        cap.release()
        print(f"Success: Last frame saved as '{output_path}' (using time-based seek)")
        return True

    # Method 3: Use millisecond seek
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps > 0:
        duration_ms = (total_frames / fps) * 1000
        cap.set(cv2.CAP_PROP_POS_MSEC, duration_ms - 100)  # 0.1s before end
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(output_path, frame)
            cap.release()
            print(f"Success: Last frame saved as '{output_path}' (millisecond seek)")
            return True

    cap.release()
    print("Failed: Could not extract the last frame.")
    return False


def main():
    # Find all .mp4 files in current directory (case-insensitive)
    mp4_files = glob.glob("*.mp4") + glob.glob("*.MP4") + glob.glob("*.Mp4")
    mp4_files = sorted(set(mp4_files))  # Remove duplicates, sort nicely

    if not mp4_files:
        print("No .mp4 videos found in the current folder!")
        print(f"Current directory: {os.getcwd()}")
        input("\nPress Enter to exit...")
        return

    # Display numbered list
    print("\nFound MP4 videos:\n")
    for i, filename in enumerate(mp4_files, 1):
        size_mb = os.path.getsize(filename) / (1024 * 1024)
        print(f"  {i:2d}. {filename}  ({size_mb:.1f} MB)")

    # Get user choice
    while True:
        try:
            choice = input(f"\nEnter video number (1-{len(mp4_files)}): ").strip()
            if not choice:
                print("Please enter a number.")
                continue
            idx = int(choice) - 1
            if 0 <= idx < len(mp4_files):
                selected_video = mp4_files[idx]
                break
            else:
                print(f"Please enter a number between 1 and {len(mp4_files)}.")
        except ValueError:
            print("Invalid input. Please type a number.")

    # Suggest default output: either output.png or video_name_last.png
    base_name = os.path.splitext(selected_video)[0]
    default_output = "output.png" if os.path.exists("output.png") == False else f"{base_name}_last.png"

    print(f"\nSelected: {selected_video}")

    # Ask for output filename
    user_output = input(f"Enter output image filename [default: {default_output}]: ").strip()
    if not user_output:
        output_path = default_output
    else:
        # Ensure it has an image extension
        if not user_output.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            output_path = user_output + ".png"
        else:
            output_path = user_output

    print(f"\nExtracting last frame from '{selected_video}'...")
    get_last_frame(selected_video, output_path)

    print(f"\nDone! Image saved as: {output_path}")
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()

