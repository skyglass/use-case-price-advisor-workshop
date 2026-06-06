# Copyright (c) 2025 Konstantinos Karavitis
#
# Licensed under the Creative
# Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0).
# You may not use this file for commercial purposes. See the LICENSE file in
# the project root or visit: https://creativecommons.org/licenses/by-nc/4.0/

import tensorflow as tf, pathlib, pprint
mdl = tf.saved_model.load(pathlib.Path('data/pricing_saved_model'))
print("Variables:", [v.shape for v in mdl.trainable_variables])