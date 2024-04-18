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
