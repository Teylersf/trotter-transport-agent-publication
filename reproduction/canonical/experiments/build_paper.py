"""Assemble manuscript and LaTeX body; compilation is a separate checked step."""
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
paper = ROOT/'paper'


def demote_headings(text, amount=1):
    return re.sub(r'^(#{1,5})(?= )', lambda match: match[1] + '#' * amount,
                  text, flags=re.M)


def journal_concordance():
    path = paper/'revision-journal-concordance.md'
    if not path.exists():
        return ''
    text = demote_headings(path.read_text(encoding='utf-8').strip())
    text = re.sub(r'^### Journal edition and statement concordance$',
                  '### 3.1. Journal edition and statement concordance', text, count=1,
                  flags=re.M)
    if not text.startswith('### 3.1.'):
        raise ValueError('Unexpected journal-concordance heading')
    return text


def source_appendix():
    path = paper/'revision-source-quotes.md'
    if not path.exists():
        return ''
    text = path.read_text(encoding='utf-8')
    if text.count('## C1.') != 1:
        raise ValueError('Expected exactly one C1 source-quotation section')
    body = '## C1.' + text.split('## C1.', 1)[1]
    body = body.split('\n## Integration boundary', 1)[0].strip()
    body = body.replace(
        " The published registry's p.32 locator is one page early and should be "
        'corrected in a revision, without changing the archived version-1 record.', '')
    paragraphs = body.split('\n\n')
    for index, paragraph in enumerate(paragraphs):
        if re.match(r'^\*\*(?:Correct )?Locators?:\*\*', paragraph, flags=re.I):
            paragraphs[index] = paragraph.rstrip()+' [1]'
    body = '\n\n'.join(paragraphs)
    ids = re.findall(r'^## C(\d+)\.', body, flags=re.M)
    if ids != [str(i) for i in range(1, 11)]:
        raise ValueError('Source appendix must preserve C1 through C10 in order')
    body = re.sub(r'^## C(\d+)\. (.+)$',
                  lambda match: f'### A.{match[1]}. {match[2]} (C{match[1]})',
                  body, flags=re.M)
    provenance = text.split('The supplied/official v2 PDF', 1)[1].split('\n\n', 1)[0]
    conventions = text.split('**Reading convention.**', 1)[1].split('\n## C1.', 1)[0]
    intro = (
        '## Appendix A. Attributed source statements and equation reproductions\n\n'
        'The quotations and source equations below are attributed to the audited '
        'arXiv v2 [1]. Their printed preprint pages and TeX line numbers are retained. '
        'Section 3.1 supplies the matching printed/PDF pages and equation labels in '
        'the directly inspected journal article [2]. Each of these ten correction '
        'groups persists at its mapped journal location. The equation reproductions '
        'here identify the original arXiv expressions; journal agreement was checked '
        'separately and is not inferred from identical numbering.\n\n'
        'The supplied/official v2 PDF' + provenance + '\n\n'
        '**Reading convention.** ' + conventions.strip() + '\n\n'
    )
    return intro + body


def numerical_appendix():
    path = paper/'revision-numerical-provenance.md'
    if not path.exists():
        return ''
    text = path.read_text(encoding='utf-8')
    marker = '### Matrix and state norms'
    if text.count(marker) != 1:
        raise ValueError('Unexpected numerical-provenance appendix structure')
    body = marker + text.split(marker, 1)[1]
    index = 0

    def number_heading(match):
        nonlocal index
        index += 1
        return f'### B.{index}. {match[1]}'

    body = re.sub(r'^### (.+)$', number_heading, body, flags=re.M)
    body = body.replace(
        ' A DOI archive, if later obtained, must contain that same verified '
        'snapshot rather than a mutable working directory.', '')
    intro = (
        '## Appendix B. Numerical provenance and reproducible constructions\n\n'
        'All values below come from the released scientific snapshot '
        '`1fb4be68eecce95b93adb8026c4e3d29fb442583`. '
        'The appendix documents the existing calculations and their error '
        'qualifications; no new data or fitted constants are introduced.\n\n'
    )
    return intro + body.strip()


resource = (paper/'resource-discussion.md').read_text(encoding='utf-8')
resource = resource.replace('# Resource implications and the scope of the numerical evidence',
                            '## 6. Discussion: resources and numerical evidence')
resource = re.sub(r'^## ', '### ', resource, flags=re.M).replace('### 6. Discussion:', '## 6. Discussion:')
core = (paper/'core.md').read_text(encoding='utf-8')
concordance = journal_concordance()
section_four = '## 4. Results: regularity and finite-grid resource bounds'
if core.count(section_four) != 1:
    raise ValueError('Expected exactly one Section 4 insertion boundary')
if concordance:
    core = core.replace(section_four, concordance+'\n\n'+section_four, 1)
closing = (paper/'closing.md').read_text(encoding='utf-8')
references_marker = '## References\n'
if closing.count(references_marker) != 1:
    raise ValueError('Expected exactly one References boundary')
closing_body, references = closing.split(references_marker, 1)
appendices = [text for text in (source_appendix(), numerical_appendix()) if text]
content = '\n\n'.join([core.strip(), resource.strip(), closing_body.strip(),
                         *appendices, references_marker+references.strip()])+'\n'
(paper/'manuscript.md').write_text(content,encoding='utf-8',newline='\n')
pandoc = shutil.which('pandoc') or r'C:\Users\theri\AppData\Local\Pandoc\pandoc.exe'
subprocess.run([pandoc,str(paper/'manuscript.md'),'-f','markdown+tex_math_dollars+raw_tex+autolink_bare_uris',
                '-t','latex','-o',str(paper/'latex/body.tex')],check=True)
body = (paper/'latex/body.tex').read_text(encoding='utf-8').replace('../figures/','images/')
body = re.sub(r'\\texttt\{([^{}]*)\}',
              lambda m:r'\nolinkurl{'+m[1].replace(r'\_','_')+'}',body)
# The concordance has short ID/status cells and longer location/description cells.
table_header = re.search(r'(\\begin\{longtable\}\[\]\{@\{\}\n)(.*?)(@\{\}\}\n\\toprule)',
                         body, flags=re.S)
if concordance and table_header:
    widths = iter(('0.0500', '0.2200', '0.2800', '0.1100', '0.3400'))
    columns = re.sub(r'\\real\{0\.2000\}', lambda match: r'\real{'+next(widths)+'}',
                     table_header[2])
    body = body[:table_header.start(2)]+columns+body[table_header.end(2):]
body = re.sub(r'^(\\subsection\{[56]\. )', r'\\FloatBarrier\n\1', body, flags=re.M)
reference_heading = r'\subsection{References}\label{references}'
if body.count(reference_heading) != 1:
    raise ValueError('Expected exactly one LaTeX References heading')
before_references, reference_body = body.split(reference_heading, 1)
reference_paragraphs = [paragraph for paragraph in reference_body.strip().split('\n\n')
                        if paragraph.strip()]
reference_body = '\n\n'.join(r'\begin{samepage}'+'\n'+paragraph+'\n'+r'\end{samepage}'
                              for paragraph in reference_paragraphs)
body = (before_references+reference_heading+'\n\n'+r'\begingroup\small'+'\n'
        +reference_body+'\n'+r'\endgroup'+'\n')
(paper/'latex/body.tex').write_text(body,encoding='utf-8',newline='\n')
(paper/'latex/images').mkdir(exist_ok=True)
for f in (ROOT/'figures').glob('*.png'):
    shutil.copy2(f,paper/'latex/images'/f.name)
print({'words_regex':len(re.findall(r'\b[\w-]+\b',content)), 'characters':len(content),
       'journal_concordance_included':bool(concordance),
       'appendices_included':len(appendices)})
