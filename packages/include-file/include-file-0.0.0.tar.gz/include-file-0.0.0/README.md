# Include File

Managing documentation is always challenging.

1. Some information ([ex] setting up git command) might comes up in multiple documentation
    * see [Include](#include), [path](#path)
1. Directly link to github url because contents are huge ([ex] jupyter, data files)
    * see [Link](#link)
1. Need entire file structure or support multi-language ([ex] python, java)
    * see [Repo](#repo) ([Note] in [Gitbook](https://gitbook.com/) syntax)

## Usage

* pip install include_file

```yml
# .github/workflows/deploy.yml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: seanhwangg/include-file
        with:
          globs: ["**/*.md", "**/*.st", "**/*.html"]
          path: "./.included-file"
          stem: False
          validate: True
          include: include
          link: link
          repo: repo
      - name: Push changes
        uses: ad-m/github-push-action@master
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          branch: deploy
          force: true
```

## Flags

### glob

Which glob files to embed
Default: ["\*\*/\*.md", "\*\*/\*.st", "\*\*/\*.html"]

### path

Where to look for embed file
Default: ./.include-file/

### stem

Use stem of markdown to overwrite path
Default: False

* Example: embeds for `REAMD.md` are stored in `README/embed.txt`

### validate

Whether to fail CI in case of embed error
Default: True

### include

Overwrite default `include`
Default: include

> Input

```md
<!-- README.md  -->

* List before embed
{% include 'embed.txt' %}
* List after embed

<!-- embed.txt  -->
* I am in embed
```

> Result

```md
<!-- README.md -->
* List before embed
* I am in embed
* List after embed
```

### link

Overwrite default `link`
Default: link

> Input

```md
<!-- README.md -->
* List before embed
{% link 'embed.txt' %}
* List after embed

<!-- embed.txt  -->
* I am in embed
```

> Result

```md
<!-- REAMD.md -->
* List before embed
\[embed.txt](https://github.com/[user]/[repository]/blob/[]/local.yml)
* List after embed
```

## Gitbook Flags

> Note: These are completely optional for [Gitbook](https://gitbook.com/) users

### repo

Overwrite default `repo`
Default: repo

> Input

```md
<!-- README.md  -->
* List before embed
{% repo 'embed' %}
* List after embed

<!-- embed/embed1.md  -->
* I am in embed1

<!-- embed/nested/embed2.md  -->
* I am in embed2
```

> Result

![Result on gitbook web](images/20210626_114700.png)

```md
<!-- README.md -->
* List before embed

{% tabs %}
{% tab title='embed1.md' %}

* I am in embed1

{% endtab %}
{% tab title='nested/embed2.md' %}

* I am in embed2

{% endtab %}
{% endtabs %}

* List after embed
```

### TOC

Create table of contents
Default: None

> Input

```md
<!-- SUMMARY.md -->
* [Cloud](cloud/cloud.md)
  * [AWS](cloud/aws.md)
  * [GCP](cloud/gcp.md)

* [Database](database/database.md)
  * [SQL](database/sql.md)
  * [SQL Tool](database/sql-tool.md)
  * [No SQL](database/nosql.md)

* [Devops](devops/devops.md)
  * [CI](devops/ci.md)
  * [Docker](devops/docker.md)
  * [Git](devops/git.md)
  * [Test](devops/test.md)
  * [Documentation](devops/documentation.md)

* [Editor](editor/others.md)
  * [Vim](editor/vim.md)
  * [VScode](editor/vscode.md)
```

> Output

```md
# Table of Contents

## A

### B.md

* [cloud](https://seanhwangg.gitbook.io/tool/cloud/cloud#cloud)
  * [service](https://seanhwangg.gitbook.io/tool/cloud/cloud#service)

### aws.md

* [aws](https://seanhwangg.gitbook.io/tool/cloud/aws#aws)
  * [ami](https://seanhwangg.gitbook.io/tool/cloud/aws#ami)
```
