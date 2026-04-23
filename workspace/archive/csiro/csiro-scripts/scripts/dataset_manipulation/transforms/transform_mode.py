# transform_mode.py
# Transform mode enumeration
# Defines the different modes for applying transforms: training, validation, and TTA

from enum import Enum


class TransformMode(Enum):
    """
    Enumeration of transform application modes.
    
    - TRAIN: Random/probabilistic augmentation for training
    - VAL: No augmentation, preprocessing only for validation
    - TTA: Deterministic variants for test-time augmentation
    """
    TRAIN = "train"
    VAL = "val"
    TTA = "tta"

