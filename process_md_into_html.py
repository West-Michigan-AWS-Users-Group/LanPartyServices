import os
import markdown

# Define the root directory and the target directory for HTML files
root_dir = 'lan_party_services'
target_dir = os.path.join(root_dir, 'info_mirror')

# Ensure the target directory exists
os.makedirs(target_dir, exist_ok=True)

# CSS link to be added to each HTML file
css_link = '<link rel="stylesheet" type="text/css" href="../styles.css">'

# Walk through the root directory
for subdir, _, files in os.walk(root_dir):
    if 'README.md' in files:
        readme_path = os.path.join(subdir, 'README.md')
        with open(readme_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Convert markdown to HTML
        html_content = markdown.markdown(md_content)

        # Add the CSS link to the HTML content
        html_content_with_css = f'<html><head>{css_link}</head><body>{html_content}</body></html>'

        # Determine the output HTML file path
        relative_path = os.path.relpath(subdir, root_dir)
        output_dir = os.path.join(target_dir, relative_path)
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'index.html')

        # Write the HTML content to the output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content_with_css)

print("Markdown files have been converted to HTML with CSS and saved in the info_mirror directory.")
