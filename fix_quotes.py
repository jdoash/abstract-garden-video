#!/usr/bin/env python3
import re

with open('.github/workflows/memory-story-system.yml', 'r') as f:
    content = f.read()

# Fix pattern: "text" - Author, Year", should be "text - Author, Year",
pattern = r'quote: "(.*?)" - (.*?)",'
replacement = r'quote: "\1 - \2",'

fixed = re.sub(pattern, replacement, content)

with open('.github/workflows/memory-story-system.yml', 'w') as f:
    f.write(fixed)

print("Fixed all quotes")