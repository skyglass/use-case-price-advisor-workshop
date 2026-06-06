# Copyright (c) 2025 Konstantinos Karavitis
#
# Licensed under the Creative
# Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0).
# You may not use this file for commercial purposes. See the LICENSE file in
# the project root or visit: https://creativecommons.org/licenses/by-nc/4.0/


import pathlib
import zipfile

src  = pathlib.Path("data/pricing_saved_model")
dest = pathlib.Path("data/pricing_saved_model.zip")
with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as zf:
  for f in src.rglob("*"):
    zf.write(f, f.relative_to(src))
print("Zipped model →", dest)
