from textnode import markdown_to_html_node, extract_title
import shutil
import os

def copy():
  cwd = os.getcwd()
  static_path = os.path.join(cwd, 'static')
  public_path = os.path.join(cwd, 'public')
  if os.path.exists(public_path):
    shutil.rmtree(public_path)
  shutil.copytree(static_path, public_path)

def generate_page(from_path: str, template_path: str, dest_path: str):
  print(f"Generating page from {from_path} to {dest_path} using {template_path}")
  try:
    md_f = open(from_path, mode='r')
    temp_f = open(template_path, mode='r')
    dest_f = open(dest_path, 'w')
    markdown = md_f.read()
    html = temp_f.read()
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    html = html.replace('{{ Title }}', title)
    html = html.replace('{{ Content }}', content)
    dest_f.write(html)
  except Exception as e:
    print(e)
  finally:
    md_f.close()
    temp_f.close()
    dest_f.close()

def generate_many_pages(from_path: str, template_path: str, dest_path: str):
  from_path, template_path, dest_path = os.path.join(from_path), os.path.join(template_path), os.path.join(dest_path)
  for path in os.listdir(from_path):
    if path.endswith('.md'):
      new_from_path = os.path.join(from_path, path)
      new_dest_path = os.path.join(dest_path, f'{path[:-2]}html' )
      generate_page(new_from_path, template_path, new_dest_path)

def main():
  copy()
  generate_many_pages('content/', 'template.html', 'public/')

main()