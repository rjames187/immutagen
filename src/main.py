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
  from_path, template_path, dest_path = os.path.join(from_path), os.path.join(template_path), os.path.join(dest_path)
  try:
    md_f = open(from_path, mode='r')
    temp_f = open(template_path, mode='r')
    dest_f = open(dest_path, 'w')
    markdown = md_f.read()
    html = temp_f.read()
    content = markdown_to_html_node(markdown).to_html()
    print(content)
    title = extract_title(markdown)
    html = html.replace('{{ Title }}', title)
    html = html.replace('{{ Content }}', content)
    dest_f.write(html)
  except Exception as e:
    print(type(e))
    print(e)
  finally:
    md_f.close()
    temp_f.close()
    dest_f.close()

def main():
  copy()
  generate_page('content/index.md', 'template.html', 'public/index.html')

main()