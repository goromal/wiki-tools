import dokuwiki
import json
import logging
import sys

from wiki_tools.defaults import WikiToolsDefaults as WTD

class WikiTools(object):
    def __init__(self, **kwargs):
        self.wiki_url = WTD.getKwargsOrDefault("wiki_url", **kwargs)
        self.wiki_secrets_file = WTD.getKwargsOrDefault("wiki_secrets_file", **kwargs)
        self.enable_logging = WTD.getKwargsOrDefault("enable_logging", **kwargs)

        if self.enable_logging:
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
