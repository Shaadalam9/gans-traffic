import cv2
import os

def images_to_video(image_folder, output_video_path,ends_with, fps=60):
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

if __name__ == "__main__":
    # Define the paths
    # image_folder = "results/v2c_experiment/test_1/images"
    # output_video_path = "output_video_fake_A.mp4"
    # ends_with = "_fake_A.png"

    # # Convert images to video
    # images_to_video(image_folder, output_video_path, ends_with)
    # print("Video fake A created successfully.")

    image_folder = "results/v2c_experiment/test_1/images"
    output_video_path = "output_video_fake_B.mp4"
    ends_with = "_fake_B.png"

    # Convert images to video
    images_to_video(image_folder, output_video_path, ends_with)
    print("Video fake B created successfully.")


    image_folder = "results/v2c_experiment/test_1/images"
    output_video_path = "output_video_real_A.mp4"
    ends_with = "_real_A.png"

    # Convert images to video
    images_to_video(image_folder, output_video_path, ends_with)
    print("Video real A created successfully.")

    image_folder = "results/v2c_experiment/test_1/images"
    output_video_path = "output_video_real_B.mp4"
    ends_with = "_real_B.png"

    # Convert images to video
    images_to_video(image_folder, output_video_path, ends_with)
    print("Video real B created successfully.")
