import click
import os
import random
from datetime import datetime

from wiki_tools.defaults import WikiToolsDefaults as WTD
from wiki_tools.conversions import dokuToMarkdown, markdownToDoku
from wiki_tools.wiki import WikiTools

class NotRequiredIf(click.Option):
    def __init__(self, *args, **kwargs):
        self.not_required_if = kwargs.pop('not_required_if')
        assert self.not_required_if, "'not_required_if' parameter required"
        kwargs['help'] = (kwargs.get('help', '') +
            ' NOTE: This argument is mutually exclusive with %s' %
            self.not_required_if
        ).strip()
        super(NotRequiredIf, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        we_are_present = self.name in opts
        other_present = self.not_required_if in opts

        if other_present:
            if we_are_present:
                raise click.UsageError(
                    "Illegal usage: `%s` is mutually exclusive with `%s`" % (
                        self.name, self.not_required_if))
            else:
                self.prompt = None

        return super(NotRequiredIf, self).handle_parse_result(
            ctx, opts, args)

def put_impl(ctx, page_id, content_file, content):
    if content_file is not None:
        with open(content_file, "r") as infile:
            content = infile.read()
    ctx.obj.putPage(id=page_id, content=content)

def put_md_impl(ctx, page_id, content_file, content):
    if content_file is not None:
        with open(content_file, "r") as infile:
            content = infile.read()
    ctx.obj.putPage(id=page_id, content=markdownToDoku(content))

@click.group()
@click.pass_context
@click.option(
    "--url",
    "wiki_url",
    type=str,
    default=WTD.WIKI_URL,
    show_default=True,
    help="URL of the DokuWiki instance (https).",
)
@click.option(
    "--secrets-file",
    "secrets_file",
    type=click.Path(),
    default=WTD.WIKI_SECRETS_FILE,
    show_default=True,
    help="Path to the DokuWiki login secrets JSON file.",
)
@click.option(
    "--enable-logging",
    "enable_logging",
    type=bool,
    default=WTD.ENABLE_LOGGING,
    show_default=True,
    help="Whether to enable logging.",
)
def cli(ctx: click.Context, wiki_url, secrets_file, enable_logging):
    """Read and edit DokuWiki instance pages."""
    ctx.obj = WikiTools(wiki_url=wiki_url, wiki_secrets_file=secrets_file, enable_logging=enable_logging)

@cli.command()
@click.pass_context
@click.option(
    "--page-id",
    "page_id",
    type=str,
    required=True,
    help="ID of the DokuWiki page.",
)
@click.option(
    "--output",
    "output",
    type=str,
    default="",
    show_default=True,
    help="Output text file name. Will print to terminal if not specified.",
)
def get(ctx: click.Context, page_id, output):
    """Read the content of a DokuWiki page."""
    doku = ctx.obj.getPage(id=page_id)
    if output != "":
        with open(output, "w") as outfile:
            outfile.write(doku)
    else:
        print(doku)

@cli.command()
@click.pass_context
@click.option(
    "--page-id",
    "page_id",
    type=str,
    required=True,
    help="ID of the DokuWiki page.",
)
@click.option(
    "--output",
    "output",
    type=str,
    default="",
    show_default=True,
    help="Output Markdown file name. Will print to terminal if not specified.",
)
def get_md(ctx: click.Context, page_id, output):
    """Read the content of a DokuWiki page in Markdown format."""
    doku = ctx.obj.getPage(id=page_id)
    if output != "":
        with open(output, "w") as outfile:
            outfile.write(dokuToMarkdown(doku))
    else:
        print(dokuToMarkdown(doku))

@cli.command()
@click.pass_context
@click.option(
    "--page-id",
    "page_id",
    type=str,
    required=True,
    help="ID of the DokuWiki page.",
)
@click.option(
    "--file",
    "content_file",
    type=click.Path(exists=True),
    required=False,
    help="File containing the target content.",
)
@click.option(
    "--content",
    "content",
    type=str,
    cls=NotRequiredIf,
    not_required_if="content_file",
    help="Content to put on the page if file is not specified.",
)
def put(ctx: click.Context, page_id, content_file, content):
    """Put content onto a DokuWiki page."""
    put_impl(ctx, page_id, content_file, content)

@cli.command()
@click.pass_context
@click.option(
    "--page-id",
    "page_id",
    type=str,
    required=True,
    help="ID of the DokuWiki page.",
)
@click.option(
    "--file",
    "content_file",
    type=click.Path(exists=True),
    required=False,
    help="Markdown file containing the target content.",
)
@click.option(
    "--content",
    "content",
    type=str,
    cls=NotRequiredIf,
    not_required_if="content_file",
    help="Markdown content to put on the page if file is not specified.",
)
def put_md(ctx: click.Context, page_id, content_file, content):
    """Put Markdown content onto a DokuWiki page."""
    put_md_impl(ctx, page_id, content_file, content)

@cli.command()
@click.pass_context
@click.option(
    "--pages-dir",
    "pages_dir",
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
    required=True,
    help="Directory with .txt pages to upload."
)
@click.option(
    "--namespace",
    "namespace",
    type=str,
    required=True,
    help="Namespace to upload the pages to."
)
def put_dir(ctx: click.Context, pages_dir, namespace):
    """Put a directory of pages into a DokuWiki namespace."""
    for file in os.listdir(pages_dir):
        if file.endswith(".txt"):
            page_id = (f"{namespace}:" if namespace else "") + file[:-4]
            put_impl(ctx, page_id, os.path.join(pages_dir, file), None)

@cli.command()
@click.pass_context
@click.option(
    "--pages-dir",
    "pages_dir",
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
    required=True,
    help="Directory with .txt pages to upload."
)
@click.option(
    "--namespace",
    "namespace",
    type=str,
    required=True,
    help="Namespace to upload the pages to."
)
def put_md_dir(ctx: click.Context, pages_dir, namespace):
    """Put a directory of Markdown pages into a DokuWiki namespace."""
    for file in os.listdir(pages_dir):
        if file.endswith(".md"):
            page_id = (f"{namespace}:" if namespace else "") + file[:-3]
            put_md_impl(ctx, page_id, os.path.join(pages_dir, file), None)

@cli.command()
@click.pass_context
@click.option(
    "--namespace",
    "namespace",
    type=str,
    default="journals",
    show_default=True,
    help="Journal pages namespace."
)
@click.option(
    "--output",
    "output",
    type=str,
    default="",
    show_default=True,
    help="Output text file name. Will print to terminal if not specified.",
)
def get_rand_journal(ctx: click.Context, namespace, output):
    """Get a random journal entry between 2013 and now."""
    page_id = f"{namespace}:{random.choice([y for y in range(2013, datetime.now().year+1)])}"
    entries = ctx.obj.getPage(id=page_id, as_list=True)
    random_entry = random.choice(entries)
    formatted_entry = f"""{random_entry[0]}

{random_entry[1]}
"""
    if output != "":
        with open(output, "w") as outfile:
            outfile.write(formatted_entry)
    else:
        print(formatted_entry)

def main():
    cli()

if __name__ == "__main__":
    main()
