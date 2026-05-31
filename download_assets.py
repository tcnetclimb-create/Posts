import re
import urllib.request
import os
from urllib.parse import urlparse

html_path = r"c:\Users\alice\Downloads\tcnet-posts\index.html"
base_dir = r"c:\Users\alice\Downloads\tcnet-posts"
files_dir = os.path.join(base_dir, "tcnet-posts_files")
os.makedirs(files_dir, exist_ok=True)

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'(src|href)=["\'](https?://[^"\']+?)["\']'

def download_file(match):
    attr = match.group(1)
    url = match.group(2)
    
    parsed = urlparse(url)
    ext = os.path.splitext(parsed.path)[1].lower()
    
    # Determine if it's a file to download
    # Usually images, styles, scripts
    is_file = ext in ['.css', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.js', '.pdf', '.webp', '.ico']
    
    if not is_file and attr == 'href':
        return match.group(0)
        
    filename = os.path.basename(parsed.path)
    if not filename:
        return match.group(0)
        
    local_path = os.path.join(files_dir, filename)
    local_relative = f'./tcnet-posts_files/{filename}'
    
    if not os.path.exists(local_path):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response, open(local_path, 'wb') as out_file:
                out_file.write(response.read())
            print(f"Downloaded: {url} -> {local_path}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            return match.group(0)
    else:
        # Already exists
        pass
            
    return f'{attr}="{local_relative}"'

new_content = re.sub(pattern, download_file, content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Done")
