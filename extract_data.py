import json
import os
import tarfile
from shutil import copyfile

DATASET_DIR = 'dataset_downloads/pascal_2012/'
MAX_IMAGE_PER_CAT = 50

def extract_archive(path, to_directory='.'):
  cwd = os.getcwd()
  os.chdir(to_directory)

  try:
      file = tarfile.open(path, 'r:gz')
      try: 
        file.extractall()
      finally: 
        file.close()
  finally:
      os.chdir(cwd)

def read_metadata():
  with open(DATASET_DIR + 'train.json') as json_file:
    return json.load(json_file)

def copy_image(metadata, category_name, image_id):
  for image in metadata['images']:
    if image['id'] == image_id:
      src_path = DATASET_DIR + 'train/' + image['file_name']
      dest_path = "./dataset/" + category_name + "/" + image['file_name']
      #print('copy', src_path, dest_path)
      copyfile(src_path, dest_path)

def process_category(metadata, category):
  print('process category', category['name'])
  path = "./dataset/" + category['name']

  try:
    os.makedirs(path)
  except OSError:
    print ("Creation of the directory %s failed" % path)
  else:
    print ("Successfully created the directory %s" % path)

  image_counter = 0

  for annotation in metadata['annotations']:
    if annotation['category_id'] == category['id']:
      image_id = annotation['image_id']
      copy_image(metadata, category['name'], image_id)
      image_counter = image_counter + 1
      if image_counter >= MAX_IMAGE_PER_CAT:
        break
    
  print('copied', image_counter, 'images.')
  

if __name__ == "__main__":
  extract_archive('pascal_2012.tgz', './dataset_downloads')
  metadata = read_metadata()

  for cat in metadata['categories']:
    process_category(metadata, cat)