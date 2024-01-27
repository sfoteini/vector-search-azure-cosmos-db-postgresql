"""
Uploads the images specified in the 'dataset/dataset_embeddings.csv'
file to a new Azure Blob Storage container.

To execute the script, use the following command from the root folder:
`python data_upload/upload_images_to_blob.py`

Author: Foteini Savvidou (GitHub @sfoteini)
"""

import os
import csv
import sys
from dotenv import load_dotenv
from azure.storage.blob import (
    BlobServiceClient,
    ContainerClient,
    ContentSettings,
)
from azure.core.exceptions import ResourceExistsError
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# Constants
MAX_WORKERS = 4
IMAGE_FILE_CSV_COLUMN_NAME = "image_file"

# Directories
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)

# Load environemt file
load_dotenv(os.path.join(parent_dir, ".env"), override=True)
# Azure Blob Storage credentials
blob_account_name = os.getenv("BLOB_ACCOUNT_NAME")
blob_account_key = os.getenv("BLOB_ACCOUNT_KEY")
blob_endpoint_suffix = os.getenv("BLOB_ENDPOINT_SUFFIX")
blob_connection_string = (
    f"DefaultEndpointsProtocol=https;AccountName={blob_account_name};"
    f"AccountKey={blob_account_key};EndpointSuffix={blob_endpoint_suffix}"
)
container_name = os.getenv("CONTAINER_NAME")

# Dataset's folder
dataset_folder = os.path.join(parent_dir, "dataset")
dataset_filepath = os.path.join(dataset_folder, "dataset_embeddings.csv")

# Images' folder
images_folder = os.path.join(parent_dir, "semart_dataset", "images")

# Content-Type for blobs
content_settings = ContentSettings(content_type="image/jpeg")


def main():
    # Create Azure Blob Storage client
    blob_service_client = BlobServiceClient.from_connection_string(
        conn_str=blob_connection_string,
    )

    # Create a new container
    try:
        container_client = blob_service_client.create_container(
            name=container_name,
            public_access="blob",
        )
    except ResourceExistsError:
        sys.exit(f"A container with name {container_name} already exists.")

    # Find the URLs of the images in the dataset
    images = load_image_filenames()

    print(f"Number of images in the dataset: {len(images)}")
    print(f"Uploading images to container '{container_name}'")

    # Upload images to blob storage
    upload_images(images=images, container_client=container_client)


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


def upload_blob_from_local_file(
    image_filepath: str,
    container_client: ContainerClient,
) -> None:
    """
    Uploads a local image file to Azure Blob Storage.

    :param image_filepath: The filepath of the image to upload.
    :param container_client: A ContainerClient object.
    """
    blob_name = os.path.basename(image_filepath)
    try:
        blob_client = container_client.get_blob_client(blob=blob_name)
        with open(image_filepath, mode="rb") as data:
            blob_client.upload_blob(
                data=data,
                overwrite=True,
                content_settings=content_settings,
            )
    except Exception as e:
        print(
            f"Couldn't upload image {blob_name} to Azure Storage Account due "
            f"to error: {e}"
        )


def upload_images(images: list[str], container_client: ContainerClient) -> None:
    """
    Uploads a collection of local image files to Azure Blob Storage.

    :param images: The names of the images to upload.
    :param container_client: A ContainerClient object.
    """
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        list(
            tqdm(
                executor.map(
                    lambda x: upload_blob_from_local_file(
                        image_filepath=os.path.join(images_folder, x),
                        container_client=container_client,
                    ),
                    images,
                ),
                total=len(images),
            )
        )


if __name__ == "__main__":
    main()
    print("Done!")
