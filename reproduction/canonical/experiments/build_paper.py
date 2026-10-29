"""Assemble manuscript and LaTeX body; compilation is a separate checked step."""
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
paper = ROOT/'paper'
resource = (paper/'resource-discussion.md').read_text(encoding='utf-8')
resource = resource.replace('# Resource implications and the scope of the numerical evidence',
                            '## 6. Discussion: resources and numerical evidence')
resource = re.sub(r'^## ', '### ', resource, flags=re.M).replace('### 6. Discussion:', '## 6. Discussion:')
content = (paper/'core.md').read_text(encoding='utf-8')+'\n'+resource+'\n'+(paper/'closing.md').read_text(encoding='utf-8')
(paper/'manuscript.md').write_text(content,encoding='utf-8',newline='\n')
pandoc = shutil.which('pandoc') or r'C:\Users\theri\AppData\Local\Pandoc\pandoc.exe'
subprocess.run([pandoc,str(paper/'manuscript.md'),'-f','markdown+tex_math_dollars+raw_tex',
                '-t','latex','-o',str(paper/'latex/body.tex')],check=True)
body = (paper/'latex/body.tex').read_text(encoding='utf-8').replace('../figures/','images/')
body = re.sub(r'\\texttt\{([^{}]*)\}',
              lambda m:r'\nolinkurl{'+m[1].replace(r'\_','_')+'}',body)
(paper/'latex/body.tex').write_text(body,encoding='utf-8',newline='\n')
(paper/'latex/images').mkdir(exist_ok=True)
for f in (ROOT/'figures').glob('*.png'):
    shutil.copy2(f,paper/'latex/images'/f.name)
print({'words_regex':len(re.findall(r'\b[\w-]+\b',content)), 'characters':len(content)})
