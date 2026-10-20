import glob
import re

for html_file in sorted(glob.glob("*.html")):
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    img_tags = re.findall(r'<img[^>]+>', content, re.DOTALL | re.IGNORECASE)
    for tag in img_tags:
        src_match = re.search(r'src=["\']([^"\']+)["\']', tag)
        alt_match = re.search(r'alt=["\']([^"\']*)["\']', tag)
        src = src_match.group(1) if src_match else "no-src"
        alt = alt_match.group(1) if alt_match else "MISSING"
        # Flatten spaces in tag
        clean_tag = " ".join(tag.split())
        print(f"{html_file} | {src} | alt=\"{alt}\"")
