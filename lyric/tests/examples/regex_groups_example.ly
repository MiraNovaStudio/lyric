# Regex Group Handling Example
# This demonstrates the regex group functionality from Sprint 7 Task 2

rex title = regex("/<title>(.*?)</title>/")
var match = title.search("<title>Hello</title>")
if match:
    print match.group(1)
else:
    print "No match found"
end
