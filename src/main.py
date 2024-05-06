from textnode import TextNode
import shutil
import os

def copy():
  cwd = os.getcwd()
  static_path = os.path.join(cwd, 'static')
  public_path = os.path.join(cwd, 'public')
  if os.path.exists(public_path):
    shutil.rmtree(public_path)
  shutil.copytree(static_path, public_path)

def main():
  copy()

main()