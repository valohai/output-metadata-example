"""Execution step that creates random files with metadata.

Metadata is stored in one file per execution.
"""

import json
import logging
from typing import Any

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


def format_metadata_line(file_path: str, file_metadata: dict[str, Any]) -> str:
    """Format metadata for an output file into a format Valohai understands.

    Args:
        file_path: The path to the file (relative to the execution outputs root directory).
        file_metadata: The metadata for the file.
    """

    return (
        json.dumps(
            {
                "file": file_path,
                "metadata": file_metadata,
            }
        )
        + "\n"
    )


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

# the metadata file must be saved in the outputs root directory
# under the name "valohai.metadata.jsonl"
metadata_file_path = valohai.outputs().path("valohai.metadata.jsonl")

# metadata format: {file_path: metadata, ...}
execution_outputs_metadata: dict[str, dict[str, Any]] = {}

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
