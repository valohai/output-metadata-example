"""Execution step that creates random files with metadata.

Metadata is stored in one file per execution.
"""

import json
import logging
from typing import Any

import valohai  # type: ignore

from util import iso_date, random_filenames, dummy_metadata, random_paragraphs

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

valohai.prepare(
    step="create-files",
    image="python:3.13-slim",
)

# put the created files in a directory named after the current date
# this is not required; it is just a way to organize the outputs
# example value: "2024-11-25"
output_dir = iso_date()

# the metadata file must be saved in the outputs root directory
# under the name "outputs.metadata.jsonl"
metadata_file_path = valohai.outputs().path("outputs.metadata.jsonl")

# metadata format: {file_path: metadata, ...}
execution_outputs_metadata: dict[str, dict[str, Any]] = {}

# create random files with metadata

nr_of_files = 10
output_path = valohai.outputs(output_dir)
for filename in random_filenames(nr_of_files):
    # create a file with dummy content
    logger.info(f"Creating file: {filename}")
    with open(output_path.path(filename), "w") as output_file:
        output_file.write(random_paragraphs())

    # create file metadata
    file_path = f"{output_dir}/{filename}"
    file_metadata = dummy_metadata()
    execution_outputs_metadata[file_path] = file_metadata

# save metadata to a file

logger.info(f"Saving metadata to: {metadata_file_path}")
with open(metadata_file_path, "w") as metadata_file:
    metadata_file.writelines(
        format_metadata_line(filename, file_metadata)
        for filename, file_metadata in execution_outputs_metadata.items()
    )

# output the metadata to the execution log

with open(metadata_file_path) as metadata_file:
    logger.info("Execution metadata:\n" + metadata_file.read())
