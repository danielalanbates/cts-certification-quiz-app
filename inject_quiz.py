import json
import re
import shutil

# Paths
workspace_json = "/Users/daniel/code/cts-mastery-quiz-native/quizData.json"
icloud_html = "/Users/daniel/Library/Mobile Documents/com~apple~CloudDocs/Downloads/CTS_Mastery_Quiz.html"
icloud_native_json = "/Users/daniel/Library/Mobile Documents/com~apple~CloudDocs/Downloads/CTS_Mastery_Quiz_Native/quizData.json"

# Load the new questions
with open(workspace_json, "r") as f:
    data_str = f.read()

# 1. Update the HTML file
with open(icloud_html, "r") as f:
    html_content = f.read()

# Replace the data array in the HTML
new_html_content = re.sub(
    r"const data = (\[.*?\]);",
    f"const data = {data_str};",
    html_content,
    flags=re.DOTALL
)

with open(icloud_html, "w") as f:
    f.write(new_html_content)

print(f"Updated HTML file at: {icloud_html}")

# 2. Update the Native App JSON file
shutil.copy2(workspace_json, icloud_native_json)

print(f"Copied JSON to Native App folder at: {icloud_native_json}")
