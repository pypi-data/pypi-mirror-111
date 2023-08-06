from typing import Tuple, List, Union
import cv2
import math
import numpy as np

from .models import Coord2D, Detection, ReferencePointConfiguration, Resolution, TrackedDetection


def detection_to_middle_bottom_coord(detections: Union[List[Detection], List[TrackedDetection]]) -> List[Coord2D]:
    """
    Turns a list of detections into a list of coordinates.
    :param detections: the detections to be mapped.
    :return: a list of mapped coordinates.
    """
    result = []
    for detection in detections:
        result.append(Coord2D(round(detection.p0.x + ((detection.p1.x - detection.p0.x) / 2)), detection.p1.y))
    return result


def resize_image_batch(batch: np.array, resolution: Resolution) -> np.array:
    """
    Resizes a batch of images into a given resolution.
    :param batch: the batch of images to be resized.
    :param resolution: the destination resolution.
    :return: a batch of images resized.
    """
    output = np.zeros((batch.shape[0], resolution.width, resolution.height, batch.shape[-1]))
    for n, i in enumerate(batch):
        output[n, :, :, :] = cv2.resize(batch[n, :, :, :], output.shape[1:-1])
    return output


def split_coords(coords: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Split's the coordinates (x, y) from a np.array (n, 2) into to np.arrays (n,) each containing a respective coordinate
    value.
    :param coords: the np.array original coordinates.
    :return: the original coordinates split into two np.arrays.
    """
    x, y = [], []
    for coord in coords:
        x.append(coord[0])
        y.append(coord[1])
    return np.array(x), np.array(y)


def to_middle_bottom_part(detection: Union[Detection, TrackedDetection]) -> Coord2D:
    """
    Takes a detection and turns it into a the middle bottom coord representation of it.
    :param detection: the detection to be mapped.
    :return: the coordinate representation of the middle bottom coord of the original detection.
    """
    return Coord2D(round(detection.p0.x + ((detection.p1.x - detection.p0.x) / 2)), detection.p1.y)

