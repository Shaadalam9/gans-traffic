from helper import process_helper

helper_ = process_helper()

# Define the paths
image_folder = "results/v2c_experiment/test_1/images"

# Making video ffrom frames for fake video A
output_video_path = "output_video_fake_A.mp4"
ends_with = "_fake_A.png"
helper_.images_to_video(image_folder, output_video_path, ends_with)
print("Video fake A created successfully.")


# Making video ffrom frames for fake video B
output_video_path = "output_video_fake_B.mp4"
ends_with = "_fake_B.png"
helper_.images_to_video(image_folder, output_video_path, ends_with)
print("Video fake B created successfully.")


# Making video ffrom frames for real video A
output_video_path = "output_video_real_A.mp4"
ends_with = "_real_A.png"
helper_.images_to_video(image_folder, output_video_path, ends_with)
print("Video real A created successfully.")


# Making video ffrom frames for real video B
output_video_path = "output_video_real_B.mp4"
ends_with = "_real_B.png"
helper_.images_to_video(image_folder, output_video_path, ends_with)
print("Video real B created successfully.")
