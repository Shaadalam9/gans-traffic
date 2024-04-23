from helper import process_helper
import os

helper_ = process_helper()

videos_train_folder = "video/train"
videos_test_folder = "video/test"

# Get list of video files in the folder
video_files = [f for f in os.listdir(videos_train_folder) if os.path.isfile(os.path.join(videos_train_folder, f))]

# Iterate through each video file and extract frames
for i, video_file in enumerate(video_files):
    video_path = os.path.join(videos_train_folder, video_file)
    # Split the frames into test and validate.
    # The index "i" used for determine the location of the frames of the two video.
    train_output_folder = os.path.join("data", "train", "A" if i % 2 == 0 else "B")
    val_output_folder = os.path.join("data", "val", "A" if i % 2 == 0 else "B")

    fps_video = helper_.extract_frames(video_path, train_output_folder, val_output_folder, 0.8)
