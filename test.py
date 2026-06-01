import requests
import re

URL = "https://mir-x-tg.netlify.app/"

response = requests.get(URL, timeout=10)
html = response.text

# Look for form action or onclick
print("=" * 50)
print("SEARCHING FOR FORM/INPUT/BUTTON...")
print("=" * 50)

# Find input fields
inputs = re.findall(r'<input[^>]*>', html)
for inp in inputs:
    print(f"INPUT: {inp}")

# Find buttons
buttons = re.findall(r'<button[^>]*>.*?</button>', html, re.DOTALL)
for btn in buttons:
    print(f"BUTTON: {btn[:200]}")

# Find all JavaScript function calls
calls = re.findall(r'fetch\(["\']([^"\']+)["\']', html)
print(f"\nFETCH URLs found: {len(calls)}")
for c in calls:
    print(f"  → {c}")

# Find axios calls
axios_calls = re.findall(r'axios\.(get|post)\(["\']([^"\']+)["\']', html)
print(f"\nAXIOS URLs found: {len(axios_calls)}")
for method, url in axios_calls:
    print(f"  → {method.upper()} {url}")

# Find any URL patterns
urls = re.findall(r'["\']([^"\']*(?:signal|asset|api|data)[^"\']*)["\']', html, re.IGNORECASE)
print(f"\nSIGNAL/ASSET/API URLs: {len(urls)}")
for u in urls:
    print(f"  → {u}")
