import argparse
import logging
from pathlib import Path

from include_file.models import File, Gitbook, Include, Link, Markdown, Repo, Repository


def get_parser():
  parser = argparse.ArgumentParser()
  parser.add_argument('-l', '--log_level', type=int, default=20)
  parser.add_argument('-u', '--user', type=str, required=True)

  # Flags
  parser.add_argument('-g', '--glob', type=str, default="**/*")
  parser.add_argument('-p', '--path', type=Path, default=Path("."))
  parser.add_argument('-s', '--stem', action='store_true')
  parser.add_argument('-v', '--validate', action='store_true')
  parser.add_argument('-e', '--embed_path', type=str, default=".include_file")

  # Gitbook Flags
  parser.add_argument('-y', '--summary_path', default="")
  parser.add_argument('-d', '--deploy_branch', default="deploy")
  parser.add_argument('-t', '--toc', default="")
  parser.add_argument('-url', '--url_path', type=str, default="")
  parser.add_argument('--home', action='store_true')

  # Custom Flags
  parser.add_argument('--include', default='include')
  parser.add_argument('--link', default='link')
  parser.add_argument('--repo', default="repo")

  return parser.parse_args()


if __name__ == "__main__":
  ag = get_parser()
  logging.basicConfig(format='%(asctime)s %(levelname)-6s [%(filename)s:%(lineno)d] %(message)s',
                      datefmt='%m%d:%H%M%S')
  logging.getLogger().setLevel(ag.log_level)

  Include.INCLUDE, Link.LINK, Repo.REPO = ag.include, ag.link, ag.repo

  if ag.summary_path:
    book = Gitbook(ag.user, ag.path.resolve(), ag.glob, ag.embed_path, ag.stem, ag.deploy_branch, ag.home, ag.url_path)
    book.summary = Markdown(book, book.path / ag.summary_path)
    if ag.toc:
      book.toc = File(book, book.path / ag.toc)
      table_of_contents = book.table_of_contents()
      book.toc.path.write_text(table_of_contents)
    if ag.toc and book.home:
      book.organize_embeds_images()
    book.include_file()
  else:
    repo = Repository(ag.user, ag.path, ag.glob, ag.embed_path, ag.stem)
    repo.include_file()
