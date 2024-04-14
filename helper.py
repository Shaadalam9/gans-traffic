import os
from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip
import cv2
import params as params
from collections import defaultdict
import shutil
import numpy as np
import pandas as pd


class youtube_helper:

    def __init__(self):
        self.resolution = None
        self.video_title = None

    def download_video_with_resolution(self, video_id, resolutions=["720p","360p"], output_path="."):
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
