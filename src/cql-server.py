import socket
from BaseHTTPServer import  HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import time,json, sys , subprocess as sp
from cassandra_result_parser import parseCassandraOutput

hostName = ""
hostPort = 3434

class MyServer(SimpleHTTPRequestHandler):

#   GET is for clients geting the predi
    def do_GET(self):
        return SimpleHTTPRequestHandler.do_GET(self)

    #POST is for submitting data.
    def do_POST(self):
        if("/getDBQuery" in self.path):
            self.getPostData()
            self.send_response(200)
            self.end_headers()
            response= self.dbQuery()
            self.wfile.write(json.dumps(response))

    def dbQuery(self):
        if(not self.request["query"].strip() == ""):
            pipe = sp.Popen( 'cqlsh -e "%s"' % self.request["query"] , shell=True, stdout=sp.PIPE, stderr=sp.PIPE )
            res = pipe.communicate()
            results = parseCassandraOutput(res[0])
            results.update({"errors": res[1]})
        else:
            results = {"errors":"Query should not be empty","message":""}
        results.update({"query": self.request["query"]})
        return results
        
        
    def getPostData(self):
        content_length = int(self.headers['Content-Length']) 
        post_data = self.rfile.read(content_length) 
        self.request = json.loads(post_data)
    

if(len(sys.argv)> 1 and sys.argv[1] is int):
    hostPort = sys.argv[1] 
myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
