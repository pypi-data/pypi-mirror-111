import numpy as np
from typing_extensions import Annotated
from napari.layers import Image, Labels, Layer
LayerInput = Annotated[Layer, {"label": "Image"}]

def convert_to_numpy(layer : LayerInput) -> Layer:
    if isinstance(layer, Labels):
        return Labels(np.asarray(layer.data), name="np " + layer.name)
    else:
        return Image(np.asarray(layer.data), name="np " + layer.name)

def convert_to_2d_timelapse(layer : LayerInput) -> Layer:
    if isinstance(layer, Labels):
        return Labels(np.expand_dims(layer.data, axis=1), name="2d+t " + layer.name)
    else:
        return Image(np.expand_dims(layer.data, axis=1), name="2d+t " + layer.name)
