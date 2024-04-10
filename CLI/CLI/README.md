This is a Bash script for managing the EMPAIA service. It provides a user-friendly menu for performing various tasks, such as initiating the service, adding a picture, adding an app, and exiting the CLI.

## Prerequisites

- Docker
- jq
- sudo access

If `jq` is not installed, the script will attempt to install it using `apt-get`.

## Configuration

The script uses a JSON configuration file to store various settings. The configuration file is created automatically if it doesn't exist. The following settings can be configured:

- `EXIT_PATH`: The path where the script should navigate to before exiting.
- `DOCKER_DESKTOP_PATH`: The path to Docker Desktop.
- `EMPAIA_PATH`: The path to the EMPAIA service.

## Usage

To run the script, navigate to the directory containing the script and run the following command:

```bash
./script.sh