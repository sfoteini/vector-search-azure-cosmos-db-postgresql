# Data Processing

This directory contains Python code samples designed for cleaning up the [SemArt Dataset](https://researchdata.aston.ac.uk/id/eprint/380/) and generating embeddings for the images.

## Data Preprocessing

For our application, we'll be working with a subset of the original dataset. Alongside the image files, we aim to retain associated metadata like the title, artist's name, and description for each painting.

In the *[data_preprocessing.ipynb](data_preprocessing.ipynb)* Jupyter Notebook, you will take the following steps:

1. Clean up the text descriptions by removing special characters to minimize errors related to character encoding.

2. Clean up the names of the artists, addressing encoding issues for some artists' names.

3. Exclude artists with fewer than 15 paintings from the dataset, along with other data we won't be using.

After these steps, the final dataset will comprise 11,206 images of paintings.

## Vector Embeddings Generation

Run the *[generate_embeddings.py](generate_embeddings.py)* script to compute the embeddings of all the images using the following command from the root folder:

```bash
python data_processing/generate_embeddings.py
```

The final dataset is saved in the *dataset_embeddings.csv* file. To generate embeddings for the images, our process can be summarized as follows:

1. Retrieve the filenames of the images in the dataset.

2. Divide the data into batches, and for each batch, perform the following steps:

    1. Compute the vector embedding for each image in the batch using the Vectorize Image API of Azure AI Vision.

    2. Save the vector embeddings of the images along with the filenames into a file.

3. Update the dataset by inserting the vector embedding of each image.
