# Import needed package

import pycodestyle

files_to_check = ["../src/load.py","../src/extract.py","../src./transform.py"]

# Create a StyleGuide instance

style_checker = pycodestyle.StyleGuide()

# Run PEP 8 check on multiple files

result = style_checker.check_files(files_to_check)

# Print result of PEP 8 style check

print(result.messages)


