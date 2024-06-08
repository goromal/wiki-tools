import os

class WikiToolsDefaults:
    WIKI_URL = "https://notes.andrewtorgesen.com"
    WIKI_SECRETS_FILE = "~/secrets/wiki/secrets.json"
    ENABLE_LOGGING = False

    @staticmethod
    def getKwargsOrDefault(argname, **kwargs):
        argname_mapping = {
            "wiki_url": WikiToolsDefaults.WIKI_URL,
            "wiki_secrets_file": WikiToolsDefaults.WIKI_SECRETS_FILE,
            "enable_logging": WikiToolsDefaults.ENABLE_LOGGING,
        }
        return kwargs[argname] if (argname in kwargs and kwargs[argname] is not None) else argname_mapping[argname]
