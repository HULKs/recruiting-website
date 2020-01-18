import sys
import os
import os.path
import shutil
import bs4

html_path = sys.argv[1]
source_path = sys.argv[2]

for root, dirs, files in os.walk(html_path):
  for file in [file for file in files if os.path.splitext(file)[1] == '.html']:
    file_path = os.path.join(root, file)
    with open(file_path) as f:
      soup = bs4.BeautifulSoup(f.read(), 'html.parser')
      for img in soup.find_all('img'):
        img_target_path = os.path.join(root, img['src'])
        img_source_path = os.path.join(source_path, os.path.relpath(img_target_path, start=html_path))
        print(f'{img_source_path} -> {img_target_path} (for {file_path})')
        shutil.copyfile(img_source_path, img_target_path)
