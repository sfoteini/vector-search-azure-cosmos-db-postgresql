# Image similarity search on Azure Cosmos DB for PostgreSQL with pgvector

This project demonstrates the creation of an image similarity search application utilizing Azure Cosmos DB for PostgreSQL as a vector database and Azure AI Vision for generating embeddings. It serves as a starting point that can be used for the development of more sophisticated vector search solutions.

In this sample application, we will explore image similarity search on Azure Cosmos DB for PostgreSQL using the [SemArt Dataset](https://researchdata.aston.ac.uk/id/eprint/380/). This dataset contains approximately 21k paintings gathered from the Web Gallery of Art. Each painting comes with various attributes, like a title, description, and the name of the artist.

## Prerequisites

Before you start, ensure that you have the following prerequisites installed and configured:

* An Azure subscription - Create an [Azure free account](https://azure.microsoft.com/free/?WT.mc_id=AI-MVP-5004971) or an [Azure for Students account](https://azure.microsoft.com/free/students/?WT.mc_id=AI-MVP-5004971).

* An Azure AI Vision resource or a multi-service resource for Azure AI services - It is recommended to use the standard tier because the free tier allows only 20 transactions per minute.

    > The multi-modal embeddings APIs are available in the following regions: East US, France Central, Korea Central, North Europe, Southeast Asia, West Europe, West US.

* Python 3.10, Visual Studio Code, Jupyter Notebook, and Jupyter Extension for Visual Studio Code.

## Set-up your working environment

Before running the Python scripts and Jupyter Notebooks, you should:

1. Clone this repository to to have it locally available.

2. Download the [SemArt Dataset](https://researchdata.aston.ac.uk/id/eprint/380/) into the *semart_dataset* directory.

3. Create a [virtual environment](https://docs.python.org/3/library/venv.html) and activate it.

4. Install the required Python packages using the following command:

    ```bash
    pip install -r requirements.txt
    ```

5. Generate a *.env* file by using the provided *[.env.sample](.env.sample)* file from this repository.

## How to use the samples

### Data Preprocessing

For our application, we'll be working with a subset of the original dataset. Alongside the image files, we aim to retain associated metadata like the title, author's name, and description for each painting.

In the *[data_preprocessing.ipynb](data_processing/data_preprocessing.ipynb)* Jupyter Notebook, you will take the following steps:

1. Clean up the text descriptions by removing special characters to minimize errors related to character encoding.

2. Clean up the names of the artists, addressing encoding issues for some artists' names.

3. Exclude artists with fewer than 15 paintings from the dataset, along with other data we won't be using.

After these steps, the final dataset will comprise 11,206 images of paintings.

### Vector Embeddings Generation

Run the *[generate_embeddings.py](data_processing/generate_embeddings.py)* script to compute the embeddings of all the images using the following command from the root folder:

```bash
python data_processing/generate_embeddings.py
```

The final dataset is saved in the *dataset_embeddings.csv* file. To generate embeddings for the images, our process can be summarized as follows:

1. Retrieve the filenames of the images in the dataset.

2. Divide the data into batches, and for each batch, perform the following steps:

    1. Compute the vector embedding for each image in the batch using the Vectorize Image API of Azure AI Vision.

    2. Save the vector embeddings of the images along with the filenames into a file.

3. Update the dataset by inserting the vector embedding of each image.

<br>

**More samples will be added soon!**

## Blog Posts

This repository hosts the source code for the "Image similarity search with pgvector" learning series.

* [Part 1: Use the Azure AI Vision multi-modal embeddings API for image retrieval](https://sfoteini.github.io/blog/use-the-azure-ai-vision-multi-modal-embeddings-api-for-image-retrieval/)
* [Part 2: Generate embeddings with Azure AI Vision multi-modal embeddings API](https://sfoteini.github.io/blog/generate-embeddings-with-azure-ai-vision-multi-modal-embeddings-api/)

*Feel free to experiment with the project and modify the code to meet your specific use cases and requirements!*
