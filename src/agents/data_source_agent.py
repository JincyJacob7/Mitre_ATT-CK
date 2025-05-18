def identify_log_source(description, provided_source):
    if "Windows" in provided_source:
        return "Windows Event Log"
    if "sysmon" in description.lower():
        return "Sysmon"
    return provided_source or "Unknown"
