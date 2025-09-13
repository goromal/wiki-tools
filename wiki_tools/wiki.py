import dokuwiki
import json
import logging
import sys
import os

from wiki_tools.defaults import WikiToolsDefaults as WTD
from wiki_tools.conversions import dokuToList

class WikiTools(object):
    def _check_valid_interface(func):
        def wrapper(self, *args, **kwargs):
            if self.wiki is None:
                raise Exception("Wiki interface not initialized properly; check your secrets")
            return func(self, *args, **kwargs)
        return wrapper

    def __init__(self, **kwargs):
        self.wiki_url = WTD.getKwargsOrDefault("wiki_url", **kwargs)
        self.wiki_user = WTD.getKwargsOrDefault("wiki_user", **kwargs)
        self.wiki_pass = WTD.getKwargsOrDefault("wiki_pass", **kwargs)
        self.enable_logging = WTD.getKwargsOrDefault("enable_logging", **kwargs)
        self.wiki = None

        if self.enable_logging:
            logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
        
        try:
            self.wiki = dokuwiki.DokuWiki(self.wiki_url, self.wiki_user, self.wiki_pass, cookieAuth=True)
        except:
            pass

    @_check_valid_interface
    def getPage(self, id, as_list=False):
        if self.wiki is None:
            raise Exception("Wiki interface not initialized properly; check your secrets")
        if self.enable_logging:
            logging.info(f"[WIKI-TOOLS] Getting page {id}")
        return self.wiki.pages.get(id) if not as_list else dokuToList(self.wiki.pages.get(id))

    @_check_valid_interface
    def putPage(self, id, content):
        if self.wiki is None:
            raise Exception("Wiki interface not initialized properly; check your secrets")
        if self.enable_logging:
            logging.info(f"[WIKI-TOOLS] Editing page {id}")
        self.wiki.pages.set(id, content)
