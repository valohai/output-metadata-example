"""Execution step that creates random files with metadata.

Metadata is stored in sidecar files (one per output file).
"""

import json
import logging

import valohai  # type: ignore

from util import (
    dummy_metadata,
    iso_date,
    new_dataset_version,
    random_filenames,
    random_paragraphs,
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

for filename in random_filenames(nr_of_files):
    # create a file with dummy content
    logger.info(f"Creating file: {filename}")
    with open(output_path.path(filename), "w") as output_file:
        output_file.write(random_paragraphs())

    # create some dummy metadata for the file
    file_path = f"{output_dir}/{filename}"
    file_metadata = dummy_metadata()

    # add the file to the dataset versions
    file_metadata["valohai.dataset-versions"] = [
        f"dataset://{dataset_name}/{dataset_version}",
        f"dataset://{dataset_2_name}/{dataset_version}",
    ]

    logger.info("Creating a sidecar file")
    with open(output_path.path(filename + ".metadata.json"), "w") as sidecar_file:
        sidecar_file.write(json.dumps(file_metadata))
