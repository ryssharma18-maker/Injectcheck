import html

def make_html(results):
    bad = sum(1 for r in results if r["vulnerable"])
    errs = sum(1 for r in results if r["error"])
    rows = ""
    for r in results:
        if r["error"]:
            tag, color = "ERROR", "#b8860b"
        elif r["vulnerable"]:
            tag, color = "VULNERABLE", "#d93025"
        else:
            tag, color = "safe", "#1e8e3e"
        rows += "<tr><td style='color:" + color + ";font-weight:bold'>" + tag + "</td>"
        rows += "<td>" + html.escape(r["name"]) + "</td></tr>"
    head = "<h1>injectcheck report</h1>"
    head += "<p><b>" + str(bad) + "</b> of " + str(len(results)) + " attacks got through, "
    head += str(errs) + " errors</p>"
    style = "body{font-family:sans-serif;max-width:640px;margin:30px auto}"
    style += "td{padding:6px 14px;border-bottom:1px solid #ddd}"
    return "<html><head><meta charset='utf-8'><style>" + style + "</style></head><body>" + head + "<table>" + rows + "</table></body></html>"
