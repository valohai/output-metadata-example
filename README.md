# Demo Project for Single Metadata File

This is an example of how to use a single metadata file for all execution outputs
instead of creating an individual sidecar file for each output.

## Prerequisites

To run this project as-is, you need Python 3.9 or later installed on your system.

### Recommended Tools

The following tools are recommended but not required:

- `uv` for handling virtual environments and dependencies
- `just` for running the project tasks

## Setup

To set up the project, first create a virtual environment, and then install the required dependencies with:

```shell
just dev
```

You can also use the `requirements.txt` file to install the dependencies manually with `pip` instead.

Next, you need to log on Valohai and associate the project directory with a project.
(See [Valohai documentation](https://docs.valohai.com/hc/en-us/) → _Command-line Client_ for more information.)

## Running the Project

You can run the execution from the command-line (using `valohai-cli`) with:

```shell
vh execution run create-files
```
