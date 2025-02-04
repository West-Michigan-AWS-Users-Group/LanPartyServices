import os
import markdown
from typing import List


def convert_md_to_html(root_dir: str, target_dir: str) -> None:
    """
    Convert Markdown files to HTML and save them in the target directory.

    :param root_dir: The root directory to search for Markdown files.
    :param target_dir: The target directory to save the converted HTML files.
    """
    # Ensure the target directory exists
    os.makedirs(target_dir, exist_ok=True)

    # CSS link to be added to each HTML file
    css_link = '<link rel="stylesheet" type="text/css" href="../styles.css">'

    # Walk through the root directory
    for subdir, _, files in os.walk(root_dir):
        # Skip the discord_bot directory
        if "discord_bot" in subdir:
            continue
        if "api" in subdir:
            continue

        if "README.md" in files:
            readme_path = os.path.join(subdir, "README.md")
            with open(readme_path, "r", encoding="utf-8") as f:
                md_content = f.read()

            # Convert markdown to HTML
            html_content = markdown.markdown(md_content)

            # Add the CSS link to the HTML content
            html_content_with_css = (
                f"<html><head>{css_link}</head><body>{html_content}</body></html>"
            )

            # Determine the output HTML file path
            relative_path = os.path.relpath(subdir, root_dir)
            output_dir = os.path.join(target_dir, relative_path)
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, "index.html")

            # Write the HTML content to the output file
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content_with_css)

    print(
        "Markdown files have been converted to HTML with CSS and saved in the info_mirror directory."
    )


def render_script_js(root_dir: str, script_path: str) -> None:
    """
    Render the script.js file with the folders in the root directory, excluding 'core' and 'info_mirror'.

    :param root_dir: The root directory to search for folders.
    :param script_path: The path to the script.js file to be updated.
    """
    folders: List[str] = [
        d
        for d in os.listdir(root_dir)
        if os.path.isdir(os.path.join(root_dir, d))
        and d
        not in ["__pycache__", "core", "info_mirror", "common", "discord_bot", "api"]
    ]

    # JavaScript code to be written to the script.js file
    js_code = f"""
        document.addEventListener("DOMContentLoaded", function() {{
            const folders = {folders};
            const folderList = document.getElementById("folder-list");
    
            // Sort folders alphabetically
            folders.sort((a, b) => a.localeCompare(b, undefined, {{ sensitivity: 'base' }}));
    
            folders.forEach(folder => {{
                const listItem = document.createElement("li");
                const link = document.createElement("a");
                link.href = `/${{folder}}/index.html`;
    
                // Replace underscores with spaces and capitalize each word, except for specific cases
                let formattedName;
                if (folder === 'ut2k4') {{
                    formattedName = 'Unreal Tournament 2004';
                }} else if (folder === 'ut99') {{
                    formattedName = 'Unreal Tournament 1999';
                }} else if (folder === 'bar') {{
                    formattedName = 'Beyond All Reason';
                }} else if (folder === 'cnc_generals_zero_hour') {{
                    formattedName = 'Command and Conquer Generals: Zero Hour';
                }} else {{
                    formattedName = folder.replace(/_/g, ' ').replace(/\\b\\w/g, char => char.toUpperCase());
                }}
                link.textContent = formattedName;
    
                listItem.appendChild(link);
                folderList.appendChild(listItem);
            }});
        }});
    """
    # Write the JavaScript code to the script.js file
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(js_code)

    print(f"Script.js file has been updated with folders from {root_dir}.")


if __name__ == "__main__":
    root_directory = "lan_party_services"
    target_directory = os.path.join(root_directory, "info_mirror/site")
    script_js_path = os.path.join(target_directory, "script.js")

    convert_md_to_html(root_directory, target_directory)
    render_script_js(root_directory, script_js_path)
