import markdown2
import weasyprint
import re
from pygments import highlight
from pygments.lexers import BashLexer, PythonLexer, get_lexer_by_name
from pygments.formatters import HtmlFormatter

with open('img_base64.txt', 'r', encoding='utf-8') as f:
    img_base64 = f.read().strip()

with open('README.md', 'r', encoding='utf-8') as f:
    md = f.read()

# Logo
md = md.replace('![Logo GlicoCare](img/glicocare.png)', 
                f'<p style="text-align:center;"><img src="data:image/png;base64,{img_base64}" alt="Logo GlicoCare" style="max-width:300px;"></p>')

# Evidenziazione sintassi con Pygments
def highlight_code(match):
    lang = match.group(1).strip() or 'text'
    code = match.group(2)
    try:
        lexer = get_lexer_by_name(lang, stripall=True)
    except:
        lexer = get_lexer_by_name('text', stripall=True)
    formatter = HtmlFormatter(style='github-dark', cssclass='highlight')
    return highlight(code, lexer, formatter)

md = re.sub(r'```(\w+)\n(.*?)```', highlight_code, md, flags=re.DOTALL)

html = markdown2.markdown(
    md,
    extras=['tables', 'fenced-code-blocks', 'code-friendly']
)

pygments_css = HtmlFormatter(style='github-dark').get_style_defs('.highlight')

css = f"""
@page {{
    margin: 1.2cm;
    size: A4;
}}
body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    margin: 0;
    color: #1f2328;
    line-height: 1.5;
    font-size: 10pt;
    hyphens: none;
    word-break: normal;
    overflow-wrap: normal;
    text-align: left;
}}
img {{ max-width: 100%; height: auto; }}
blockquote {{
    border-left: 4px solid #d0d7de;
    margin: 12px 0;
    padding: 8px 16px;
    color: #656d76;
    background: #f6f8fa;
    border-radius: 0 6px 6px 0;
}}
ol, ul {{ padding-left: 24px; margin: 8px 0; }}
li {{ margin: 4px 0; }}
.highlight {{
    background: #f6f8fa;
    padding: 12px;
    border-radius: 6px;
    font-size: 9pt;
    line-height: 1.45;
    overflow-x: auto;
    margin: 12px 0;
}}
.highlight pre {{
    margin: 0;
    padding: 0;
    background: none;
    font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace;
}}
:not(.highlight) > code {{
    background: rgba(175,184,193,0.2);
    padding: 2px 5px;
    border-radius: 6px;
    font-size: 9pt;
    font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace;
}}
{pygments_css}
h1 {{ font-weight: 600; font-size: 16pt; border-bottom: 1px solid #d0d7de; padding-bottom: 6px; margin-top: 24px; margin-bottom: 14px; }}
h2 {{ font-weight: 600; font-size: 13pt; border-bottom: 1px solid #d0d7de; padding-bottom: 4px; margin-top: 20px; margin-bottom: 12px; }}
a {{ color: #0969da; text-decoration: none; }}
table {{ border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 9pt; }}
th, td {{ border: 1px solid #d0d7de; padding: 6px 12px; text-align: left; }}
th {{ background: #f6f8fa; font-weight: 600; }}
tr:nth-child(even) {{ background: #f6f8fa; }}
sup {{ font-size: 8pt; color: #656d76; }}
strong {{ font-weight: 600; }}
"""

full_html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><style>{css}</style></head>
<body>{html}</body>
</html>"""

weasyprint.HTML(string=full_html).write_pdf('README.pdf')
print("Creato README.pdf")