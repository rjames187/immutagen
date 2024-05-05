from htmlnode import LeafNode

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

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
  text_type = text_node.text_type
  text = text_node.text
  if text_type == "text":
    return LeafNode(None, text)
  elif text_type == "bold":
    return LeafNode("b", text)
  elif text_type == "italic":
    return LeafNode("i", text)
  elif text_type == "code":
    return LeafNode("code", text)
  elif text_type == "link":
    return LeafNode("a", text, {"href": text_node.url})
  elif text_type == "image":
    return LeafNode("img", None, {"src": text_node.url, "alt": text})
  else:
    raise Exception("Text node type must be bold, italic, code, link, or image")