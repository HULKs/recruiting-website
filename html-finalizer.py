import sys
import os
import os.path
import shutil
import bs4

html_path = sys.argv[1]

for root, dirs, files in os.walk(html_path):
  for file in [file for file in files if os.path.splitext(file)[1] == '.html']:
    file_path = os.path.join(root, file)
    soup = None
    with open(file_path) as f:
      soup = bs4.BeautifulSoup(f.read(), 'html.parser')
      for viewer in soup.find_all('x-viewer'):
        new_tag = soup.new_tag('b')
        new_tag.string = f'Viewer of type \'{viewer["type"]}\' for \'{viewer["file"]}\''
        viewer.replace_with(new_tag)
      for editor in soup.find_all('x-editor'):
        new_tag = soup.new_tag('b')
        new_tag.string = f'Editor of type \'{editor["type"]}\' for \'{editor["file"]}\''
        editor.replace_with(new_tag)
      for terminal in soup.find_all('x-terminal'):
        new_tag = soup.new_tag('b')
        new_tag.string = f'Terminal in initial working-directory \'{terminal["working-directory"]}\''
        terminal.replace_with(new_tag)
    with open(file_path, 'w') as f:
      f.write(soup.prettify())
