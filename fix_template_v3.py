
import re
import os

path = r"c:\Users\PRIYANSHI\Desktop\ibanking\templates\customer_dashboard.html"

print(f"Reading {path}...")
with open(path, 'rb') as f:
    content = f.read().decode('utf-8')

# 1. Fix the split string
# Pattern: txn.transaction_type == 'Transfer<newlines/spaces>Received'
pattern = re.compile(r"txn\.transaction_type\s*==\s*'Transfer\s+Received'")
matches = pattern.findall(content)
print(f"Found {len(matches)} broken matches.")

if matches:
    new_content = pattern.sub("txn.transaction_type == 'Transfer Received'", content)
    
    # Write back
    with open(path, 'wb') as f:
        f.write(new_content.encode('utf-8'))
    print("Wrote fixed content.")
    
    # Read back immediately
    with open(path, 'rb') as f:
        check_content = f.read().decode('utf-8')
    
    # Check if it persists
    if "txn.transaction_type == 'Transfer Received'" in check_content:
        print("Verification: FIXED string found in file.")
    else:
        print("Verification: FIXED string NOT found (weird).")
        
    # Check for split
    if re.search(r"txn\.transaction_type\s*==\s*'Transfer\s+Received'", check_content):
        print("Verification: BROKEN split still exists!")
    else:
        print("Verification: BROKEN split is GONE.")

else:
    print("No broken matches found to fix.")
    # Check if maybe it's the OTHER broken state (missing txn.transaction_type)
    pattern2 = re.compile(r"or\s+'Transfer\s+Received'")
    matches2 = pattern2.findall(content)
    if matches2:
        print(f"Found {len(matches2)} logic-broken matches (missing txn check). fixing...")
        new_content = pattern2.sub("or txn.transaction_type == 'Transfer Received'", content)
        with open(path, 'wb') as f:
            f.write(new_content.encode('utf-8'))
        print("Fixed logic-broken matches.")
