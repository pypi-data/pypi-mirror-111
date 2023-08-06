"""API Extractor - Extract Python docstring written in Markdown format"""

import inspect
import json
import re
from pathlib import Path
from types import BuiltinFunctionType, FunctionType, MethodType
from typing import (
  Any,
  Dict,
  Generator,
  Iterable,
  Optional,
  Set,
  Tuple,
  TypeVar,
  Union,
  cast,
)

with open('package.json', 'r') as f:
  __version__ = json.load(f)['version']


# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html?highlight=napol#docstring-sections
# pylint: disable=line-too-long
DOCSTRING_SECTIONS_RE = re.compile(
  r'(?:Args|Arguments|Attention|Attributes|Caution|Danger|Error|Examples?|Hint|Important|Keyword Args|Keyword Arguments|Methods|Notes?|Parameters|Returns?|Raises?|References|See Also|Tip|Todo|Warnings?|Warns?|Yields?):$',  # noqa: E501
  re.MULTILINE,
)
# pylint: enable=line-too-long
ObjType = TypeVar(
  'ObjType', type, FunctionType, MethodType, BuiltinFunctionType
)


def generate(
  pages: Dict[str, Dict[str, Union[str, Iterable[ObjType]]]],
  output_dir: str,
  indent_size: int = 4,
) -> None:
  """Generates markdown files from given `pages` in `output_dir`.

  Parameters:

  - `pages`: A dictionary of APIs to document.
    Key is page name and value is another dictionary containing
    `title` and `content` keys. Value of `content` key is the
    iterable of python objects to be documented.

  - `output_dir`: The output directory to write the files in.

  - `indent_size`: The indent size for the formatted class and
    function signatures.

  Returns:

  - `None`

  Examples:

  ```py
  >>> from api_extractor import generate
  >>> pages = {
  ...  'api.md': {
  ...    'title': 'API Reference',
  ...    'content': [generate],
  ...    }
  ...  }
  >>> generate(pages, './api/', 2)
  ```
  """
  indent: str = ' ' * indent_size
  out_dir: Path = Path(output_dir)
  out_dir.mkdir(parents=True, exist_ok=True)

  for file_path, values in pages.items():
    markdown_text: str = ''
    for obj in values['content']:
      obj = cast(ObjType, obj)
      markdown_text += render(obj, indent, obj.__name__)
      if inspect.isclass(obj):
        for name, member in get_public_members(obj):
          markdown_text += render(member, indent, name, obj)
    write_to_file(
      markdown_text, out_dir / file_path, cast(str, values['title'])
    )
  print()


def render(
  obj: ObjType,
  indent: str,
  name: str = '',
  parent: Optional[Any] = None,
) -> str:
  """Renders the given `obj` in readable markdown style.

  Parameters:

  - `obj`: The python object to render.

  - `indent`: 4 space or 2 space indent.

  - `name`: The name of the python object.

  - `parent`: The parent python object.

  Returns:

  - Markdown formatted doc of `obj`.
  """
  text_list: list = []
  heading = format_heading(name, parent)
  signature = format_name_and_signature(obj, indent, name)
  base_cls = format_base_cls(cast(type, obj))
  docstring = format_docstring(obj)
  text_list.append(heading)
  text_list.append(signature)

  if base_cls:
    text_list.append(base_cls)
  if docstring:
    text_list.append(docstring)

  text_list.append('')

  return '\n\n'.join(text_list)


def get_public_members(
  obj: object,
) -> Generator[Tuple[str, ObjType], None, None]:
  """Get documentable public members from given `obj`.

  Parameters:

  - `obj`: The object to get the members from.

  Yields:

  - `name`: The name of the member.

  - `member`: The member object.
  """
  for name, member in inspect.getmembers(obj):
    if not name.startswith('_'):
      if (
        inspect.isclass(member)
        or inspect.isfunction(member)
        or inspect.ismethod(member)
        or inspect.iscoroutinefunction(member)
        or isinstance(member, property)
      ):
        yield name, member


def write_to_file(text: str, file: Path, title: str) -> None:
  """Write the `text` to the `file`.

  Parameters:

  - `text`: The text to write

  - `file`: The file to be write the `text` in.

  - `title`: The h1 title of the `file`.

  Returns:

  - `None`
  """
  print(f'Generating {file}...', end='\r')
  text = f'# {title}\n\n' + text
  file.write_text(text, 'utf-8')


def format_heading(name: str, parent: Any) -> str:
  """Get the h2 or h3 markdown formatted heading.

  Parameters:

  - `name`: The name of heading.

  - `parent`: The parent python object to check
    if `name` exists in parent's attributes.

  Returns:

  - h2 or h3 markdown formatted text.
  """
  if getattr(parent, name, None) is not None:
    return f'### `{name}`'
  return f'## `{name}`'


def format_name_and_signature(obj: ObjType, indent: str, name: str = '') -> str:
  """Get markdown formatted class or function name and signature inside
  python code fence. If the total length (class or function name + signature)
  is greater than 80, they will break into next line.

  Parameters:

  - `obj`: The python object to get signature from.

  - `indent`: 4 space or 2 space indent.

  - `name`: The name of the given `obj`.

  Returns:

  - Markdown formatted class or function name and signature inside
  python code fence.
  """
  if not is_property(obj):
    name = obj.__name__

  signature = get_signature(obj)
  prefix = typeof(obj)
  code = name + signature

  if prefix:
    code = prefix + code

  if len(code) > 80:
    start = code.find('(')
    end = code.rfind(')')
    signature = code[start + 1 : end]
    signature = f',\n{indent}'.join(re.split(r'\, (?=\w+\:)', signature))
    code = re.sub(r'\(.+\)', f'(\n{indent}{signature}\n)', code)

  return code_fence(code)


def get_signature(obj: ObjType) -> str:
  """Get the class or function signatures. If the `obj` contains
  `self`, `self` will be dropped.

  Parameters:

  - `obj`: The python object to get signature from.

  Returns:

  - Class or function signature with `self` (if exist).
  """
  if not is_property(obj):
    signature = str(inspect.signature(obj)).replace('(self, ', '(')
    signature = signature.replace('(self)', '()')
  else:
    signature = ''

  return signature


def format_base_cls(obj: type) -> Optional[str]:
  """Get the formatted base classes in string.

  Parameters:

  - `obj`: The python class to find its base classes.

  Returns:

  - A string of `**Bases: <base classes>**`.
  """
  base_cls = get_base_cls(obj)
  if base_cls:
    base_cls_names = ', '.join([f'`{cls.__name__}`' for cls in base_cls])
    return f'**Bases: {base_cls_names}**'
  return None


def get_base_cls(obj: type) -> Optional[Set[type]]:
  """Get a set of base classes of given `obj`.

  Parameters:

  - `obj`: The python class to find its base classes.

  Returns:

  - A set of base classes or `None`.
  """
  if inspect.isclass(obj):
    return set(obj.__bases__)
  return None


def format_docstring(obj: ObjType) -> Optional[str]:
  """Format the docstring with bold docstring sections.

  Parameters:

  - `obj`: The python object to get the docstring from.

  Returns:

  - Bold formatted docstring sections of docstring or `None`.
  """
  docstring = inspect.getdoc(obj)
  if docstring:
    docstring = transform_docstring(docstring)
  return docstring


def transform_docstring(docstring: str) -> str:
  """Make docstring sections bold.

  Parameters:

  - `docstring`: The docstring to bold.

  Returns:

  - Bold formatted docstring sections of docstring.
  """
  matches = DOCSTRING_SECTIONS_RE.finditer(docstring)
  for match in matches:
    matchstr = match.group()
    docstring = docstring.replace(matchstr, f'**{matchstr}**', 1)
  return docstring


def code_fence(string: str) -> str:
  """Wrap the given `string` in python code fence.

  Parameters:

  - `string`: The string to wrap.

  Returns:

  - The string wrapped in python code fence.
  """
  return f'```py\n{string}\n```'


def typeof(obj: Any) -> Optional[str]:
  """Get the definition of the given `obj`.

  Parameters:

  - `obj`: The python object to find its definition.

  Returns:

  - `class ` if class.
  - `def ` if function.
  - `async def ` if async function.
  - `property ` if defined with `@property`.
  - `None` otherwise.
  """
  type_: Optional[str] = None
  if inspect.isclass(obj):
    type_ = 'class '
  elif inspect.iscoroutinefunction(obj):
    type_ = 'async def '
  elif inspect.ismethod(obj) or inspect.isfunction(obj):
    type_ = 'def '
  elif isinstance(obj, property):
    type_ = 'property '
  return type_


def is_property(obj: Any):
  """Check the given `obj` is defined with `@property`.

  Parameters:

  - `obj`: The python object to check.

  Returns:

  - `True` if defined with `@property`, otherwise `False`.
  """
  return isinstance(obj, property)
