from dataclasses import dataclass, field
from typing import Any, Sequence, Tuple, Type

import numpy as np
from napari.layers import Image, Labels, Layer
from typing_extensions import Annotated

FloatRange = Annotated[float, {"min": np.finfo(np.float32).min, "max": np.finfo(np.float32).max}]
PositiveFloatRange = Annotated[float, {"min": 0, "max": np.finfo(np.float32).max}]
ImageInput = Annotated[Image, {"label": "Image"}]
LayerInput = Annotated[Layer, {"label": "Image"}]
LabelsInput = Annotated[Labels, {"label": "Labels"}]
global_magic_opts = {"auto_call": True}


@dataclass
class Category:
    name: str
    inputs: Sequence[Type]
    default_op: str
    output: str = "image"  # or labels
    # [(name, annotation, default), ...]
    args: Sequence[Tuple[str, Type, Any]] = field(default_factory=tuple)
    # categories
    include: Sequence[str] = field(default_factory=tuple)
    exclude: Sequence[str] = field(default_factory=tuple)
    # visualization
    color_map : str = "gray"
    blending : str = "translucent"
    tool_tip : str = None


CATEGORIES = {
    "Remove noise": Category(
        name="Removal noise",
        inputs=(ImageInput,),
        default_op="gaussian_blur",
        args=[
            ("x", FloatRange, 1),
            ("y", FloatRange, 1),
            ("z", FloatRange, 0)
        ],
        include=("filter", "denoise"),
        exclude=("combine",),
    ),
    "Remove background": Category(
        name="Remove background",
        inputs=(ImageInput,),
        default_op="top_hat_box",
        args=[
            ("x", FloatRange, 10),
            ("y", FloatRange, 10),
            ("z", FloatRange, 0)
        ],
        include=("filter", "background removal"),
        exclude=("combine",),
    ),
    "Filter": Category(
        name="Filter",
        inputs=(ImageInput,),
        default_op="gamma_correction",
        args=[
            ("x", FloatRange, 1),
            ("y", FloatRange, 1),
            ("z", FloatRange, 0)
        ],
        include=("filter",),
        exclude=("combine", "denoise", "background removal", "binary processing"),
    ),
    "Combine": Category(
        name="Combine",
        inputs=(LayerInput, LayerInput),
        default_op="add_images",
        include=("combine",),
        exclude=("map",),
        args=[
            ("a", FloatRange, 1),
            ("b", FloatRange, 1),
        ]
    ),
    "Transform": Category(
        name="Transform",
        inputs=(LayerInput,),
        default_op="sub_stack",
        output="image",  # can also be labels
        args=[
            ("a", FloatRange, 0),
            ("b", FloatRange, 0),
            ("c", FloatRange, 0),
            ("d", bool, False),
            ("e", bool, False),
        ],
        include=("transform",),
    ),
    "Projection": Category(
        name="Projection",
        inputs=(LayerInput,),
        default_op="maximum_z_projection",
        output="image",  # can also be labels
        include=("projection",),
    ),
    "Binarize": Category(
        name="Binarize",
        inputs=(LayerInput,),
        default_op="threshold_otsu",
        output="labels",
        args=[
            ("radius_x", PositiveFloatRange, 1),
            ("radius_y", PositiveFloatRange, 1),
            ("radius_z", PositiveFloatRange, 0),
        ],
        include=("binarize",),
        exclude=("combine",),
    ),
    "Label": Category(
        name="Label",
        inputs=(LayerInput,),
        default_op="voronoi_otsu_labeling",
        output="labels",
        args=[
            ("a", PositiveFloatRange, 2),
            ("b", PositiveFloatRange, 2)
        ],
        include=("label",),
    ),
    "Process labels": Category(
        name="Process labels",
        inputs=(LabelsInput,),
        default_op="exclude_labels_on_edges",
        output="labels",
        args=[
            ("min", PositiveFloatRange, 2),
            ("max", PositiveFloatRange, 100)
        ],
        include=("label processing",),
    ),
    "Measure labels": Category(
        name="Measure labels",
        inputs=(LabelsInput,),
        default_op="pixel_count_map",
        args=[
            ("n", PositiveFloatRange, 1),
            ("m", PositiveFloatRange, 1)
        ],
        include=("label measurement", "map"),
        exclude=("combine",),
        color_map="turbo",
        blending="translucent",
    ),
    "Measure labeled image": Category(
        name="Measure labeled image",
        inputs=(ImageInput, LabelsInput),
        default_op="label_mean_intensity_map",
        args=[
            ("n", PositiveFloatRange, 1),
            ("m", PositiveFloatRange, 1)
        ],
        include=("combine","label measurement", "map"),
        color_map="turbo",
        blending="translucent",
    ),
    "Mesh": Category(
        name="Mesh",
        inputs=(LabelsInput,),
        default_op="draw_mesh_between_touching_labels",
        args=[
            ("n", PositiveFloatRange, 1)
        ],
        include=("label measurement", "mesh"),
        color_map="green",
        blending="additive",
    ),
    "Label neighbor filters": Category(
        name="Label neighbor filters",
        inputs=(ImageInput, LabelsInput),
        default_op="mean_of_n_nearest_neighbors_map",
        args=[
            ("n", PositiveFloatRange, 1),
            ("m", PositiveFloatRange, 100),
        ],
        include=("neighbor",),
        color_map="turbo",
        blending="translucent",
    ),
}

def attach_tooltips():
    # attach tooltips
    import pyclesperanto_prototype as cle
    for k, c in CATEGORIES.items():
        choices = list(cle.operations(['in assistant'] + list(c.include), c.exclude))
        # temporary workaround: remove entries that start with "label_", those have been renamed in pyclesperanto
        # and are only there for backwards compatibility
        choices = list([c for c in choices if not c.startswith('label_')])
        c.tool_tip = "\n".join(choices)
