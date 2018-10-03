import socket
import sys
import traceback
import os


def response_ok(body=b"This is a minimal response", mimetype=b"text/plain"):
    """
    returns a basic HTTP response
    Ex:
        response_ok(
            b"<html><h1>Welcome:</h1></html>",
            b"text/html"
        ) ->

        b'''
        HTTP/1.1 200 OK\r\n
        Content-Type: text/html\r\n
        \r\n
        <html><h1>Welcome:</h1></html>\r\n
        '''
    """

    return b"\r\n".join([
        b"HTTP/1.1 200 OK",
        b"Content-Type: " + mimetype,
        b"",
        body,
    ])

def response_method_not_allowed():
    """Returns a 405 Method Not Allowed response"""

    return b"\r\n".join([
        b"HTTP/1.1 405 Method Not Allowed",
        b"",
        b"You can't do that on this server!",
    ])


def response_not_found():
    """Returns a 404 Not Found response"""

    # TODO: Implement response_not_found
    return b"\r\n".join([
        b"HTTP/1.1 404 Method Not Allowed",
        b"",
        b"Location or file not found!",
    ])


def parse_request(request):
    """
    Given the content of an HTTP request, returns the path of that request.

    This server only handles GET requests, so this method shall raise a
    NotImplementedError if the method of the request is not GET.
    """

    #split request into lines
    #take the first line as [0]
    #split first line on spaces
    method, path, version = request.split("\r\n")[0].split(" ")
    
    if method != "GET": #only hand get requests this exercise
        raise NotImplementedError

    return path

def response_path(path):
    print('response_path path: ', path)
    """
    This method should return appropriate content and a mime type.

    If the requested path is a directory, then the content should be a
    plain-text listing of the contents with mimetype `text/plain`.

    If the path is a file, it should return the contents of that file
    and its correct mimetype.

    If the path does not map to a real location, it should raise an
    exception that the server can catch to return a 404 response.

    Ex:
        response_path('/a_web_page.html') -> (b"<html><h1>North Carolina...",
                                            b"text/html")

        response_path('/images/sample_1.png')
                        -> (b"A12BCF...",  # contents of sample_1.png
                            b"image/png")

        response_path('/') -> (b"images/, a_web_page.html, make_type.py,...",
                             b"text/plain")

        response_path('/a_page_that_doesnt_exist.html') -> Raises a NameError

    """

    # TODO: Raise a NameError if the requested content is not present
    # under webroot.

    # TODO: Fill in the appropriate content and mime_type give the path.
    # See the assignment guidelines for help on "mapping mime-types", though
    # you might need to create a special case for handling make_time.py
    #
    # If the path is "make_time.py", then you may OPTIONALLY return the
    # result of executing `make_time.py`. But you need only return the
    # CONTENTS of `make_time.py`.
    
    if path == '/':
        #content = b'sample.txt\r\nimages'
        local_path = os.path.join('webroot', *path.split('/'))
        content = os.listdir(local_path)
        content = ','.join(content).replace(',', ' ').encode()
        mime_type = b'text/plain'
        
        return b'\r\n'.join([
                b'HTTP/1.1 200 OK',
                b'Content-Type: ' + mime_type,
                b'',
                content])
    
    elif path == '/sample.txt':
        f = open('webroot/sample.txt', 'rb')
        content = f.read()
        mime_type = b'text/plain'

        return b'\r\n'.join([
                    b'HTTP/1.1 200 OK',
                    b'Content-Type: ' + mime_type,
                    b'',
                    content])
    
    elif 'images' in path:
        
        mime_type1 = b'text/plain'
        mime_type2 = b'image/jpeg'
        mime_type3 = b'image/png'
        
        if path[7:] == '/images':
            
            #local_path = os.path.join('webroot', *path.split('/'))
            #print('local_path: ', local_path)
            content = os.listdir(path)
            print('path: ', content)
            content = ','.join(content).replace(',', ' ').encode()
            
            return b'\r\n'.join([
                b'HTTP/1.1 200 OK',
                b'Content-Type: ' + mime_type1,
                b'',
                content])
        
#        
#        print(path)
        
#        print(content)
        
#        path = path.split('\\')[2]
#        content = path.encode()
#        print('New path: ', path)

       
        
        
    
        elif path[-3:] == 'jpg':
            
            f = open(path, 'rb')            
            content = f.read()
            print('jpg path: ', content)

            return b'\r\n'.join([
                b'HTTP/1.1 200 OK',
                b'Content-Type: ' + mime_type2,
                b'',
                content])
    
        elif path[-3:] == 'png':
            
            f = open(path, 'rb')            
            content = f.read()
            print('png path: ', content)

            return b'\r\n'.join([
                b'HTTP/1.1 200 OK',
                b'Content-Type: ' + mime_type3,
                b'',
                content])
        
    
#    content = b"not implemented"
#    mime_type = b"not implemented"
#
#    return content, mime_type


def server(log_buffer=sys.stderr):
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("making a server on {0}:{1}".format(*address), file=log_buffer)
    sock.bind(address)
    sock.listen(1)

    try:
        while True:
            print('waiting for a connection', file=log_buffer)
            conn, addr = sock.accept()  # blocking
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)

                request = ''
                while True:
                    data = conn.recv(1024) #bytes
                    request += data.decode('utf8')
                    
                    if '\r\n\r\n' in request:  #full blank line
                        break

                print("Request received:\n{}\n\n".format(request))

                try:
                    path = parse_request(request)
                    print('parse_request path: ', path)
                    local_path = os.path.join('webroot', *path.split('/'))
                    
                    if path == '/':
                        response = response_path(path)
 
                    elif 'images' in path:
                        response = response_path(local_path)
                    
                    #elif os.path.exists(local_path):
                    
                    elif path == '/sample.txt':
                            response = response_path(path)
                            
                    else:
                        response = response_not_found()
                        
                except NotImplementedError:
                    response = response_method_not_allowed()
                    
                    
#                     TODO: Use response_path to retrieve the content and                                               #                     the mimetype,
#                     based on the request path.

#                     TODO:
#                     If response_path raised
#                     a NameError, then let response be a not_found response. Else,
#                     use the content and mimetype from response_path to build a 
#                     response_ok.
                    
                    
#                    response = response_ok(
#                        body=b"Welcome to my web server",
#                        mimetype=b"text/plain")

                conn.sendall(response)
            
            except:
                traceback.print_exc()
            finally:
                conn.close() 

    except KeyboardInterrupt:
        
        conn.close()
        return "Blah"
    except:
        traceback.print_exc()


if __name__ == '__main__':
    server()
    sys.exit(0)


