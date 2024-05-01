import os
import requests
import numpy as np
from PIL import Image
from io import BytesIO
import cv2
from typing import List, Tuple

APP_URL = "http://app-service:8000"
JOB_ID = os.environ.get('EMPAIA_JOB_ID')
TOKEN = os.environ.get('EMPAIA_TOKEN')
HEADER = {"Authorization": f"Bearer {TOKEN}"}
PIXEL_CLASS = "org.empaia.helse_vest_piv.cool_app.v3.1.classes.pixel"

# Retrieve meta-data
input_url = f"{APP_URL}/v3/{JOB_ID}/inputs/my_wsi"

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

sat = 50


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


def post_items_to_collection(collection_id: str, items: list):
    """
    add items to an existing output collection

    Parameters:
        items: list of data elements
        :param items:
        :param collection_id:
        :param self:
    """
    url = f"{APP_URL}/v3/{JOB_ID}/collections/{collection_id}/items"
    f = requests.post(url, json={"items": items}, headers=HEADER)
    f.raise_for_status()
    return f.json()


def quantification(wsi_tile2: Image):
    """
    pretends to do something useful

    Parameters:
        wsi_tile2: WSI image tile
    """
    return 42


def detect_pixel2(slide: dict, roi: dict, mask, density: float) -> Tuple[dict, dict]:
    """
    pretends to detect pixels

    Parameters:
        slide: contains WSI id (and meta data)
        roi: tile position on level 0
        :param mask:
    """

    pixels = []
    confidences = []

    points = detect_pixels_in_mask(roi, mask)

    slide_npp = slide["pixel_size_nm"]["x"]

    for point in points:
        pixel = {
            "name": "pixel",
            "type": "point",
            "reference_id": slide["id"],
            "reference_type": "wsi",
            "coordinates": point,
            "npp_created": 499,
            "npp_viewing": [
                499,
                3992,
            ],
            "creator_type": "job",  # NEW required in v3 apps
            "creator_id": JOB_ID,  # NEW required in v3 apps
        }
        pixels.append(pixel)

        confidence_value = 0.5

        confidence = {
            "name": "confidence score",
            "type": "float",
            "value": confidence_value,
            "reference_id": None,
            "reference_type": "annotation",
            "creator_type": "job",  # NEW required in v3 apps
            "creator_id": JOB_ID,  # NEW required in v3 apps
        }
        confidences.append(confidence)

    return pixels, confidences


def classify_pixel(confidences: dict, pixel_class: str, threshold: float = 0.5):
    """
    classifies nuclei based on Value for each item in a collection of float values

    Parameters:
        confidences: a collection of float values for model confidence referencing corresponding annotations
        positive_class: class assigned for values > threshold
        negative_class: class assigned for values <= threshold
        threshold: threshold for positive/negative classifications, default: 0.5
    """
    num_pixels = 0
    classifications = []
    for confidence in confidences:
        num_pixels += 1
        classification = {
            "value": pixel_class,
            "reference_id": confidence["reference_id"],
            "reference_type": "annotation",
            "type": "class",  # NEW required in v3 apps
            "creator_type": "job",  # NEW required in v3 apps
            "creator_id": JOB_ID,  # NEW required in v3 apps
        }

        classifications.append(classification)

    return classifications, num_pixels


def detect_pixels_in_mask(rectangle, mask):
    # Find contours in the binary mask
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    x_min = rectangle["upper_left"][0]
    y_min = rectangle["upper_left"][1]
    print(x_min)
    print(y_min)

    # Initialize a list to store detected cell coordinates
    detected_pixel_coordinates = []

    # Loop over contours
    for contour in contours:
        # Compute the center of the contour
        M = cv2.moments(contour)
        if M["m00"] != 0:  # To avoid division by zero
            x = int(x_min + (M["m10"] / M["m00"]))
            y = int(y_min + (M["m01"] / M["m00"]))
            detected_pixel_coordinates.append([x, y])

    return detected_pixel_coordinates


def detect_pixel(my_wsi: dict, my_rectangle: dict, mask):
    """

    Parameters:
        my_wsi: contains WSI id (and meta data)
        my_rectangle: tile position on level 0
        :param mask:
    """

    pixels = {
        "item_type": "point",
        "items": [],
        "reference_id": my_rectangle["id"],  # point annotations collection references my_rectangle
        "reference_type": "annotation",
        "type": "collection",  # NEW required in v3 apps
        "creator_type": "job",  # NEW required in v3 apps
        "creator_id": JOB_ID,  # NEW required in v3 apps
    }

    pixel_classes = {
        "item_type": "class",
        "items": [],
        "type": "collection",  # NEW required in v3 apps
        "creator_type": "job",  # NEW required in v3 apps
        "creator_id": JOB_ID,  # NEW required in v3 apps,
    }

    detected_pixel_coordinates = detect_pixels_in_mask(mask)

    for coord in detected_pixel_coordinates:
        cell = {
            "name": "cell",
            "type": "point",
            "reference_id": my_wsi["id"],  # each point annotation references my_wsi
            "reference_type": "wsi",
            "coordinates": coord,  # replace with actual coordinates
            "npp_created": 499,
            # pixel resolution level of the WSI, that has been used to create the annotation (relevant for viewer)
            "npp_viewing": [
                499,
                3992,
            ],
            # (optional) recommended pixel reslution range for viewer to display annotation, if npp_created is not sufficient
            "creator_type": "job",  # NEW required in v3 apps
            "creator_id": JOB_ID,  # NEW required in v3 apps
        }
        pixels['items'].append(cell)

        pixel_class = {
            "value": PIXEL_CLASS,  # possible values defined in EAD
            "reference_id": None,  # yet unknown
            "reference_type": "annotation",
            "type": "class",  # NEW required in v3 apps
            "creator_type": "job",  # NEW required in v3 apps
            "creator_id": JOB_ID,  # NEW required in v3 apps
        }
        pixel_classes["items"].append(pixel_class)

    return pixels, pixel_classes


def pil_image_to_opencv(image):
    # Convert PIL image to OpenCV image format
    image_cv = np.array(image)  # Convert PIL image to a numpy array
    image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)  # Convert RGB to BGR
    return image_cv


def quantification2(img, sat=50):
    # Quantify amount of fibrosis in a single image
    # img = cv2.imread(file)  # loaded as B G R
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

    return score, idx, mask_red


my_wsi = get_input("my_wsi")
my_rectangle = get_input("my_rectangle")

wsi_tile = get_wsi_tile(my_wsi, my_rectangle)

wsi_tile_cv = pil_image_to_opencv(wsi_tile)

score, idx, mask_red = quantification2(wsi_tile_cv)

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

'''
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

my_pixels = {
    "item_type": "collection",
    "items": [],
    "type": "collection",  # NEW required in v3 apps
    "creator_type": "job",  # NEW required in v3 apps
    "creator_id": JOB_ID,  # NEW required in v3 apps
}
my_pixel_classes = {
    "item_type": "collection",
    "items": [],
    "type": "collection",  # NEW required in v3 apps
    "creator_type": "job",  # NEW required in v3 apps
    "creator_id": JOB_ID,  # NEW required in v3 apps
}

'''

pixel_collection = {
    "item_type": "point",
    "reference_id": my_rectangle["id"],
    "reference_type": "annotation",
    "items": [],
    "type": "collection",  # NEW required in v3 apps
    "creator_type": "job",  # NEW required in v3 apps
    "creator_id": JOB_ID,  # NEW required in v3 apps
}

confidence_collection = {
    "item_type": "float",
    "items": [],
    "type": "collection",  # NEW required in v3 apps
    "creator_type": "job",  # NEW required in v3 apps
    "creator_id": JOB_ID,  # NEW required in v3 apps
}

classification_collection = {
    "item_type": "class",
    "items": [],
    "type": "collection",  # NEW required in v3 apps
    "creator_type": "job",  # NEW required in v3 apps
    "creator_id": JOB_ID,  # NEW required in v3 apps
}

POINT_DENSITY = 0.5
CLASSIFICATION_THRESHOLD = 0.7
BATCH_SIZE = 5000

pixel_collection = post_output("detected_pixels", pixel_collection)
confidence_collection = post_output("model_confidences", confidence_collection)
classification_collection = post_output("pixel_classifications", classification_collection)

pixels, confidences = detect_pixel2(my_wsi, my_rectangle, mask_red, density=POINT_DENSITY)
classifications, num_pixels = classify_pixel(
    confidences, PIXEL_CLASS, threshold=CLASSIFICATION_THRESHOLD
)

batch_size = BATCH_SIZE
start_idx = 0
end_idx = start_idx + batch_size
while start_idx < len(pixels):
    nuclei = post_items_to_collection(pixel_collection["id"], pixels[start_idx:end_idx])

    for nucleus, confidence, classification in zip(
            nuclei["items"], confidences[start_idx:end_idx], classifications[start_idx:end_idx]
    ):
        classification["reference_id"] = confidence["reference_id"] = nucleus["id"]

    post_items_to_collection(confidence_collection["id"], confidences[start_idx:end_idx])
    post_items_to_collection(classification_collection["id"], classifications[start_idx:end_idx])
    start_idx += batch_size
    end_idx = start_idx + batch_size

numerical_outputs = {
    "number_of_red_pixels": num_pixels,
    "fibrosis_score": score,
}

for key, value in numerical_outputs.items():
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
