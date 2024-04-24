import os
import cv2


class process_helper():

    def __init__(self):
        pass

    # Function to extract frames from a video
    def extract_frames(self, video_path, train_output_folder, val_output_folder, _time_, train_percentage=0.8):
        # Create train and validation output folders if they don't exist
        if not os.path.exists(train_output_folder):
            os.makedirs(train_output_folder)
        if val_output_folder is not None:
            if not os.path.exists(val_output_folder):
                os.makedirs(val_output_folder)

        # Open the video file
        print(video_path)
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error: Unable to open video file.")
            return

        # Get frame rate and total number of frames
        fps = cap.get(cv2.CAP_PROP_FPS)  # Pass this fps for future
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Calculate total time of the video
        total_time = total_frames / fps

        # Calculate the number of frames for the first hour of footage
        num_frames_time = int(fps * _time_ * 60) if total_time >= (_time_ * 60) else total_frames

        # Iterate through the video and extract frames
        for i in range(num_frames_time):
            ret, frame = cap.read()
            if not ret:
                break

            # Decide whether to save in train or validation folder
            if val_output_folder is not None:
                if i % int(1/(1-train_percentage)) == 0:
                    output_folder = val_output_folder
                else:
                    output_folder = train_output_folder

            else:
                output_folder = train_output_folder

            # Save frame as an image
            frame_filename = os.path.join(output_folder, f"frame_{i}.jpg")
            cv2.imwrite(frame_filename, frame)

        # Release the video capture object
        cap.release()
        return fps

    def images_to_video(self, image_folder, output_video_path, ends_with, fps=60):
        # Get the list of image files in the folder
        image_files = [f for f in os.listdir(image_folder) if f.startswith("frame_") and f.endswith(ends_with)]

        # Ensure the list is sorted by frame number
        image_files.sort(key=lambda x: int(x.split('_')[1]))

        # Get the first image to determine dimensions
        first_image = cv2.imread(os.path.join(image_folder, image_files[0]))
        height, width, _ = first_image.shape

        # Define the video codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

        # Write each image to the video
        for image_file in image_files:
            image_path = os.path.join(image_folder, image_file)
            frame = cv2.imread(image_path)
            out.write(frame)

        # Release the VideoWriter object
        out.release()
