"""
Generates vector embeddings for images specified in the 'dataset/dataset.csv'
file using the Azure AI Vision Vectorize Image API. The resulting embeddings
are stored in the 'dataset/dataset_embeddings.csv' file.

To execute the script, use the following command from the root folder:
`python data_processing/generate_embeddings.py`

Author: Foteini Savvidou (GitHub @sfoteini)
"""

import os
import csv
from dotenv import load_dotenv
import pandas as pd
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

# Constants
BATCH_SIZE = 1000
MAX_WORKERS = 4
IMAGE_FILE_CSV_COLUMN_NAME = "image_file"
EMBEDDINGS_CSV_COLUMN_NAME = "vector"

# Directories
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)

# Load environemt file
load_dotenv(os.path.join(parent_dir, ".env"))
# Azure AI Vision credentials
vision_endpoint = os.getenv("VISION_ENDPOINT") + "computervision/"
vision_key = os.getenv("VISION_KEY")
vision_api_version = os.getenv("VISION_VERSION")
vectorize_img_url = vision_endpoint + "retrieval:vectorizeImage" + vision_api_version

# Datasets' folder
dataset_folder = os.path.join(parent_dir, "dataset")
dataset_filepath = os.path.join(dataset_folder, "dataset.csv")
embeddings_filepath = os.path.join(dataset_folder, "embeddings.csv")
final_dataset_filepath = os.path.join(dataset_folder, "dataset_embeddings.csv")

# Images' folder
images_folder = os.path.join(parent_dir, "semart_dataset", "images")


def main():
    # Set-up folder and embeddings file
    os.makedirs(dataset_folder, exist_ok=True)
    if os.path.exists(embeddings_filepath):
        os.remove(embeddings_filepath)

    # Get the names of image files
    image_names = load_image_filenames()
    print(f"Number of images in the dataset: {len(image_names)}")

    # Compute vector embeddings and save them in a csv file
    compute_embeddings(image_names)

    # Save the final dataset
    generate_dataset()


def load_image_filenames() -> list[str]:
    """
    Returns a list of filenames for the images in the dataset.

    :return: A list containing the filenames of the images.
    """
    with open(dataset_filepath, "r") as csv_file:
        csv_reader = csv.DictReader(
            csv_file,
            delimiter="\t",
            skipinitialspace=True,
        )
        image_filenames = [row[IMAGE_FILE_CSV_COLUMN_NAME] for row in csv_reader]

    return image_filenames


def get_image_embedding(image: str) -> list[float] | None:
    """
    Generates a vector embedding for an image using Azure AI Vision 4.0
    (Vectorize Image API).

    :param image: The image filepath.
    :return: The vector embedding of the image.
    """
    with open(image, "rb") as img:
        data = img.read()

    headers = {
        "Content-type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": vision_key,
    }

    try:
        r = requests.post(vectorize_img_url, data=data, headers=headers)
        if r.status_code == 200:
            image_vector = r.json()["vector"]
            return image_vector
        else:
            print(
                f"An error occurred while processing {image}. "
                f"Error code: {r.status_code}."
            )
    except Exception as e:
        print(f"An error occurred while processing {image}: {e}")

    return None


def compute_embeddings(image_names: list[str]) -> None:
    """
    Computes vector embeddings for the provided images and saves the embeddings
    alongside their corresponding image filenames in a CSV file.

    :param image_names: A list containing the filenames of the images.
    """
    image_names_batches = [
        image_names[i:(i + BATCH_SIZE)]
        for i in range(0, len(image_names), BATCH_SIZE)
    ]
    for batch in tqdm(range(len(image_names_batches)), desc="Computing embeddings"):
        images = image_names_batches[batch]
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            embeddings = list(
                tqdm(
                    executor.map(
                        lambda x: get_image_embedding(
                            image=os.path.join(images_folder, x),
                        ),
                        images,
                    ),
                    total=len(images),
                    desc=f"Processing batch {batch+1}",
                    leave=False,
                )
            )
        valid_data = [
            [images[i], str(embeddings[i])] for i in range(len(images))
            if embeddings[i] is not None
        ]
        save_data_to_csv(valid_data)


def save_data_to_csv(data: list[list[str]]) -> None:
    """
    Appends a list of image filenames and their associated embeddings to
    a CSV file.

    :param data: The data to be appended to the CSV file.
    """
    with open(embeddings_filepath, "a", newline="") as csv_file:
        write = csv.writer(csv_file)
        write.writerows(data)


def generate_dataset() -> None:
    """
    Appends the corresponding vectors to each column of the original dataset
    and saves the updated dataset as a CSV file.
    """
    dataset_df = pd.read_csv(dataset_filepath, sep="\t", dtype="string")
    embeddings_df = pd.read_csv(
        embeddings_filepath,
        dtype="string",
        names=[IMAGE_FILE_CSV_COLUMN_NAME, EMBEDDINGS_CSV_COLUMN_NAME],
    )
    final_dataset_df = dataset_df.merge(
        embeddings_df, how="inner", on=IMAGE_FILE_CSV_COLUMN_NAME
    )
    final_dataset_df.to_csv(final_dataset_filepath, index=False, sep="\t")


if __name__ == "__main__":
    main()
    print("Done!")
