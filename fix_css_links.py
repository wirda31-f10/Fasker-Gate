import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace href="dashboard.css" with href="css/dashboard.css"
    content = content.replace('href="dashboard.css"', 'href="css/dashboard.css"')
    content = content.replace('href="index.css"', 'href="css/index.css"')
    content = content.replace('href="masuk.css"', 'href="css/masuk.css"')
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Fixed CSS links!")
