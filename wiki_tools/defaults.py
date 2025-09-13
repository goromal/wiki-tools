import os

class WikiToolsDefaults:
    WIKI_URL = "https://notes.andrewtorgesen.com"
    WIKI_USER = "None"
    WIKI_PASS = "None"
    ENABLE_LOGGING = False

    @staticmethod
    def getKwargsOrDefault(argname, **kwargs):
        argname_mapping = {
            "wiki_url": WikiToolsDefaults.WIKI_URL,
            "wiki_user": WikiToolsDefaults.WIKI_USER,
            "wiki_pass": WikiToolsDefaults.WIKI_PASS,
            "enable_logging": WikiToolsDefaults.ENABLE_LOGGING,
        }
        return kwargs[argname] if (argname in kwargs and kwargs[argname] is not None) else argname_mapping[argname]
