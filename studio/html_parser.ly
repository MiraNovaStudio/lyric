# html_parser.ly - Advanced HTML parsing with rex datatype

importpy requests

def parse_html(str url): {
    print "Fetching: " + url
    var r = requests.get(url)
    print "Status: " + str(r.status_code)
    
    if r.status_code != 200:
        print "Failed to fetch page"
        return
    
    # Extract title
    rex title_pattern = /<title>(.*?)<\/title>/
    var title_match = title_pattern.search(r.text)
    
    if title_match:
        print "Page title: " + title_match.group(1)
    else:
        print "No title found"
    
    # Extract all links
    rex link_pattern = /<a[^>]+href=["']([^"']+)["'][^>]*>([^<]+)<\/a>/
    var links = link_pattern.findall(r.text)
    
    print "Found " + str(len(links)) + " links:"
    for link in links:
        print "  " + link[1] + " -> " + link[0]
    
    # Extract meta description
    rex meta_pattern = /<meta[^>]+name=["']description["'][^>]+content=["']([^"']+)["'][^>]*>/
    var meta_match = meta_pattern.search(r.text)
    
    if meta_match:
        print "Meta description: " + meta_match.group(1)
    else:
        print "No meta description found"
    
    # Extract all headings
    rex heading_pattern = /<h([1-6])[^>]*>([^<]+)<\/h[1-6]>/
    var headings = heading_pattern.findall(r.text)
    
    print "Found " + str(len(headings)) + " headings:"
    for heading in headings:
        print "  H" + heading[0] + ": " + heading[1]
}

# Test with a few different sites
parse_html("https://miranova.studio")
print "\n" + "="*50 + "\n"
parse_html("https://httpbin.org/html")
