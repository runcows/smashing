import re
import os
import zipfile, shutil

__name__ = "smashing"
__version__ = "1.2.0"

MC_VERSION_RANGE = "1.21.8-11"


######################################
##            VERSIONING            ##
######################################
PATHS_REPLACE_VERSION_NUM = [
  "data/rc_smashing/dialog/about.json",
  "backport_81/data/rc_smashing/dialog/about.json",
  "pack.mcmeta"
]
PATHS_REPLACE_LOAD_STATUS = [
  "data/rc_smashing/function/init.mcfunction"
]

major, minor, patch = map(int, __version__.split('.'))

def find_replace_in_file(path: str, pattern: str, replace):
  with open(path, "r+") as file:
    contents = file.read()
    contents = re.sub(pattern, replace, contents)
    file.seek(0)
    file.write(contents)
    file.truncate()

# vX.X.X
for file_path in PATHS_REPLACE_VERSION_NUM:
  find_replace_in_file(file_path, r'v[0-9]*\.[0-9]*\.[0-9]*', f"v{__version__}")
  print(f"\tvX.X.X -> v{__version__} in {file_path}")

# load.status
for file_path in PATHS_REPLACE_LOAD_STATUS:
  find_replace_in_file(file_path, r'rc_smashing load\.status [0-9]*', f"rc_smashing load.status {major}")
  find_replace_in_file(file_path, r'rc_smashing_minor load\.status [0-9]*', f"rc_smashing_minor load.status {minor}")
  print(f"\treplacing load.status values in {file_path}")


######################################
##             BUILDING             ##
######################################
PATH_OUTPUT = "out/"

datapack_out = PATH_OUTPUT + f"{MC_VERSION_RANGE}_{__name__}_v{__version__}.zip"

include = [
  "data/",
  "backport_81/",
  "pack.mcmeta",
  "pack.png",
  "LICENSE"
]

# Clear out/
shutil.rmtree(PATH_OUTPUT) if os.path.isdir(PATH_OUTPUT) else None
os.mkdir(PATH_OUTPUT)

def zipdir(path: str, ziph: zipfile.ZipFile):
  # ziph is zipfile handle
  for root, dirs, files in os.walk(path):
    for file in files:
      ziph.write(
        os.path.join(root, file), 
        os.path.relpath(
          os.path.join(root, file), 
          os.path.join(path, '..')
        )
      )

# Build datapack
with zipfile.ZipFile(datapack_out, "w", zipfile.ZIP_DEFLATED) as zipf:
  for include_path in include:
    if include_path.endswith("/"):
      zipdir(include_path, zipf)
    else:
      zipf.write(include_path)
