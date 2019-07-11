class Request(object):
    def __init__(self, *args):
        pass


    def parsed_request(request):
        """
        把所有的 request 字段全部转换成 dict 格式
        """
        request_dict = {}
        header = request.split('\r\n\r\n')[0]
        body = request.split('\r\n\r\n')[1]
        a = header.split('\r\n')[0]
        others_list = header.split('\r\n')[1:]
        method = a.split()[0]
        path = a.split()[1]
        protocol = a.split()[2]
        print(others_list)
        for i in others_list:
            print('i', i)
            k, v = i.split(': ', 1)
            request_dict[k] = v
        request_dict['method'] = method
        request_dict['protocol'] = protocol
        if '?' in path:
            path, query = path.split('?', 1)
            request_dict['query'] = query
            request_dict['path'] = path
        else:
            request_dict['query'] = ''
            request_dict['path'] = path
        return request_dict


request = 'GET / HTTP/1.1\r\nHost: localhost:2000\r\nConnection: keep-alive\r\nCache-Control: max-age=0\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3\r\nAccept-Encoding: gzip, deflate, br\r\nAccept-Language: zh-CN,zh;q=0.9\r\n\r\n'
print(parsed_request(request))
