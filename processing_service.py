import os
import requests
import shutil
import logging
import time

logging.basicConfig(level=logging.INFO)

api_url = "http://localhost:5000/get_image_embedding"
process_folder = "to_process"
processed_folder = "processed"
failed_folder = "failed"

if not os.path.exists(processed_folder):
    os.makedirs(processed_folder)
if not os.path.exists(failed_folder):
    os.makedirs(failed_folder)


def process_image(image_path):
    try:
        id = os.path.basename(image_path).split(".")[0]
        with open(image_path, "rb") as image_file:
            response = requests.post(
                api_url, files={"image": image_file}, data={"id": id}
            )
        if response.status_code == 200:
            shutil.move(image_path, processed_folder)
        else:
            shutil.move(image_path, failed_folder)
    except Exception as e:
        logging.error(f"Error processing {image_path}: {e}")
        shutil.move(image_path, failed_folder)


while True:
    for image_path in os.listdir(process_folder):
        full_image_path = os.path.join(process_folder, image_path)
        if os.path.isfile(full_image_path):
            process_image(full_image_path)
    time.sleep(5)
