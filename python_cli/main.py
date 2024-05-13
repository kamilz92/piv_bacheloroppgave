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
        eats_path = data.get('EATS_PATH')

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
                json.dump({f"{eats_path}/images": "/data"}, f, indent=4)
    else:
        return

def generate_eats_json(app_name):
    eats_data = {
        "name": app_name,
        "type": "app",
        "path": f"/data/{app_name}",
        "id": str(uuid.uuid4())
    }
    with open('ead.json', 'w') as f:
        json.dump(eats_data, f, indent=4)


@cli.command(help="Starts EMPAIA.")
def start_empaia():
    global eats_path, docker_desktop_path, config_file

    config_file = 'config.json'
    if not os.path.isfile(config_file):
        with open(config_file, 'w') as f:
            json.dump({"DOCKER_DESKTOP_PATH": "", "EATS_PATH": ""}, f, indent=4)

    if not eats_path:
        eats_path = click.prompt('Please enter the path to EMPAIA')
        update_json(config_file, "EATS_PATH", eats_path)

    os.chdir(eats_path)

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
    os.chdir(eats_path)

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


@cli.command(help="Adds an app.")
@click.argument('app_name', default="")
@click.argument('app_folder', default="")
def add_app(app_name, app_folder):
    if app_name == "":
        app_name = input("Please enter the name of the app: ")
    config_file = 'config.json'
    if not os.path.isfile(config_file):
        with open(config_file, 'w') as f:
            json.dump({"DOCKER_DESKTOP_PATH": "", "EATS_PATH": ""}, f, indent=4)

    if not eats_path:
        eats_path = click.prompt('Please enter the path to EMPAIA')
        update_json(config_file, "EATS_PATH", eats_path)

    if not os.path.isfile('eats.json'):
        print("eats.json not found.")
        generate_eats_json(app_name)
        
    if app_folder == "":
        app_folder = input("Please enter the path to the app folder: ")
    
    os.chdir(app_folder)
    docker_build_result = subprocess.run(["docker", "build", "-t", app_name, "."])
    if docker_build_result.returncode != 0:
        print("Docker build failed. Exiting...")
        return
    os.chdir("..")
    
    subprocess.run(["eats", "apps", "register", "ead.json", name], stdout=open('app.env', 'w'))
    subprocess.run(["export", "$(xargs < app.env)"])
    subprocess.run(["eats", "jobs", "register", os.getenv("APP_ID"), "./inputs"], stdout=open('job.env', 'w'))
    subprocess.run(["export", "$(xargs < job.env)"])
    subprocess.run(["eats", "jobs", "run", "./job.env"])
    subprocess.run(["eats", "jobs", "wait", os.getenv("EMPAIA_JOB_ID")])
    subprocess.run(["eats", "jobs", "status", os.getenv("EMPAIA_JOB_ID")])


@cli.command(help="Build a project.")
@click.argument('project_name', default="")
@click.option("-i", is_flag=True, help="Initialize series of question to fill in eads.json")
def build_project(i, project_name):
    os.chdir(eats_path)
    
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
    #i
    if project_name != "":
        subprocess.run(["mv", "App", f"{project_name}"])
    if i:
        print("Please fill in the following information to create a project. (press enter to skip)")
        
        name = input("Project name: ")
        update_json('ead.json', 'name', name)
        #TODO: add more fields
        
    else:
        return
    



if __name__ == '__main__':
    cli()