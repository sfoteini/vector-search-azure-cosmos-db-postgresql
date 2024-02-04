# Image similarity search on Azure Cosmos DB for PostgreSQL with pgvector

This project demonstrates the creation of an image similarity search application utilizing Azure Cosmos DB for PostgreSQL as a vector database and Azure AI Vision for generating embeddings. It serves as a starting point that can be used for the development of more sophisticated vector search solutions.

In this sample application, we will explore image similarity search on Azure Cosmos DB for PostgreSQL using the [SemArt Dataset](https://researchdata.aston.ac.uk/id/eprint/380/). This dataset contains approximately 21k paintings gathered from the Web Gallery of Art. Each painting comes with various attributes, like a title, description, and the name of the artist.

## Prerequisites

Before you start, ensure that you have the following prerequisites installed and configured:

* An Azure subscription - Create an [Azure free account](https://azure.microsoft.com/free/?WT.mc_id=AI-MVP-5004971) or an [Azure for Students account](https://azure.microsoft.com/free/students/?WT.mc_id=AI-MVP-5004971).

* An Azure AI Vision resource or a multi-service resource for Azure AI services - It is recommended to use the standard tier because the free tier allows only 20 transactions per minute.

    > The multi-modal embeddings APIs are available in the following regions: East US, France Central, Korea Central, North Europe, Southeast Asia, West Europe, West US.

* An Azure Storage account - [Create an Azure Storage account using the Azure CLI](https://learn.microsoft.com/azure/storage/blobs/storage-quickstart-blobs-cli?WT.mc_id=AI-MVP-5004971).

* An Azure Cosmos DB for PostgreSQL cluster - [Create an Azure Cosmos DB for PostgreSQL cluster in the Azure portal](https://learn.microsoft.com/azure/cosmos-db/postgresql/quickstart-create-portal?tabs=direct&WT.mc_id=AI-MVP-5004971). You should also [activate the pgvector extension](https://learn.microsoft.com/azure/cosmos-db/postgresql/howto-use-pgvector?WT.mc_id=AI-MVP-5004971#enable-extension).

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

| Sample | Description |
| ------ | ----------- |
| [Data Preprocessing](data_processing/data_preprocessing.ipynb) | Cleans up the SemArt Dataset and creates the final dataset that is utilized in our application. |
| [Embeddings Generation](data_processing/generate_embeddings.py) | Generates vector embeddings for the images in the dataset using the Azure AI Vision Vectorize Image API and creates the final dataset that is utilized in the image search application. |
| [Upload images to Azure Blob Storage](data_upload/upload_images_to_blob.py) | Creates an Azure Blob Storage container and uploads the paintings' images. |
| [Insert data to Azure Cosmos DB for PostgreSQL](data_upload/upload_data_to_postgresql.py) | Creates a table in the Azure Cosmos DB for PostgreSQL cluster and populates it with data from the dataset. |
| [Exact nearest neighbor search with pgvector](vector_search_samples/image_search.ipynb) | Demonstrates text-to-image and image-to-image search approaches, along with a simple method for metadata filtering. |

**More samples will be added soon!**

## Blog Posts

This repository hosts the source code for the "Image similarity search with pgvector" learning series.

* [Part 1: Use the Azure AI Vision multi-modal embeddings API for image retrieval](https://sfoteini.github.io/blog/use-the-azure-ai-vision-multi-modal-embeddings-api-for-image-retrieval/)
* [Part 2: Generate embeddings with Azure AI Vision multi-modal embeddings API](https://sfoteini.github.io/blog/generate-embeddings-with-azure-ai-vision-multi-modal-embeddings-api/)
* [Part 3: Store embeddings in Azure Cosmos DB for PostgreSQL with pgvector](https://sfoteini.github.io/blog/store-embeddings-in-azure-cosmos-db-for-postgresql-with-pgvector/)

*Feel free to experiment with the project and modify the code to meet your specific use cases and requirements!*
