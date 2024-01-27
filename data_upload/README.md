# Insert data to Azure Cosmos DB for PostgreSQL

## Upload images to Azure Blob Storage

Run the *[upload_images_to_blob.py](upload_images_to_blob.py)* script to upload the images to an Azure Blob Storage container using the following command from the root folder:

```bash
python data_upload/upload_images_to_blob.py
```

The process of uploading the images to Azure Blob Storage can be summarized as follows:

1. Create a new container to store the images.

2. Retrieve the filenames of the images in the dataset.

3. Upload the images in the container, utilizing multiple threads via the `ThreadPoolExecutor` class.

## Insert data to Azure Cosmos DB for PostgreSQL table

The *[upload_data_to_postgresql.py](upload_data_to_postgresql.py)* creates a new table in your Azure Cosmos DB for PostgreSQL cluster and populates it with data. To execute the script, use the following command from the root folder:

```bash
python data_upload/upload_data_to_postgresql.py
```

To insert data into an Azure Cosmos DB for PostgreSQL table, we will proceed as follows:

1. Create a table to store the filenames of the images, their embeddings, and their associated metadata. All information is saved in the CSV file created in *[data_processing/generate_embeddings.py](../data_processing/generate_embeddings.py)*.

2. Insert the data from the CSV file into the table using the PostgreSQL `COPY` command.
