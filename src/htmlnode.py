class HTMLNode:
  def __init__(self, tag: str=None, value: str=None, children: 'list[HTMLNode]'=None, props: dict=None) -> None:
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props
  
  def to_html(self) -> str:
    raise NotImplementedError
  
  def props_to_html(self) -> str:
    if self.props == None:
      return ''
    
    attributes = []
    for key in self.props:
      value = self.props[key]
      attribute = f'{key}="{value}"'
      attributes.append(attribute)
    return ' '.join(attributes)
  
  def __repr__(self) -> str:
    return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'

class LeafNode(HTMLNode):
  def __init__(self, tag: str=None, value: str=None, props: dict=None) -> None:
    super().__init__(tag, value, None, props)

  def to_html(self) -> str:
    if self.value == None:
      raise ValueError
    if self.tag == None:
      return self.value
    space = ' ' if self.props != None and len(self.props) > 0 else ''
    return f'<{self.tag}{space}{self.props_to_html()}>{self.value}</{self.tag}>'
