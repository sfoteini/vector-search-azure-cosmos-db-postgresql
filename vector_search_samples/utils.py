import io
import requests
from textwrap import fill
from PIL import Image
import matplotlib.pyplot as plt
from azure.storage.blob import ContainerClient


def vectorize_image_with_filepath(
    image_filepath: str,
    endpoint: str,
    key: str,
    version: str,
) -> list[float] | None:
    """
    Generates a vector embedding for a local image using Azure AI Vision 4.0
    (Vectorize Image API).

    :param image_filepath: The image filepath.
    :param endpoint: The endpoint of the Azure AI Vision resource.
    :param key: The access key of the Azure AI Vision resource.
    :param version: The version of the API.
    :return: The vector embedding of the image.
    """
    with open(image_filepath, "rb") as img:
        data = img.read()

    # Vectorize Image API
    vision_api = endpoint + "retrieval:vectorizeImage" + version

    headers = {
        "Content-type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": key,
    }

    try:
        r = requests.post(vision_api, data=data, headers=headers)
        if r.status_code == 200:
            image_vector = r.json()["vector"]
            return image_vector
        else:
            print(
                f"An error occurred while processing {image_filepath}. "
                f"Error code: {r.status_code}."
            )
    except Exception as e:
        print(f"An error occurred while processing {image_filepath}: {e}")

    return None


def vectorize_image_with_url(
    image_url: str,
    endpoint: str,
    key: str,
    version: str,
) -> list[float] | None:
    """
    Generates a vector embedding for a remote image using Azure AI Vision 4.0
    (Vectorize Image API).

    :param image_url: The URL of the image.
    :param endpoint: The endpoint of the Azure AI Vision resource.
    :param key: The access key of the Azure AI Vision resource.
    :param version: The version of the API.
    :return: The vector embedding of the image.
    """
    # Vectorize Image API
    vision_api = endpoint + "retrieval:vectorizeImage" + version

    headers = {
        "Content-type": "application/json",
        "Ocp-Apim-Subscription-Key": key,
    }

    try:
        r = requests.post(vision_api, json={"url": image_url}, headers=headers)
        if r.status_code == 200:
            image_vector = r.json()["vector"]
            return image_vector
        else:
            print(
                f"An error occurred while processing {image_url}. "
                f"Error code: {r.status_code}."
            )
    except Exception as e:
        print(f"An error occurred while processing {image_url}: {e}")

    return None


def vectorize_text(
    text: str,
    endpoint: str,
    key: str,
    version: str,
) -> list[float] | None:
    """
    Generates a vector embedding for a text prompt using Azure AI Vision 4.0
    (Vectorize Text API).

    :param text: The text prompt.
    :param endpoint: The endpoint of the Azure AI Vision resource.
    :param key: The access key of the Azure AI Vision resource.
    :param version: The version of the API.
    :return: The vector embedding of the image.
    """
    # Vectorize Text API
    vision_api = endpoint + "retrieval:vectorizeText" + version

    headers = {
        "Content-type": "application/json",
        "Ocp-Apim-Subscription-Key": key
    }

    try:
        r = requests.post(vision_api, json={"text": text}, headers=headers)
        if r.status_code == 200:
            text_vector = r.json()["vector"]
            return text_vector
        else:
            print(
                f"An error occurred while processing the prompt '{text}'. "
                f"Error code: {r.status_code}."
            )
    except Exception as e:
        print(f"An error occurred while processing the prompt '{text}': {e}")

    return None


def display_image_grid(
    image_names: list[str],
    image_titles: list[str],
    figure_title: str,
    nrows: int,
    ncols: int,
    container_client: ContainerClient,
) -> None:
    """
    Displays a collection of images in a grid. The images are downloaded from
    an Azure Blob Storage container.

    :param image_names: A list containing the filenames of the images.
    :param image_titles: The title displayed alongside each image.
    :param figure_title: The title of the figure.
    :param nrows: The number of rows.
    :param ncols: The number of columns.
    :param container_client: A `ContainerClient` object.
    """
    num_images = len(image_names)

    # Download the images from Azure Blob Storage
    images_stream = [
        download_blob(
            image_filename=image_filename,
            container_client=container_client,
        )
        for image_filename in image_names
    ]

    # Display the images
    f, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10, 10))
    for i, ax in enumerate(axes.flat):
        if i < num_images:
            ax.imshow(Image.open(images_stream[i]))
            ax.set_title(fill(image_titles[i], 35), fontsize=8)
            ax.axis("off")
        else:
            ax.axis("off")
    f.suptitle(figure_title, fontsize=14)
    f.subplots_adjust(top=0.9)
    plt.show()


def download_blob(
    image_filename: str,
    container_client: ContainerClient,
) -> io.BytesIO:
    """
    Downloads an image from Azure Blob Storage and stores it in a binary stream.

    :param image_filename: The filename of the image.
    :param container_client: A `ContainerClient` object.
    :return: The image file as a binary stream.
    """
    blob_client = container_client.get_blob_client(image_filename)
    blob_image = blob_client.download_blob().readall()

    return io.BytesIO(blob_image)
