importpy requests

def fetch(str url): {
    var r = requests.get(url)
    print "Status: " + str(r.status_code)
    print "Content length: " + str(len(r.text))

    # Extract title using rex datatype
    rex title_pattern = /<title>(.*?)<\/title>/

    var title_match = title_pattern.search(r.text)
    
    if title_match:
        print "Page title: " + title_match.group(1)
    else:
        print "No title found in HTML"
    
    # Also show first 200 characters of content
    print "First 200 chars: " + r.text[:200] + "..."
    
}

fetch("https://miranova.studio")

