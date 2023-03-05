import click
import dokuwiki
import json
import logging
import sys
import time

from wiki_tools.defaults import WikiToolsDefaults as WTD

class WikiTools(object):
    def __init__(self, **kwargs):
        self.wiki_url = WTD.getKwargsOrDefault("wiki_url", **kwargs)
        self.wiki_secrets_file = WTD.getKwargsOrDefault("wiki_secrets_file", **kwargs)
        self.enable_logging = WTD.getKwargsOrDefault("enable_logging", **kwargs)

        if self.enable_logging:
            logging.basicConfig(filename="LOG-wiki-tools%s.log" % time.strftime("%Y%m%d-%H%M%S"), level=logging.INFO)
            logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
        
        with open(self.wiki_secrets_file, "r") as secrets_file:
            secrets = json.loads(secrets_file.read())
        
        self.wiki = dokuwiki.DokuWiki(self.wiki_url, secrets["user"], secrets["pass"], cookieAuth=True)

    def getPage(self, id):
        if self.enable_logging:
            logging.info(f"[WIKI-TOOLS] Getting page {id}")
        return self.wiki.pages.get(id)
    
    def putPage(self, id, content):
        if self.enable_logging:
            logging.info(f"[WIKI-TOOLS] Editing page {id}")
        self.wiki.pages.set(id, content)

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
    type=click.Path(exists=True),
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
def get(ctx: click.Context, page_id):
    """Read the content of a DokuWiki page."""
    print(ctx.obj.getPage(id=page_id))

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
    "--content",
    "content",
    type=str,
    required=True,
    help="Content to put on the page.",
)
def put(ctx: click.Context, page_id, content):
    """Put content onto a DokuWiki page."""
    ctx.obj.putPage(id=page_id, content=content)

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
    required=True,
    help="File containing the target content.",
)
def put_file(ctx: click.Context, page_id, content_file):
    """Put content from a file onto a DokuWiki page."""
    with open(content_file, "r") as infile:
        ctx.obj.putPage(id=page_id, content=infile.read())

def main():
    cli()

if __name__ == "__main__":
    main()