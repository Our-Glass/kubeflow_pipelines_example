""" The script assumes that the folder structure is as follows:

For running:
python folder2docker.py \
    --path folder_with_code \
    --name base_im \
    --build \
    --push 

- folder_with_code
    - file1.py
    - file2.py

The script will create a Dockerfile and a requirements.txt 
file in the folder_with_code folder. as follows:

Container structure:
/usr/local/src/kfp/components
    - folder_with_code
        - file1.py
        - file2.py
        - requirements.txt

"""
import os
import argparse
from pathlib import Path


# Create the parser
parser = argparse.ArgumentParser(description='Create Dockerfile and requirements.txt')
parser.add_argument('-p', '--path', type=str, help='path to folder with code')
parser.add_argument('-n', '--name', type=str, help='name of image', default='folder2docker_image')

parser.add_argument('--build', dest='build', action='store_true')
parser.add_argument('--no-build', dest='build', action='store_false')

parser.add_argument('--push', dest='push', action='store_true')
parser.add_argument('--no-push', dest='push', action='store_false')

parser.set_defaults(build=True)
parser.set_defaults(push=False)

# Get the arguments
PATH = parser.parse_args().path
NAME_IMAGE = parser.parse_args().name
BUILD = parser.parse_args().build
PUSH = parser.parse_args().push

FOLDER_PATH = Path(PATH)


# get folder name
folder_name = FOLDER_PATH.parts[-1]
print(f'CREATING DOCKER::::  Analyzing folder ------> {folder_name}')


# use pipreqs for generating requirements.txt
CMD = f'pipreqs --force {FOLDER_PATH}'
if os.system(CMD) != 0:
    raise Exception('pipreqs failed')
else:
    print(f'CREATING DOCKER::::  requirements created on ------> {FOLDER_PATH}/requirements.txt')


# Create Dockerfile
with open(f'{FOLDER_PATH}/Dockerfile', 'w') as f:
    f.write(f'FROM python:3.7\n')
    f.write(f'COPY . /usr/local/src/kfp/components/{folder_name}\n')
    f.write(f'WORKDIR  /usr/local/src/kfp/components\n')
    f.write(f'COPY requirements.txt .\n')
    f.write(f'RUN pip install -r requirements.txt\n')

print(f'CREATING DOCKER::::  Dockerfile created on ------> {FOLDER_PATH}/Dockerfile.txt')


# build image
if BUILD:
    if os.system(f'docker build -t {NAME_IMAGE} {FOLDER_PATH}') != 0:
        raise Exception('docker build failed')
    else:
        print(f'CREATING DOCKER::::  Image created with name ------> {NAME_IMAGE}')


if PUSH:
    CMD = f'docker push {NAME_IMAGE}'
    if os.system(CMD) != 0:
        raise Exception('docker push failed')
    else:
        print(f'CREATING DOCKER::::  Image pushed with name ------> {NAME_IMAGE}')