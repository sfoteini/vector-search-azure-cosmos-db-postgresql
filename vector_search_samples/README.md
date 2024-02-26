# Vector Search Code Samples

This directory includes notebooks designed to showcase the vector search capabilities of the `pgvector` extension on Azure Cosmos DB for PostgreSQL. Before running these notebooks, ensure that you have set up your working environment and your Azure Cosmos DB for PostgreSQL table as outlined in the [project description](../README.md).

![Image similarity search workflow](../docs/images/vector-search-flow.png)

The image similarity search workflow is summarized as follows:

1. Use the Vectorize Image API or the Vectorize Text API to generate vector embeddings of an image or text, respectively.
2. To calculate similarity and retrieve images, use `SELECT` statements and the built-it vector operators of the PostgreSQL database.
3. Display the retrieved images using the `matplotlib` package.

## Exact Nearest Neighbor Search

In the *[image_search.ipynb](image_search.ipynb)* Jupyter Notebook, you will build a basic image similarity search application using the Azure AI Vision multi-modal embeddings APIs and Azure Cosmos DB for PostgreSQL. You will explore both text-to-image and image-to-image search approaches, along with a simple method for metadata filtering.

## Approximate Nearest Neighbor Search with IVFFlat Index

In the *[image_search_ivfflat_index.ipynb](image_search_ivfflat_index.ipynb)* Jupyter Notebook, we'll explore how to find similar images using the IVFFlat index of the pgvector extension on Azure Cosmos DB for PostgreSQL and see how well the index performs compared to exact search.

## Approximate Nearest Neighbor Search with HNSW Index

In the *[image_search_hnsw_index.ipynb](image_search_hnsw_index.ipynb)* Jupyter Notebook, we'll explore how to find similar images using the HNSW index of the pgvector extension on Azure Cosmos DB for PostgreSQL and see how well the index performs compared to exact search.
