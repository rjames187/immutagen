from htmlnode import LeafNode, ParentNode
import re

# constants
text_type_text = "text"
text_type_code = "code"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_image = "image"
text_type_link = "link"

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

class TextNode:
  def __init__(self, text:str, text_type: str, url: str=None) -> None:
    self.text = text
    self.text_type = text_type
    self.url = url
  
  def __eq__(self, other: "TextNode") -> bool:
    if self.text != other.text:
      return False
    if self.text_type != other.text_type:
      return False
    if self.url != other.url:
      return False
    return True
  
  def __repr__(self) -> str:
    return f'TextNode({self.text}, {self.text_type}, {self.url})'

def split_nodes_delimiter(old_nodes: 'list[TextNode]', delimiter: str, text_type: str) -> 'list[TextNode]':
  res = []
  for old_node in old_nodes:
    if old_node.text_type != text_type_text:
      res.append(old_node)
    else:
      new_texts = old_node.text.split(delimiter)
      if len(new_texts) % 2 == 0:
        raise Exception(f'All opening {delimiter} delimiters must have a closing delimiter')
      for i in range(len(new_texts)):
        if len(new_texts[i]) == 0:
          continue
        if i % 2 == 0:
          res.append(TextNode(new_texts[i], text_type_text))
        else:
          res.append(TextNode(new_texts[i], text_type))
  return res

def extract_markdown_images(text: str) -> 'tuple[list[str]]':
  matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
  return matches

def extract_markdown_links(text: str) -> 'tuple[list[str]]':
  matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
  return matches

def split_nodes_image(old_nodes: 'list[TextNode]') -> 'list[TextNode]':
  res = []
  for old_node in old_nodes:
    if old_node.text_type != text_type_text:
      res.append(old_node)
      continue
    text = old_node.text
    images = extract_markdown_images(text)
    if len(images) == 0:
      res.append(old_node)
      continue
    for image in images:
      split = text.split(f"![{image[0]}]({image[1]})", 1)
      if split[0] != "":
        res.append(TextNode(split[0], text_type_text))
      res.append(TextNode(image[0], text_type_image, image[1]))
      text = split[1]
    if text != "":
      res.append(TextNode(text, text_type_text))
  return res

def split_nodes_link(old_nodes: 'list[TextNode]') -> 'list[TextNode]':
  res = []
  for old_node in old_nodes:
    if old_node.text_type != text_type_text:
      res.append(old_node)
      continue
    text = old_node.text
    links = extract_markdown_links(text)
    if len(links) == 0:
      res.append(old_node)
      continue
    for link in links:
      split = text.split(f"[{link[0]}]({link[1]})", 1)
      if split[0] != "":
        res.append(TextNode(split[0], text_type_text))
      res.append(TextNode(link[0], text_type_link, link[1]))
      text = split[1]
    if text != "":
      res.append(TextNode(text, text_type_text))
  return res

def text_to_textnodes(text: str) -> 'list[TextNode]':
  nodes = split_nodes_image([TextNode(text, text_type_text)])
  nodes = split_nodes_link(nodes)
  nodes = split_nodes_delimiter(nodes, '`', text_type_code)
  nodes = split_nodes_delimiter(nodes, '**', text_type_bold)
  nodes = split_nodes_delimiter(nodes, '*', text_type_italic)
  return nodes

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
  text_type = text_node.text_type
  text = text_node.text
  if text_type == text_type_text:
    return LeafNode(None, text)
  elif text_type == text_type_bold:
    return LeafNode("b", text)
  elif text_type == text_type_italic:
    return LeafNode("i", text)
  elif text_type == text_type_code:
    return LeafNode("code", text)
  elif text_type == text_type_link:
    return LeafNode("a", text, {"href": text_node.url})
  elif text_type == text_type_image:
    return LeafNode("img", None, {"src": text_node.url, "alt": text})
  else:
    raise Exception("Text node type must be bold, italic, code, link, or image")

def markdown_to_blocks(markdown: str) -> 'list[str]':
  blocks = re.split(r'\n\n+', markdown)
  return list(map(lambda x: x.strip(), blocks))

def block_to_block_type(block: str) -> str:
  if re.fullmatch(r"^#{1,6} .+", block):
    return block_type_heading
  elif block.startswith('```') and block.endswith('```'):
    return block_type_code
  lines = block.split('\n')
  if len(list(filter(lambda x: x.startswith('>'), lines))) == len(lines):
    return block_type_quote
  if len(list(filter(lambda x: re.fullmatch(r'^[\*-] '), lines))) == len(lines):
    return block_type_unordered_list
  for i in range(len(lines)):
    if not lines[i].startswith(f'{i + 1}. '):
      break
    if i == len(lines) - 1:
      return block_type_ordered_list
  return block_type_paragraph

def quote_block_to_html_node(block: str) -> ParentNode:
  children = []
  for line in block.split('\n'):
    textnodes = text_to_textnodes(line[1:])
    children.extend(list(map(text_node_to_html_node, textnodes)))
  return ParentNode('blockquote', children)

def unordered_list_block_to_html_node(block: str) -> ParentNode:
  items = []
  for line in block.split('\n'):
    textnodes = text_to_textnodes(line[2:])
    children = list(map(text_node_to_html_node, textnodes))
    items.append(ParentNode('li', children))
  return ParentNode('ul', items)

def ordered_list_block_to_html_node(block: str) -> ParentNode:
  items = []
  for line in block.split('\n'):
    textnodes = text_to_textnodes(line[3:])
    children = list(map(text_node_to_html_node, textnodes))
    items.append(ParentNode('li', children))
  return ParentNode('ol', items)

def code_block_to_html_node(block: str) -> ParentNode:
  textnodes = text_to_textnodes(block[3:-3])
  children = list(map(text_node_to_html_node, textnodes))
  return ParentNode('pre', [ParentNode('code', children)])

def heading_block_to_html_node(block: str) -> ParentNode:
  level = block.split(' ')[0].count('#')
  textnodes = text_to_textnodes(block[level+1:])
  children = list(map(text_node_to_html_node, textnodes))
  return ParentNode(f'h{level}', children)

def paragraph_block_to_html_node(block: str) -> ParentNode:
  textnodes = text_to_textnodes(block)
  children = list(map(text_node_to_html_node, textnodes))
  return ParentNode('p', children)

def markdown_to_html_node(markdown: str) -> ParentNode:
  children = []
  blocks = markdown_to_blocks(markdown)
  for block in blocks:
    block_type = block_to_block_type(block)
    if block_type == block_type_quote:
      children.append(quote_block_to_html_node(block))
    elif block_type == block_type_unordered_list:
      children.append(unordered_list_block_to_html_node(block))
    elif block_type == block_type_ordered_list:
      children.append(ordered_list_block_to_html_node(block))
    elif block_type == block_type_code:
      children.append(code_block_to_html_node(block))
    elif block_type == block_type_heading:
      children.append(heading_block_to_html_node(block))
    elif block_type == block_type_paragraph:
      children.append(paragraph_block_to_html_node(block))
  return ParentNode('div', children)
