importpy requests

def fetch(str url): {
    var r = requests.get(url)
    print "Status: " + str(r.status_code)
    print "Content length: " + str(len(r.text))

    # Also show first 200 characters of content
    print "First 200 chars: " + r.text[:200] + "..."
    
    rex title_pattern = r"<title>(.*?)<.title>"

    print title_pattern.group(1)
    

    rex link_pattern = regex("<a[^>]+href=["']([^"']+)["'][^>]*>([^<]+)<\/a>/")
    var links = link_pattern.findall(r.text)

    print "Found " + str(len(links)) + " links:"
    given link in links:
        print "  " + link[1] + " -> " + link[0]
    done
}

fetch("https://miranova.studio")

