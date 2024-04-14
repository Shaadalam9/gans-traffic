import os
import cv2
import math

# Function to extract frames from a video
def extract_frames(video_path, train_output_folder, val_output_folder, train_percentage, video_index):
    # Create train and validation output folders if they don't exist
    if not os.path.exists(train_output_folder):
        os.makedirs(train_output_folder)
    if not os.path.exists(val_output_folder):
        os.makedirs(val_output_folder)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Unable to open video file.")
        return

    # Get frame rate and total number of frames
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate total time of the video
    total_time = total_frames / fps

    # Calculate the number of frames for the first hour of footage
    num_frames_1hr = int(fps * 3600) if total_time >= 3600 else total_frames

    # Calculate number of frames for train and validation sets
    num_train_frames = min(math.ceil(num_frames_1hr * train_percentage), num_frames_1hr)
    num_val_frames = num_frames_1hr - num_train_frames

    # Iterate through the video and extract frames
    for i in range(num_frames_1hr):
        ret, frame = cap.read()
        if not ret:
            break

        # Decide whether to save in train or validation folder
        if i % 5 == 0:
            output_folder = val_output_folder
        else:
            output_folder = train_output_folder

        # Save frame as an image
        frame_filename = os.path.join(output_folder, f"frame_{i}.jpg")
        cv2.imwrite(frame_filename, frame)

    # Release the video capture object
    cap.release()

# Main function
def main():
    # Path to the folder containing videos
    videos_folder = "video"

    # Get list of video files in the folder
    video_files = [f for f in os.listdir(videos_folder) if os.path.isfile(os.path.join(videos_folder, f))]

    # Percentage of frames to be included in the train set
    train_percentage = 0.8

    # Iterate through each video file and extract frames
    for i, video_file in enumerate(video_files):
        video_path = os.path.join(videos_folder, video_file)
        train_output_folder = os.path.join("data", "train", "A" if i % 2 == 0 else "B")
        val_output_folder = os.path.join("data", "val", "A" if i % 2 == 0 else "B")
        extract_frames(video_path, train_output_folder, val_output_folder, train_percentage, i)

if __name__ == "__main__":
    main()
