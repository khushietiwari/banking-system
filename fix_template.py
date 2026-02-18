
import os

file_path = r"c:\Users\PRIYANSHI\Desktop\ibanking\templates\customer_dashboard.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Lines 84-85
# Pattern: {% if txn.transaction_type == 'Deposit' or txn.transaction_type == 'Transfer\n                                            Received' %}
# We will match the string roughly and just replace the specific bad split string.

old_string_1 = "txn.transaction_type == 'Transfer\n                                            Received'"
new_string_1 = "txn.transaction_type == 'Transfer Received'"

# Fix 2: Lines 103-104
old_string_2 = "txn.transaction_type == 'Transfer\n                                        Received'"
new_string_2 = "txn.transaction_type == 'Transfer Received'"

# Since exact indentation might vary slightly, I'll do a more generic replace
# Replace "Transfer\n                                            Received" with "Transfer Received"
# I will finding the occurrences of 'Transfer' followed by whitespace and 'Received' inside the template tag logic if possible.
# But string replace is safer if I can construct the exact string.

# Let's try to normalize the file content first? No.

# Let's look for the specific split string: 'Transfer' + newline + many spaces + 'Received'
# I'll use regex to be safe.
import re

pattern = re.compile(r"'Transfer\s+Received'")
# This matches 'Transfer' followed by any whitespace (including newlines) followed by 'Received' in single quotes.
# We want to replace it with 'Transfer Received' (single space).

new_content = pattern.sub("'Transfer Received'", content)

if content == new_content:
    print("No changes made. Pattern not found.")
else:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully patched the file.")
