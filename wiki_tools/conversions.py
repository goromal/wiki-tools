import re

def applyConversions(original, rules):
    final = original
    for rule in rules:
        final = re.sub(rule[0], rule[1], final, flags=re.M)
    return final

def dokuToMarkdown(doku):
    rules = [
        (r"======\s+([^=]+)\s+======", r"# \1"),
        (r"=====\s+([^=]+)\s+=====", r"## \1"),
        (r"====\s+([^=]+)\s+====", r"### \1"),
        (r"===\s+([^=]+)\s+===", r"#### \1"),
        (r"//([^/]+)//", r"*\1*"),
        (r"\[\[(.+)\|(.*)\]\]", r"[\2](\1)"),
    ]
    return applyConversions(doku, rules)

def markdownToDoku(markdown):
    rules = [
        (r"####\s+(.+)", r"=== \1 ==="),
        (r"###\s+(.+)", r"==== \1 ===="),
        (r"##\s+(.+)", r"===== \1 ====="),
        (r"#\s+(.+)", r"====== \1 ======"),
        (r"([^\*])\*([^\*]+)\*([^\*])", r"\1//\2//\3"),    
        (r"\[(.+)\]\((.+)\)", r"[[\2|\1]]"),
    ]
    return applyConversions(markdown, rules)
