from __future__ import annotations
from fileinput import FileInput

import logging
import re
from bs4 import BeautifulSoup
from subprocess import check_output
from dataclasses import dataclass
from pathlib import Path
from markdown import Markdown as Md
from typing import Optional


@dataclass
class Repository:
  user: str
  path: Path
  glob: str
  embed_path: str
  stem: bool

  @property
  def url(self) -> str:
    return f"https://github.com/{self.user}/{self.path.name}"

  def include_file(self):
    for markdown in File.files(self):
      line2txt = {}
      logging.info("Markdown: %s", markdown.path)
      for embed in Embed.embeds(markdown):
        logging.info("Embed: %s", embed.name)
        line2txt[embed.line] = embed.to_markdown()
      with FileInput(markdown.path, inplace=True) as file:
        for i, line in enumerate(file, 1):
          if i in line2txt:
            print(line2txt[i], end="")
          else:
            print(line, end="")


@dataclass
class Image:
  file: File
  path: Path
  RE = r"]\((.*images/.*.png)\)"

  @classmethod
  def images(cls, file) -> list[Image]:
    ret = []
    for full_img in re.findall(Image.RE, file.path.read_text()):
      name = full_img.split("/")[-1]
      ret.append(cls(file, file.path / "images" / name))
    return ret


@dataclass
class Gitbook(Repository):
  deploy_branch: str
  home: bool
  url_path: str
  summary: Optional[Markdown] = None
  toc: Optional[File] = None

  def __post_init__(self):
    logging.debug("__post_init__(%s)", self)
    if self.url_path == "":
      self.url_path = f"https://{self.user}.gitbook.io/{self.path.name}"

  def table_of_contents(self) -> str:
    assert self.summary, "Doesn't have SUMMARY.md"

    logging.debug("generate_table_of_contents(%s)", self)

    lines = ["# Table of Contents"]
    prev_dir = ""
    for markdown in self.summary.extract_summary():
      dir_name = markdown.path.parent.name
      if prev_dir != dir_name:
        prev_dir = dir_name
        lines.append(f"\n## {dir_name}")
      lines.append(f"\n### {markdown.path.relative_to(markdown.path.parent).name}\n")
      lines.append(markdown.table_of_contents(self.url_path))

    return "\n".join(lines) + "\n"

  def organize_embeds_images(self) -> None:
    logging.debug("organize_embeds_images(%s)", self)
    assert self.home
    files, path2embeds = [], {}

    for repo in Gitbook.gitbooks(self):
      for file in File.files(repo):
        files.append(file)
    logging.info("total files %s", len(files))

    for file in files:
      for image in Image.images(file):
        path2embeds[image.path] = image
      for embed in Embed.embeds(file):
        path2embeds[embed.path] = embed

    logging.info("actual embeds %s", len(path2embeds))
    cnt = 0
    for file in files:
      for actual_path in [*file.path.glob("**/images/*"), *file.embed_path.glob("*")]:
        if actual_path not in path2embeds:
          continue
        correct_path = path2embeds[actual_path].path
        if correct_path != actual_path:
          actual_path.rename(correct_path)
          cnt += 1
          logging.info("Fixed %s -> %s", actual_path, correct_path)
    logging.info(f"{cnt} wrong image link has been fixed")

  @classmethod
  def gitbooks(cls, home: Gitbook) -> list[Gitbook]:
    assert home.home
    res = []
    for path in home.path.glob("[private][public]*/*"):
      book = Gitbook(home.user, path, home.glob, home.embed_path, home.stem, home.deploy_branch, False, home.url_path)
      book.summary = Markdown(book, path / 'SUMMARY.md')
      res.append(book)
    return res


@dataclass
class File:
  repo: Repository
  path: Path
  content: str = ""

  def __post_init__(self):
    logging.debug("__post_init__(%s)", self)
    if self.content == "":
      self.content = self.path.read_text()

  @property
  def embed_path(self) -> Path:
    if self.repo.stem:
      embed_path = self.path.parent / self.path.stem
    else:
      embed_path = self.repo.path / self.repo.embed_path
    if not embed_path.is_dir():
      embed_path.mkdir()
    return embed_path

  @classmethod
  def files(cls, repo: Repository) -> list[File]:
    if isinstance(repo, Gitbook):
      assert repo.summary
      return [Markdown(repo, repo.path / path) for path in re.findall(Markdown.RE, repo.summary.content)]
    else:
      return [File(repo, file) for file in repo.path.glob(repo.glob)]


class Markdown(File):
  RE = r"\((.*\.md)\)"  # * [Module](cpp/module.md) -> cpp/module.md

  def extract_summary(self) -> list[Markdown]:
    assert self.path.name == "SUMMARY.md"
    logging.debug("extract_summary()")
    return [Markdown(self.repo, self.repo.path / path) for path in re.findall(Markdown.RE, self.content)]

  @staticmethod
  def normalize(st):
    return st.lower().replace(' ', '-')

  def extract_heading(self) -> list[tuple[int, str]]:
    logging.debug("extract_markdown()")
    text = Md(extensions=['fenced_code']).convert(self.content)
    md = BeautifulSoup(text, "html.parser")
    return [(int(str(line)[2]), str(line)[4:-5]) for line in md.find_all(re.compile('^h[1-6]$'))]

  def table_of_contents(self, url_path) -> str:
    logging.debug("table_of_contents(%s, %s)", self, url_path)
    lines = []
    for level, name in self.extract_heading():
      path = str(self.path.relative_to(self.repo.path)).replace(".md", "")
      lines.append(f"{'  ' * (level - 1)}* [{name}]({url_path}/{path}#{Markdown.normalize(name)})")
    return "\n".join(lines)


@dataclass
class Embed:
  file: File
  name: str
  line: int
  glob: str = "**/*"

  @property
  def path(self) -> Path:
    return self.file.embed_path.parent / self.file.embed_path.stem / self.name

  @classmethod
  def embeds(cls, file: File) -> list[Embed]:
    embeds = []
    for line, txt in enumerate(file.path.read_text().split("\n"), 1):
      for cls_ in [Repo, Link, Include]:
        match = re.match(cls_.RE(cls_), txt)
        if match:
          name, glob = match.group(1), "**/*"
          if "|" in name:
            name, glob = name.split("|", 1)
            name, glob = name.strip(" '\""), glob.strip(" '\"")
          embeds.append(cls_(file, name, line, glob))
    return embeds

  @staticmethod
  def RE(cls) -> str:
    raise NotImplementedError

  def to_markdown(self):
    raise NotImplementedError

  def update_link(self, text: str) -> str:
    logging.debug("update_link(%s)", text)
    prefix = self.file.embed_path.relative_to(self.file.repo.path)
    text = re.sub(r"(!\[.*\])\((.*)\)", rf'\1({prefix}/\2)', text.strip())

    return "".join(ch for i, ch in enumerate(text) if i <= 1 or not (text[i - 1] == text[i - 2] == ch == "\n")) + "\n"


@dataclass
class Repo(Embed):
  REPO = "repo"

  @staticmethod
  def RE(cls) -> str:
    return fr'{{% {cls.REPO} [\'"](.*)[\'"] %}}'

  def to_markdown(self):
    logging.debug("_repo_to_markdown(%s)", self.path)
    assert self.path.is_dir(), f"{self.path} is not a directory"
    lines = []
    ignored = [".gitignore"] + check_output("git ls-files --other", text=True, shell=True).splitlines()
    for file_glob in self.glob.split("|"):
      lines += ["{% tabs %}"]
      for file in self.path.glob(file_glob):
        if file.is_file() and file not in ignored:
          lines += [f"{{% tab title=\'{file.relative_to(self.path)}\' %}}\n"]
          suffix = file.suffix[1:]
          lines += [f"````{suffix if suffix else 'txt'}"]
          try:
            lines += [file.read_text()]
          except UnicodeDecodeError:
            raise Exception("Please do not include binary files")
          lines += ["````\n"]
          lines += ["{% endtab %}"]
      lines += ["{% endtabs %}\n"]
    return self.update_link("\n".join(lines))


@dataclass
class Link(Embed):
  LINK = "link"

  @staticmethod
  def RE(cls) -> str:
    return fr'{{% {cls.LINK} [\'"](.*)[\'"] %}}'

  def to_markdown(self):
    logging.debug("_link_to_markdown(%s)", self.path)
    repo = self.file.repo
    assert self.path.is_file(), f"{self.path} is not a file"
    return f"[{self.path.name}]({repo.url}/tree/{repo.deploy_branch}/{self.path.relative_to(repo.path)})\n"


@dataclass
class Include(Embed):
  INCLUDE = "include"

  @staticmethod
  def RE(cls) -> str:
    return fr'{{% {cls.INCLUDE} [\'"](.*)[\'"] %}}'

  def to_markdown(self):
    logging.debug("_include_to_markdown(%s)", self)
    assert self.path.is_file(), f"{self.path} is not a file"
    return self.update_link(self.path.read_text())
