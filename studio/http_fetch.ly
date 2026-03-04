importpy requests

def fetch(str url): {
    var r = requests.get(url)
    print "Status: " + str(r.status_code)
    
    arr text_chars = arr(r.text)
    print "Content length: " + str(text_chars.len())

    # Also show first 200 characters of content
    # print "First 200 chars: " + r.text[:200] + "..."
    
    rex title_pattern = regex("/<title>(.*?)<.title>/")
    var title_match = title_pattern.search(r.text)
    if title_match != None
        print "Title: " + title_match.group(1)
    end

    rex link_pattern = regex("/<a[^>]+href=[\"']([^\"']+)[\"'][^>]*>([^<]+)<\/a>/")
    var links = link_pattern.findall(r.text)
    
    arr link_array = arr(links)
    print "Found " + str(link_array.len()) + " links:"
    var link
    given link in links:
        print "  " + link[1] + " -> " + link[0]
    done
}

def main() {
    fetch("https://miranova.studio")
}