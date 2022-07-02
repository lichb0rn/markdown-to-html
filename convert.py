"""
    A script to convert markdown files to html using pandoc.
    The script preserves folder structure:
        original: 
            /home/user/SecondBrain/foo.md
            /home/user/SecondBrain/bar/baz.md
            /home/user/SecondBrain/qux/quux.md

        output:
            /home/user/newSecondBrainInHTML/foo.md
            /home/user/newSecondBrainInHTML/bar/baz.md
            /home/user/newSecondBrainInHTML/qux/quux.md
"""
from pathlib import Path
import subprocess

PANDOC_PATH = "/usr/local/bin/pandoc"
MARKDOWN_FOLDER = "MARKDOWN FOLDER"
HTML_OUTPUT = "HTML FOLDER"

md_path = Path(MARKDOWN_FOLDER)
html_path = Path(HTML_OUTPUT)

def walk(path: Path) -> None:
    """Recursively walk through folders"""
    for f in path.iterdir():
        print(f"At {f}")
        if f.is_dir():
            walk(f)
        else:
            if f.suffix == ".md":
                
                process(f, md_path)


def process(md_file: Path, root: Path) -> None:
    """Process the file: convert md to html and create a target folder"""
    print(f"Processing: {md_file}")
    relative_md_path = md_file.relative_to(root).parent
    target_path = create_folder(relative_md_path, html_path)
    html_file = Path.joinpath(target_path, md_file.stem + ".html")
    convert(md_file, html_file)
    

def create_folder(folder: Path, relative_root: Path) -> Path:
    """Creates subfolders with 'folder' in 'relative_root' and returns it"""
    target = Path.joinpath(relative_root, folder)
    if not target.exists():
        print(f"Creating target folder: {target}")
        target.mkdir(parents=True)
    return target
    

def convert(md_file: Path, target_path: Path) -> None:
    """Converts markdown file to html and copies it to target_path"""
    print(f"Converting file to: {target_path}")
    subprocess.run([PANDOC_PATH, md_file, '-f', 'markdown', '-t', 'html', '-s', '-o', target_path])


if __name__ == "__main__":
    walk(md_path)