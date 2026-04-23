# transforms package
# Transform composition and factory
#
# Provides factory functions for building complete transform pipelines
# from configuration. Separates transform composition from training logic.
#
# Transform order:
# 1. PIL Image transforms (preprocessing + augmentation if training)
# 2. ToTensor (converts PIL Image to tensor)
# 3. Tensor transforms (tensor augmentation if training + normalization)
#
# The factory pattern allows easy composition of preprocessing and augmentation
# steps based on configuration, ensuring consistent transform pipelines across
# training and validation.


__all__ = ['build_train_transform', 'build_val_transform', 'build_tta_transforms']

