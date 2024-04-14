import cv2
import os

def save_frames(video_path, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    # Get the frame rate and total number of frames
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the number of frames to capture for 10 minutes
    ten_minute_frames = int(10 * 60 * fps)

    # Determine the number of frames to process
    frames_to_process = min(ten_minute_frames, total_frames)

    # Read and save frames
    for frame_count in range(frames_to_process):
        ret, frame = cap.read()
        if not ret:
            break

        # Save the frame as an image
        frame_path = os.path.join(output_folder, f"frame_{frame_count}.jpg")
        cv2.imwrite(frame_path, frame)

    # Release the video capture object
    cap.release()

if __name__ == "__main__":
    # Define the paths
    video_folder = "video"
    output_folder_A = "data/test/val/A"
    output_folder_B = "data/test/val/B"

    # Process video A
    video_path_A = os.path.join(video_folder, "13th_apr_17.00.mov")
    save_frames(video_path_A, output_folder_A)
    print("Frames from video A saved successfully.")

    # Process video B
    video_path_B = os.path.join(video_folder, "13th_apr_21.00.mov")
    save_frames(video_path_B, output_folder_B)
    print("Frames from video B saved successfully.")
