import pandas as pd
import params as params
from helper import youtube_helper
from moviepy.editor import VideoFileClip
import os
import numpy as np
import math
from PIL import Image

helper = youtube_helper()

df = pd.read_csv("mapping.csv")
youtube_links = df["video"]


def get_single_value_for_key(video_column, value_column, key):
    for video, duration in zip(video_column, value_column):
        if key in video:
            value = duration  # Convert duration to integer
            return value


def create_folder_structure(root_path):
    # Define folder names
    folders = ['train/A', 'train/B', 'val/A', 'val/B']

    # Create folders
    for folder in folders:
        folder_path = os.path.join(root_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        print("Created folder:", folder_path)


def extract_frames(video_file, frame_rate=2):
    clip = VideoFileClip(video_file)
    total_frames = math.ceil(clip.duration * frame_rate)
    frames = []

    for i in range(total_frames):
        frame_time = i / frame_rate
        frame = clip.get_frame(frame_time)
        frames.append(frame)

    return frames


for link in youtube_links:
    # Download the youtube video to the local system
    video_ids = [id.strip() for id in link.strip("[]").split(',')]
    for vid in video_ids:
        result = helper.download_video_with_resolution(video_id=vid, output_path=params.output_path)

        if result:
            video_file_path, video_title, resolution = result
        else:
            print("Download Failed")

        train_flag = get_single_value_for_key(df['video'], df['train'], video_title)

        input_file = video_file_path
        frames = extract_frames(input_file)

        create_folder_structure(root_path="data")

        if train_flag:
            for i, frame in enumerate(frames):
                rand_no = np.random.uniform()
                if rand_no < 0.8:
                    output_file = f"{params.train_A_path}/{video_title}_{i+1}.png"
                else:
                    output_file = f"{params.val_A_path}/{video_title}_{i+1}.png"
                img = Image.fromarray(frame)
                img.save(output_file)

        else:
            for i, frame in enumerate(frames):
                rand_no = np.random.uniform()
                if rand_no < 0.8:
                    output_file = f"{params.train_B_path}/{video_title}_{i+1}.png"
                else:
                    output_file = f"{params.val_B_path}/{video_title}_{i+1}.png"
                img = Image.fromarray(frame)
                img.save(output_file)
