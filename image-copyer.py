import sys
import os.path
import shutil
import bs4

html_path = sys.argv[1]
target_path = os.path.dirname(html_path)
source_path = sys.argv[2]

with open(sys.argv[1]) as f:
  soup = bs4.BeautifulSoup(f.read(), 'html.parser')
  for img in soup.find_all('img'):
    img_source_path = os.path.join(source_path, img['src'])
    img_target_path = os.path.join(target_path, img['src'])
    print(f'{img_source_path} -> {img_target_path} (for {html_path})')
    shutil.copyfile(img_source_path, img_target_path)
