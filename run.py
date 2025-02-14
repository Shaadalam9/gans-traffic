from helper import process_helper
import os

helper_ = process_helper()

videos_train_folder = os.path.join("..", "video", "train")
videos_test_folder = os.path.join("..", "video", "test")

# Get list of video files in the folder
video_files = [f for f in os.listdir(videos_train_folder) if
               os.path.isfile(os.path.join(videos_train_folder, f)) and f.endswith('.mp4')]

# Iterate through each video file and extract frames
for i, video_file in enumerate(video_files):
    video_path = os.path.join(videos_train_folder, video_file)
    # Split the frames into test and validate.
    # The index "i" used for determine the location of the frames of the two video.
    train_output_folder = os.path.join("data", "train", "A" if i % 2 == 0 else "B")
    val_output_folder = os.path.join("data", "val", "A" if i % 2 == 0 else "B")
    fps_video = helper_.extract_frames(video_path, train_output_folder, val_output_folder, 1, 0.8)


video_files = [f for f in os.listdir(videos_train_folder) if
               os.path.isfile(os.path.join(videos_train_folder, f)) and f.endswith('.mp4')]

# Iterate through each video file and extract frames
for i, video_file in enumerate(video_files):
    video_path = os.path.join(videos_train_folder, video_file)
    test_output_folder = os.path.join("data", "test", "A" if i % 2 == 0 else "B")
    val_output_folder = ""  # Provide an empty string instead of None to avoid type errors
    fps_video = helper_.extract_frames(video_path, test_output_folder, val_output_folder, 1, 1)
