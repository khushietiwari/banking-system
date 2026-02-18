
import os
import re

file_path = r"c:\Users\PRIYANSHI\Desktop\ibanking\templates\customer_dashboard.html"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find 'Transfer' followed by newlines/spaces and 'Received'
    # We want to replace it with 'Transfer Received'
    
    pattern = re.compile(r"txn\.transaction_type\s*==\s*'Transfer\s+Received'")
    
    matches = pattern.findall(content)
    print(f"Found {len(matches)} matches.")
    for m in matches:
        print(f"Match: {m[:20]}...{m[-20:]}")

    if not matches:
        print("No matches found using specific pattern. Trying broader pattern.")
        pattern = re.compile(r"'Transfer\s+Received'")
        matches = pattern.findall(content)
        print(f"Found {len(matches)} matches with broader pattern.")

    new_content = pattern.sub("'Transfer Received'", content)

    if content != new_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Successfully patched the file.")
    else:
        print("No changes made to the file.")

except Exception as e:
    print(f"Error: {e}")
