"""Execution step that creates random files with metadata.

Metadata is stored in one file per execution.
File handling is done using the `valohai-utils` helper library.
"""

import logging

import valohai  # type: ignore

from util import (
    iso_date,
    random_filenames,
    dummy_metadata,
    random_paragraphs,
    new_dataset_version,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# define the step for valohai.yaml

default_parameters = {
    "nr_of_files": 10,
}

valohai.prepare(
    step="create-files",
    image="ghcr.io/astral-sh/uv:python3.13-bookworm-slim",
    default_parameters=default_parameters,
)

# put the created files in a directory named after the current date
# this is not required; it is just a way to organize the outputs
# example value: "2024-11-25"
output_dir = iso_date()

# datasets and version to be created
dataset_name = "metadata-demo"
dataset_2_name = "metadata-demo-2"
dataset_version = new_dataset_version()

# create random files with metadata

nr_of_files = valohai.parameters("nr_of_files").value
output_path = valohai.outputs(output_dir)

with valohai.output_properties() as properties:
    # create dataset version URIs
    dataset_1_version = properties.dataset_version_uri(dataset_name, dataset_version)
    dataset_2_version = properties.dataset_version_uri(dataset_2_name, dataset_version)

    for filename in random_filenames(nr_of_files):
        # create a file with dummy content
        logger.info(f"Creating file: {filename}")
        with open(output_path.path(filename), "w") as output_file:
            output_file.write(random_paragraphs())

        # create some dummy metadata for the file
        file_path = f"{output_dir}/{filename}"
        properties.add(file=file_path, properties=dummy_metadata())

        # add the file to the dataset versions
        properties.add_to_dataset(file=file_path, dataset_version=dataset_1_version)
        properties.add_to_dataset(file=file_path, dataset_version=dataset_2_version)
