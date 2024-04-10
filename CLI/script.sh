#!/bin/sh
#
# The path to the JSON configuration file.
CONFIG_FILE="config.json"
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "config.json' file does not exist."
    echo "Creating 'config.json' file."
    echo '{"HOME_PATH": "", "DOCKER_DESKTOP_PATH": "", "EMPAIA_PATH": "", "IMAGE_PATH": ""}' > "$CONFIG_FILE"
fi

# Check if jq is installed
if ! command -v jq &> /dev/null
then
    echo "jq could not be found. Attempting to install it..."
    sudo apt-get update && sudo apt-get install -y jq
        # Check if the installation was successful
    if ! command -v jq &> /dev/null
    then
        echo "Failed to install jq. Please install it manually to continue."
        exit
    fi
fi
echo "jq is installed."
# Read the DOCKER_DESKTOP_PATH and EMPAIA_PATH from the JSON configuration file.
# jq is a command-line JSON processor.
HOME_PATH=$(jq -r '.HOME_PATH' "$CONFIG_FILE")
DOCKER_DESKTOP_PATH=$(jq -r '.DOCKER_DESKTOP_PATH' "$CONFIG_FILE")
EMPAIA_PATH=$(jq -r '.EMPAIA_PATH' "$CONFIG_FILE")
IMAGE_PATH=$(jq -r '.IMAGE_PATH' "$CONFIG_FILE")
# Function to start the EMPAIA application
# - config_file: The path to the JSON file.
# - key: The key to update in the JSON file.
# - value: The new value for the key.
update_json(){
    local config_file="$1"
    local key="$2"
    local value="$3"
    python3 -c "import json; data = json.load(open('$config_file')); data['$key'] = r'$value'; json.dump(data, open('$config_file', 'w'))"
}

# This function starts the EMPAIA application.
# If EMPAIA_PATH is not set, it asks the user to enter it and updates the JSON file.
# TO DO: Add a check to see if the EMPAIA service is already running,
start_app(){

    # Check if the EMPAIA_PATH is set
    if [[ -z $EMPAIA_PATH ]]; then
        echo "Path to EMPAIA not found."
        read -r -p "Please enter the path to EMPAIA: " EMPAIA_PATH
        update_json $CONFIG_FILE "EMPAIA_PATH" $EMPAIA_PATH
    fi
    # Change the directory to the EMPAIA_PATH
    cd $EMPAIA_PATH || exit
    # check if wsi-mount-points.json
    if [[ ! -f "wsi-mount-points.json" ]]; then
        echo "Error: 'wsi-mount-points.json' file does not exist in $EMPAIA_PATH"
        read -r -p "Would you like to create it? (yes/no): " answer
        # check if the user wants to create the file
        if [[ $answer == "yes" ]]; then
            echo "Creating 'wsi-mount-points.json' file"
            # Construct the key
            key="${EMPAIA_PATH}/eats/images"
            # Create the JSON object
            json=$(jq -n \
              --arg path "$key" \
              --arg data "/data" \
              '{($path): $data}')
            echo $json > wsi-mount-points.json
        else
            echo "Exiting..."
            return 1
        fi
    fi
    printf "\nStarting EMPAIA\n"
    eats services up ./wsi-mount-points.json
    cmd.exe /c start http://localhost:8888/wbc3/
}
# Function to add picture to the EMPAIA
add_picture(){
    # Check if the image path is empty
    if [[ -z "$IMAGE_PATH" ]]; then
        read -r -p "Please enter the image directory you want to use: " IMAGE_PATH
        # Update the IMAGE_PATH in the config.json file
        update_json "$CONFIG_FILE" "IMAGE_PATH" "$IMAGE_PATH"
    else
        echo "Image path is $IMAGE_PATH. You can change it manually if needed."
    fi

    cd "$IMAGE_PATH" || { echo "Error: Failed to change directory to $IMAGE_PATH"; return 1; }

    # Check if the images directory exists
    if [[ ! -d "images" ]]; then
        echo "Error: 'images' directory does not exist in $IMAGE_PATH"
        return 1
    fi

    ls images
    read -r -p "Please enter the name of the image you want to add, along with the type for eks. (silde21.wsi): " IMAGE_NAME

    # Check if the image file exists
    if [[ ! -f "images/$IMAGE_NAME" ]]; then
        echo "Error: Image $IMAGE_NAME does not exist"
        return 1
    fi
    
    
    # Remove the type from the image name
    IMAGE_NAME_NO_TYPE="${IMAGE_NAME%.*}"
    generated_id=$(uuidgen)
    #touch "$IMAGE_NAME_NO_TYPE.json"

        # Create the JSON structure
    json=$(jq -n \
              --arg path "/data/$IMAGE_NAME" \
              --arg id "$generated_id" \
              '{type: "wsi", path: $path, id: $id}')
    # Write the JSON structure to the file
    echo "$json" > "${IMAGE_NAME_NO_TYPE}.json"
    # Print the contents .json file
    echo "The contents of the JSON file:"
    cat "${IMAGE_NAME_NO_TYPE}.json"
    # Ask the user if they want to add the image to EATS
    read -r -p "Would you like to add this image to EATS? (yes/no): " answer

    if [[ $answer == "yes" ]]; then
    # Add the image to EATS
        eats slides register "${IMAGE_NAME_NO_TYPE}.json"
    else
    # Delete the JSON file and return to the menu
        rm "${IMAGE_NAME_NO_TYPE}.json"
        return
    fi
    
}

# create EADS FUNCTION
create_eads(){
        echo '{
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "My Cool Medical AI Algorithm",
        "name_short": "Cool App",
        "namespace": "org.empaia.helse_vest_piv.cool_app.v3.1",
        "description": "Does super advanced AI stuff, you know...",
        "io": {
            "my_wsi": {
                "type": "wsi"
            },
            "my_quantification_result": {
                "type": "float",
                "description": "Human readable text, e.g. super important metric",
                "reference": "io.my_wsi"
            }
        },
        "modes": {
            "standalone": {
                "inputs": [
                    "my_wsi"
                ],
                "outputs": [
                    "my_quantification_result"
                ]
            }
        }
    }' > ead.json
}
# TODO
# ASk about app path
# create app path if not exist
# ask user about if he wants creates eads.json with script or manually
# 
#
add_app(){
    read -r -p "Please enter the path to the app you want to use: " APP_PATH
    # Update the APP_PATH in the config.json file
    update_json "$CONFIG_FILE" "APP_PATH" "$APP_PATH"
    # Change the directory to the APP_PATH
    cd "$APP_PATH" || { echo "Error: Failed to change directory to $APP_PATH"; return 1; }

    #ask user if he wants to create eads.json
    read -r -p "Would you like to create eads.json file? (yes/no): " answer
    if [[ $answer == "yes" ]]; then
        create_eads
        cat ead.json
    fi
}
#exit cli
exit_cli(){
    printf "\nExiting...\n"
    cd ~
}

# This function shuts down the EMPAIA service and exits the script.
exit_close(){
    eats services down
    exit_cli
}

# This function opens a GitHub documentation page in the default web browser.
help(){
    cmd.exe /c start https://github.com/patologiivest/empaia-howto?tab=readme-ov-file
}

# Check if Docker is running
if docker info >/dev/null 2>&1; then
    echo "Docker is already running."
else
    # If Docker is not running, check if the DOCKER_DESKTOP_PATH is set.
    if [[ -z $DOCKER_DESKTOP_PATH ]]; then
        # If DOCKER_DESKTOP_PATH is not set, ask the user to enter it and update the JSON file.
        echo "Docker Desktop path not set."
        read -r -p "Please enter the path to Docker Desktop: " DOCKER_DESKTOP_PATH
        echo $DOCKER_DESKTOP_PATH
        update_json $CONFIG_FILE "DOCKER_DESKTOP_PATH" "$DOCKER_DESKTOP_PATH"
    fi
    # Open Docker Desktop
    echo "Opening Docker Desktop application; this can take a while"
    powershell.exe -Command "Start-Process '$DOCKER_DESKTOP_PATH'"
fi


# Define the menu options
options=("Initiate EMPAIA service; readies system for deployments." "Add picture." "Add app." "Show help; link to GitHub documentation." "Close CLI, keep service active." "Terminate CLI and EMPAIA service.")

# while loop
while true; do
    echo "What do you want to do?"
    # Use the select statement to generate a menu
    select var in "${options[@]}"; do
        case $var in
            "Initiate EMPAIA service; readies system for deployments.")
                start_app
                break
                ;;
            "Add picture.")
                add_picture
                break
                ;;
            "Add app.")
                add_app
                break
                ;;
            "Show help; link to GitHub documentation.")
                help
                break
                ;;
            "Close CLI, keep service active.")
                exit_cli
                break 2
                ;;
            "Terminate CLI and EMPAIA service.")
                exit_close
                break 2
                ;;
            *) 
                echo "Invalid option $REPLY"
                break
                ;;
        esac
    done
done