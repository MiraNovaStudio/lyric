importpy http.server; HTTPServer, SimpleHTTPRequestHandler

def main() {
    tup addr = ("0.0.0.0", 8080)
    var server = HTTPServer(addr, SimpleHTTPRequestHandler)
    print("Server created on port 8080")
    #server.serve_forever()

}
