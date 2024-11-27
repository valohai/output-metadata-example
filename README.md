# Demo Project for Single Metadata File

This is an example of how to use a single metadata file for all execution outputs
instead of creating an individual sidecar file for each output.

## Prerequisites

To run this project as-is, you need Python 3.9 or later installed on your system.

## Setup

To set up the project, first create a virtual environment,
and then install the required dependencies (from `requirements.txt`).

Next, you need to log on Valohai and associate the project directory with a project.
(See [Valohai documentation](https://docs.valohai.com/hc/en-us/) → _Command-line Client_ for more information.)

## Running the Project

Run the execution step `create-files` either from the UI or
from the command-line (using `valohai-cli`).
No parameters are needed for this step.

```shell
vh execution run create-files
```

## Creating the Metadata File

Instead of creating a sidecar file for each output,
you create a single metadata file that lists all the outputs.

The metadata file name must be `outputs.metadata.jsonl`
and it must be in the execution outputs root directory.

The file format is JSON lines,
where each line is a JSON object with the following fields:

- `file`: The name (including the path) of the output file
- `metadata`: The metadata as a JSON object

The value of the `metadata` property is the same JSON object that you would put in a sidecar file.
It is then applied to the file specified in the `file` property.

For example, if your output file is `output.txt` in a directory called `my_outputs`,
and you want to set a metadata property `my_property` to the value `my_value`,
you would create a file called `outputs.metadata.jsonl` with the following content:

```jsonlines
{"file": "my_outputs/output.txt", "metadata": {"my_property": "my_value"}}
```

(Note that in the sidecar JSON file,
you can divide the properties into multiple lines for readability,
but in the JSON lines file, each list of file properties must be on a single line.)
