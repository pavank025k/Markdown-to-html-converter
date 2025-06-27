import sys
import re
import argparse

def convert_markdown_to_html(markdown_text):
    # Convert headers
    markdown_text = re.sub(r'^#\s+(.*)$', r'<h1>\1</h1>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^##\s+(.*)$', r'<h2>\1</h2>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^###\s+(.*)$', r'<h3>\1</h3>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^####\s+(.*)$', r'<h4>\1</h4>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^#####\s+(.*)$', r'<h5>\1</h5>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^######\s+(.*)$', r'<h6>\1</h6>', markdown_text, flags=re.MULTILINE)

    # Convert bold and italic
    markdown_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', markdown_text)
    markdown_text = re.sub(r'__(.*?)__', r'<strong>\1</strong>', markdown_text)
    markdown_text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', markdown_text)
    markdown_text = re.sub(r'_(.*?)_', r'<em>\1</em>', markdown_text)

    # Convert inline code
    markdown_text = re.sub(r'`(.*?)`', r'<code>\1</code>', markdown_text)

    # Convert links
    markdown_text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', markdown_text)

    # Convert unordered lists
    markdown_text = re.sub(r'^\*\s+(.*)$', r'<li>\1</li>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^-\s+(.*)$', r'<li>\1</li>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^\+\\s+(.*)$', r'<li>\1</li>', markdown_text, flags=re.MULTILINE)
    
    # Wrap consecutive list items in <ul> tags
    markdown_text = re.sub(r'(<li>.*</li>\n?)+', lambda m: f'<ul>\n{m.group(0)}\n</ul>', markdown_text)

    # Convert ordered lists
    markdown_text = re.sub(r'^\d+\.\s+(.*)$', r'<li>\1</li>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'(<li>.*</li>\n?)+', lambda m: f'<ol>\n{m.group(0)}\n</ol>', markdown_text)

    # Convert paragraphs (handle multiple newlines)
    markdown_text = re.sub(r'([^\n]+\n+)', r'<p>\1</p>', markdown_text)

    # Handle line breaks
    markdown_text = markdown_text.replace('\n', '<br>\n')

    # Remove empty paragraphs
    markdown_text = re.sub(r'<p>\s*</p>', '', markdown_text)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Converted Markdown</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
        code {{ background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px; }}
        pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 3px; overflow-x: auto; }}
    </style>
</head>
<body>
{markdown_text}
</body>
</html>"""

def main():
    parser = argparse.ArgumentParser(description='Convert Markdown to HTML')
    parser.add_argument('input_file', help='Path to the input Markdown file')
    parser.add_argument('output_file', help='Path to the output HTML file')
    
    args = parser.parse_args()
    
    try:
        with open(args.input_file, 'r', encoding='utf-8') as md_file:
            markdown_content = md_file.read()
        
        html_content = convert_markdown_to_html(markdown_content)
        
        with open(args.output_file, 'w', encoding='utf-8') as html_file:
            html_file.write(html_content)
        
        print(f"Successfully converted {args.input_file} to {args.output_file}")
    
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 