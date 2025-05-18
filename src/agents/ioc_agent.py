def extract_iocs_from_text(text):
    import re
    ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text)
    executables = re.findall(r'\b\w+\.exe\b', text)
    return list(set(ips + executables))
