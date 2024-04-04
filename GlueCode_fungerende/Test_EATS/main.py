import os
import requests
import numpy as np
from PIL import Image
from io import BytesIO
import cv2


APP_URL = "http://host.docker.internal:8888/app-api"
JOB_ID = os.environ.get('EMPAIA_JOB_ID')
TOKEN = os.environ.get('EMPAIA_TOKEN')
HEADER = {"Authorization": f"Bearer {TOKEN}"}

print(TOKEN)
print(HEADER)

# Retrieve meta-data
input_url = f"{APP_URL}/v3/{JOB_ID}/inputs/my_wsi"
print(input_url)

r = requests.get(input_url, headers=HEADER)
r.raise_for_status()
wsi_meta = r.json()
wsi_id = wsi_meta['id']

# Download tile (7,1) at level 2
tile_url = f"{APP_URL}/v3/{JOB_ID}/tiles/{wsi_id}/level/2/position/7/1"
r = requests.get(tile_url, headers=HEADER)
r.raise_for_status()
i = Image.open(BytesIO(r.content))
a = np.array(i)
print(a.shape)
print("Hello World")


# Do something cool with your multi-dimensional array of pixel-color values, like put it in a Neural Network or so...


def put_finalize():
    """
    finalize job, such that no more data can be added and to inform EMPAIA infrastructure about job state
    """
    url = f"{APP_URL}/v3/{JOB_ID}/finalize"
    f = requests.put(url, headers=HEADER)
    f.raise_for_status()


def get_input(key: str):
    """
    get input data by key as defined in EAD
    """
    url = f"{APP_URL}/v3/{JOB_ID}/inputs/{key}"
    f = requests.get(url, headers=HEADER)
    f.raise_for_status()
    return f.json()


def get_wsi_tile(my_wsi2: dict, my_rectangle2: dict):
    """
    get a WSI tile on level 0

    Parameters:
        my_wsi2: contains WSI id (and meta data)
        my_rectangle2: tile position on level 0
    """
    x, y = my_rectangle2["upper_left"]
    width = my_rectangle2["width"]
    height = my_rectangle2["height"]

    wsi_id2 = my_wsi2["id"]
    level = 0

    tile_url2 = f"{APP_URL}/v3/{JOB_ID}/regions/{wsi_id2}/level/{level}/start/{x}/{y}/size/{width}/{height}"
    f = requests.get(tile_url2, headers=HEADER)
    f.raise_for_status()

    return Image.open(BytesIO(f.content))


def post_output(key: str, data: dict):
    """
    post output data by key as defined in EAD
    """
    url = f"{APP_URL}/v3/{JOB_ID}/outputs/{key}"
    f = requests.post(url, json=data, headers=HEADER)
    f.raise_for_status()
    return f.json()


def quantification(wsi_tile2: Image):
    """
    pretends to do something useful

    Parameters:
        wsi_tile2: WSI image tile
    """
    return 42


def pil_image_to_opencv(image):
    #Convert PIL image to OpenCV image format
    image_cv = np.array(image)             # Convert PIL image to a numpy array
    image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)  # Convert RGB to BGR
    return image_cv



def quantification2(img, sat=50):
    #Quantify amount of fibrosis in a single image
    #img = cv2.imread(file)  # loaded as B G R
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    count_foreground_pixel = np.count_nonzero(img_gray)
    grid_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask_1 = cv2.inRange(grid_HSV, (0, sat, 50), (5, 255, 255))  # (low_H, low_S, low_V), (high_H, high_S, high_V)
    mask_2 = cv2.inRange(grid_HSV, (160, sat, 20), (180, 255, 255))
    mask_red = cv2.bitwise_or(mask_1, mask_2)

    if count_foreground_pixel != 0:
        score = round((np.count_nonzero(mask_red) / count_foreground_pixel) * 100, 1)
        quant = np.where(mask_red == 255)
        idx = np.vstack((quant[1], quant[0])).T  # 1 - col - x; 0 - row - y
    else:
        score = np.nan
        idx = np.nan


    return score, idx


my_wsi = get_input("my_wsi")
my_rectangle = get_input("my_rectangle")

wsi_tile = get_wsi_tile(my_wsi, my_rectangle)

wsi_tile_cv = pil_image_to_opencv(wsi_tile)

score, idx = quantification2(wsi_tile_cv)

my_quantification_result = {
    "name": "fibrosis score",  # choose name freely
    "type": "float",
    "value": score,
    "creator_type": "job",  # NEW required in v3 apps
    "creator_id": JOB_ID,  # NEW required in v3 apps
}


post_output("my_quantification_result", my_quantification_result)

numerical_output = {
        "fibrosis_score": score,
    }

for key, value in numerical_output.items():
    data = {
        "name": key.replace("_", " "),
        "value": value,
        "type": "integer" if isinstance(value, int) else "float",
        "reference_id": my_rectangle["id"],
        "reference_type": "annotation",
        "creator_type": "job",  # NEW required in v3 apps
        "creator_id": JOB_ID,  # NEW required in v3 apps
    }
    post_output(key, data)

put_finalize()
