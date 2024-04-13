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