import re

# Read the main script
with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Read the new function
with open('script_insights_new.js', 'r', encoding='utf-8') as f:
    new_func = f.read()

# Find and replace the renderInsights function
pattern = r'function renderInsights\(markdownText\) \{[\s\S]*?console\.log\(\'✅ Smart insights rendered\'\);[\s\S]*?\}'
replacement = new_func.strip()

new_content = re.sub(pattern, replacement, content, count=1)

# Write back
with open('script.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('✅ Updated renderInsights function successfully')
