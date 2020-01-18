import sys
import os
import os.path
import shutil
import bs4

html_path = sys.argv[1]

def generate_viewer(soup, attributes):
  paragraph = soup.new_tag('p')
  b = soup.new_tag('b')
  b.string = 'Viewer'
  paragraph.append(b)
  paragraph.append(' of type ')
  code = soup.new_tag('code')
  code.string = attributes['type']
  paragraph.append(code)
  paragraph.append(' for ')
  code = soup.new_tag('code')
  code.string = attributes['file']
  paragraph.append(code)
  return paragraph

def generate_editor(soup, attributes):
  new_tag = soup.new_tag('b')
  new_tag.string = f'Editor of type \'{attributes["type"]}\' for \'{attributes["file"]}\''
  return new_tag

def generate_terminal(soup, attributes):
  new_tag = soup.new_tag('b')
  new_tag.string = f'Terminal in initial working-directory \'{attributes["working-directory"]}\''
  return new_tag

for root, dirs, files in os.walk(html_path):
  for file in [file for file in files if os.path.splitext(file)[1] == '.html']:
    file_path = os.path.join(root, file)
    soup = None
    with open(file_path) as f:
      soup = bs4.BeautifulSoup(f.read(), 'html.parser')
      for viewer in soup.find_all('x-viewer'):
        viewer.replace_with(generate_viewer(soup, viewer))
      for editor in soup.find_all('x-editor'):
        editor.replace_with(generate_editor(soup, editor))
      for terminal in soup.find_all('x-terminal'):
        terminal.replace_with(generate_terminal(soup, terminal))
    with open(file_path, 'w') as f:
      f.write(soup.encode(formatter='html5').decode('utf-8'))
