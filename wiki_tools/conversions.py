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

def dokuToList(doku):
    entries = []
    current1 = None
    current2 = None
    current3 = None
    current4 = None
    def concat_currents(c1, c2, c3, c4):
        cc = ""
        if c1 is not None:
            cc = c1
        if c2 is not None:
            cc += f"/{c2}"
        if c3 is not None:
            cc += f"/{c3}"
        if c4 is not None:
            cc += f"/{c4}"
        return cc
    current_entry = []
    for line in doku.split("\n"):
        if line:
            match1 = re.search(r"======\s+([^=]+)\s+======", line)
            if match1:
                if len(current_entry) > 0:
                    entries.append((concat_currents(current1, current2, current3, current4), "\n\n".join(current_entry)))
                    current_entry.clear()
                current1 = match1.group(1)
                current2 = None
                current3 = None
                current4 = None
                continue
            match2 = re.search(r"=====\s+([^=]+)\s+=====", line)
            if match2:
                if len(current_entry) > 0:
                    entries.append((concat_currents(current1, current2, current3, current4), "\n\n".join(current_entry)))
                    current_entry.clear()
                current2 = match2.group(1)
                current3 = None
                current4 = None
                continue
            match3 = re.search(r"====\s+([^=]+)\s+====", line)
            if match3:
                if len(current_entry) > 0:
                    entries.append((concat_currents(current1, current2, current3, current4), "\n\n".join(current_entry)))
                    current_entry.clear()
                current3 = match3.group(1)
                current4 = None
                continue
            match4 = re.search(r"===\s+([^=]+)\s+===", line)
            if match4:
                if len(current_entry) > 0:
                    entries.append((concat_currents(current1, current2, current3, current4), "\n\n".join(current_entry)))
                    current_entry.clear()
                current4 = match4.group(1)
                continue
            current_entry.append(line)
    return entries

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
