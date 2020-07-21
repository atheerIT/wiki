import re
from . import util

source = util.get_entry("CSS.md")
p = re.compile(r'# [^\s]+')
h1 = p.search(source)
print(h1)