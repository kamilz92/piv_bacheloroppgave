import click
import json
import os
import subprocess
import uuid

EATS_TEMPLATE_GIT_URL = "https://github.com/kamilz92/eats.git"
config_file = 'config.json'

with open(config_file, 'r') as f:
        data = json.load(f)
        docker_desktop_path = data.get('DOCKER_DESKTOP_PATH')
        empaia_path = data.get('EMPAIA_PATH')

@click.group()
def cli():
    pass

def update_json(config_file, key, value):
    with open(config_file, 'r+') as f:
        data = json.load(f)
        data[key] = value
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

def check_docker():
    try:
        subprocess.check_output("docker info", stderr=subprocess.STDOUT, shell=True)
        print("Docker is already running.")
    except subprocess.CalledProcessError:
        config_file = 'config.json'
        with open(config_file, 'r') as f:
            data = json.load(f)
            docker_desktop_path = data.get('DOCKER_DESKTOP_PATH')

        if not docker_desktop_path:
            print("Docker Desktop path not set.")
            docker_desktop_path = input("Please enter the path to Docker Desktop: ")
            update_json(config_file, "DOCKER_DESKTOP_PATH", docker_desktop_path)

        print("Opening Docker Desktop application; this can take a while")
        subprocess.run(["powershell.exe", "-Command", f"Start-Process '{docker_desktop_path}'"])

def create_wsi_mount_points():
    if not os.path.isfile('wsi-mount-points.json'):
        if click.confirm('"wsi-mount-points.json" not found. Would you like to create it?'):
            with open('wsi-mount-points.json', 'w') as f:
                json.dump({f"{empaia_path}/images": "/data"}, f, indent=4)
    else:
        return


@cli.command(help="Starts EMPAIA.")
def start_empaia():
    global empaia_path, docker_desktop_path, config_file

    config_file = 'config.json'
    if not os.path.isfile(config_file):
        with open(config_file, 'w') as f:
            json.dump({"DOCKER_DESKTOP_PATH": "", "EMPAIA_PATH": ""}, f, indent=4)

    if not empaia_path:
        empaia_path = click.prompt('Please enter the path to EMPAIA')
        update_json(config_file, "EMPAIA_PATH", empaia_path)

    os.chdir(empaia_path)

    if not os.path.isdir('images'):
        os.mkdir('images')

    create_wsi_mount_points()

    res = subprocess.run(["eats", "services", "up", "./wsi-mount-points.json"])
    #error handling
    if res.returncode != 0:
        print("Error starting EMPAIA.")
    else:
        print("EMPAIA started successfully.")
        print("Ctrl + click http://localhost:8888/wbc3/ to open EMPAIA in your browser.")

@cli.command(help="Closes EMPAIA.")
def close_empaia():
    subprocess.run(["eats", "services", "down", "-v"])

@cli.command(help="Adds a image.")
@click.argument('img', default="")
def add_image(img):
    os.chdir(empaia_path)

    # check if images folder exists
    if not os.path.isdir('images'):
        os.mkdir('images')
    
    if img == "":
        print(os.listdir('images')) 
        img = input('Please enter the name of the image you want to add, along with the type for eks. (silde21.wsi): ')
    
    if not '.' in img:
        print('Please enter the image name along with the type for eks. (slide21.wsi)')
        return

    img_name, img_type = img.split('.')
    # check if image exists
    if not os.path.isfile(f'images/{img}'):
        print('Image not found.')
        return
    
    if not os.path.isfile(f'{img_name}.json'):
        print('Json file for image was not found.')
        img_id = str(uuid.uuid4())
        img_data = {
        "type": "wsi",
        "path": f"/data/{img}",
        "id": img_id
        }
        with open(f"{img_name}.json", 'w') as f:
            json.dump(img_data, f, indent=4)
    else:
        print('Json file for image was found.')
        print("Created json file for image...")
        with open(f'{img_name}.json', 'r') as f:
            print(f.read())
    answer = click.prompt('Would you like to add the image to EMPAIA? (y/n)')
    if answer != 'y':
        return
    res = subprocess.run(["eats", "slides", "register", f"{img_name}.json"])

    if res.returncode != 0:
        print("Error adding image.")
    else:
        print("Image added successfully.")

#TODO
@cli.command(help="Adds an app.")
@click.argument('app_name', default="")
def add_app(app_name):
    if app_name == "":
        app_name = input("Provide folder name for the app: ")

    os.chdir(empaia_path)
    if not os.path.isdir(app_name):
        print("App not folder not found.")
        return


@cli.command(help="Build a project.")
@click.option("-i", is_flag=True, help="Initialize series of question to fill in eads.json")
def build_project(i):
    os.chdir(empaia_path)
    
    if os.path.isdir('eats'):
        print("Eats already exists.")
        return
    
    try: 
        subprocess.run(["git", "clone", EATS_TEMPLATE_GIT_URL], check=True)
    except subprocess.CalledProcessError:
        print("Error cloning repository.")
        return
    
    os.chdir('eats')
    subprocess.run(["rm", "-rf", ".git"])
    subprocess.run(["mkdir", "images"])

    create_wsi_mount_points()
    
    if i:
        print("TODO")
        print("A bunch of questions will be asked to fill in the eats.json file.")
        #TODO




if __name__ == '__main__':
    cli()