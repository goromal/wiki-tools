# Wiki-Tools

## Commands

```bash
Usage: wiki-tools [OPTIONS] COMMAND [ARGS]...

  Read and edit DokuWiki instance pages.

Options:
  --url TEXT                URL of the DokuWiki instance (https).  [default:
                            https://notes.andrewtorgesen.com]
  --secrets-file PATH       Path to the DokuWiki login secrets JSON file.
                            [default: /data/andrew/secrets/wiki/secrets.json]
  --enable-logging BOOLEAN  Whether to enable logging.  [default: False]
  --help                    Show this message and exit.

Commands:
  get       Read the content of a DokuWiki page.
  put       Put content onto a DokuWiki page.
  put-file  Put content from a file onto a DokuWiki page.
```

### Get

```bash
Usage: wiki-tools get [OPTIONS]

  Read the content of a DokuWiki page.

Options:
  --page-id TEXT  ID of the DokuWiki page.  [required]
  --help          Show this message and exit.
```

### Put

```bash
Usage: wiki-tools put [OPTIONS]

  Put content onto a DokuWiki page.

Options:
  --page-id TEXT  ID of the DokuWiki page.  [required]
  --content TEXT  Content to put on the page.  [required]
  --help          Show this message and exit.
```

### Put File

```bash
Usage: wiki-tools put-file [OPTIONS]

  Put content from a file onto a DokuWiki page.

Options:
  --page-id TEXT  ID of the DokuWiki page.  [required]
  --file PATH     File containing the target content.  [required]
  --help          Show this message and exit.
```

## Roadmap

- Basic authenticated get/put for a page ID from strings and files [X]
- Conversion functions and CLI to and from markdown [ ]
- Conversion functions and CLI to and from html [ ]
- More advanced error catching and diagnostic messaging [ ]
