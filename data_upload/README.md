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

## Insert data to Azure Cosmos DB for PostgreSQL table and create an IVFFlat index

The *[upload_data_to_postgresql_ivfflat.py](upload_data_to_postgresql_ivfflat.py)* creates a new table in your Azure Cosmos DB for PostgreSQL cluster, populates it with data, and creates an IVFFlat index. To execute the script, use the following command from the root folder:

```bash
python data_upload/upload_data_to_postgresql_ivfflat.py
```

To insert data into an Azure Cosmos DB for PostgreSQL table, we will follow the process presented in [Insert data to Azure Cosmos DB for PostgreSQL table](#insert-data-to-azure-cosmos-db-for-postgresql-table). The IVFFlat index is created after the completion of the data insertion process.

According to the pgvector repository, the optimal number of lists is calculated as `rows/1000` for datasets with up to 1 million rows, and as `sqrt(rows)` for datasets exceeding 1 million rows. In our case, we will use `lists=11`.

## Insert data to Azure Cosmos DB for PostgreSQL table and create an HNSW index

The *[upload_data_to_postgresql_hnsw.py](upload_data_to_postgresql_hnsw.py)* creates a new table in your Azure Cosmos DB for PostgreSQL cluster, populates it with data, and creates an HNSW index. To execute the script, use the following command from the root folder:

```bash
python data_upload/upload_data_to_postgresql_hnsw.py
```

To insert data into an Azure Cosmos DB for PostgreSQL table, we will follow the process presented in [Insert data to Azure Cosmos DB for PostgreSQL table](#insert-data-to-azure-cosmos-db-for-postgresql-table). The HNSW index is created after the completion of the data insertion process. (It can also be created before adding any data to the table.)

When creating the HNSW index, we will use the default values for the maximum number of connections per layer (`m=16`) and the size of the dynamic candidate list for constructing the graph (`ef_construction=64`).
