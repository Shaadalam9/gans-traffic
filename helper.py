import os
from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
import cv2
from ultralytics import YOLO
import params as params
from collections import defaultdict
import shutil
import numpy as np
import pandas as pd


class youtube_helper:

    def __init__(self):
        self.model = params.model
        self.resolution = None
        self.video_title = None

    def download_video_with_resolution(self, video_id, resolutions=["720p", "480p", "360p"], output_path="."):
        try:
            youtube_url = f'https://www.youtube.com/watch?v={video_id}'
            print(youtube_url)
            youtube_object = YouTube(youtube_url)
            for resolution in resolutions:
                video_streams = youtube_object.streams.filter(res=f"{resolution}").all()
                if video_streams:
                    self.resolution = resolution
                    print(f"Got the video in {resolution}")
                    break

            if not video_streams:
                print(f"No {resolution} resolution available for '{youtube_object.title}'.")
                return None

            selected_stream = video_streams[0]

            video_file_path = f"{output_path}/{video_id}.mp4"
            print("Youtube video download in progress...")
            # Comment the below line to automatically download with video in "video" folder
            selected_stream.download(output_path, filename=f"{video_id}.mp4")

            print(f"Download of '{youtube_object.title}' in {resolution} completed successfully.")
            self.video_title = youtube_object.title
            return video_file_path, video_id, resolution

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def extract_video_clips(video_path, clip_length=10):
        # Open the video file
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error: Unable to open video file.")
            return

        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps

    # Create output folder to store video clips
        output_folder = 'video_clips'
        os.makedirs(output_folder, exist_ok=True)

        clip_count = 1
        start_frame = 0
        while start_frame < total_frames:
            # Set start and end frames for the clip
            end_frame = min(start_frame + clip_length * fps, total_frames)

            # Read video frames between start_frame and end_frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
            current_frame = start_frame
            while current_frame < end_frame:
                ret, frame = cap.read()
                if not ret:
                    break
                current_frame += 1

                # Write frame to output video clip
                output_path = os.path.join(output_folder, f"clip_{clip_count}.mp4")
                if current_frame == start_frame + 1:
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    out = cv2.VideoWriter(output_path, fourcc, fps, (frame.shape[1], frame.shape[0]))
                out.write(frame)

            # Release the output video writer
            out.release()

            # Move to next clip
            start_frame = end_frame
            clip_count += 1

        # Release the video capture object
        cap.release()
        print(f"Video decomposed into {clip_count-1} clips of {clip_length} seconds each.")
