

import os
import re

def fix_file(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix multi-line variable tags {{ ... }}
    # We find things like {{ \n value }} and turn them into {{ value }}
    def join_variable_tag(match):
        # validation: don't join if it looks like a script or style block, though {{}} usually safe
        full_tag = match.group(0)
        # Replace newlines and extra spaces with a single space
        cleaned = re.sub(r'\s+', ' ', full_tag)
        return cleaned

    # Regex for {{ ... }} spanning multiple lines
    new_content = re.sub(r'\{\{.*?\}\}', join_variable_tag, content, flags=re.DOTALL)

    # 2. Fix multi-line block tags {% ... %}
    # Regex for {% ... %} spanning multiple lines
    new_content = re.sub(r'\{%.*?%\}', join_variable_tag, new_content, flags=re.DOTALL)

    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed {filepath}")
    else:
        print(f"No changes needed for {filepath}")

base_dir = r"c:\Users\PRIYANSHI\Desktop\ibanking\templates"
files_to_fix = [
    "base_portal.html", 
    "customer_dashboard.html", 
    "transactions.html",
    "employee/kyc_requests.html", 
    "admin_dashboard.html",
    "employee_dashboard.html"
]

for fname in files_to_fix:
    full_path = os.path.join(base_dir, fname)
    fix_file(full_path)

