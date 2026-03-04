rex title_pattern = regex("/<title>(.*?)<\/title>/")

def main() {
    str html = "<html><head><title>My Page</title></head></html>"
    var match = title_pattern.search(html)

    if match
        print("Title:", match.group(1))
    else
        print("No title found")
    end
}
