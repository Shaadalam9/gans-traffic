import pandas as pd
import params as params
from helper import youtube_helper
from moviepy.editor import VideoFileClip

helper = youtube_helper()

df = pd.read_csv("mapping.csv")
youtube_links = df["videos"]


def extract_clips(video_file, clip_duration=10):
    clip = VideoFileClip(video_file)
    total_duration = clip.duration
    clips = []

    start_time = 0
    end_time = clip_duration

    while end_time <= total_duration:
        subclip = clip.subclip(start_time, end_time)
        clips.append(subclip)
        start_time += clip_duration
        end_time += clip_duration

    # If the last clip is shorter than clip_duration, include it
    if start_time < total_duration:
        subclip = clip.subclip(start_time, total_duration)
        clips.append(subclip)

    return clips


for link in youtube_links:
    # Download the youtube video to the local system
    video_ids = [id.strip() for id in link.strip("[]").split(',')]
    for vid in video_ids:
        result = helper.download_video_with_resolution(video_id=vid, output_path=params.output_path)

        if result:
            video_file_path, video_title, resolution = result
            print(video_file_path, video_title, resolution)
            print(f"Video title: {video_title}")
            print(f"Video saved at: {video_file_path}")
        else:
            print("Download Failed")

        input_file = video_file_path
        output_prefix = video_title

        clips = extract_clips(input_file)

        for i, clip in enumerate(clips):
            output_file = f"{output_prefix}_{i+1}.mp4"
            clip.write_videofile(output_file)
