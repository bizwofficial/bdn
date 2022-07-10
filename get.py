import requests
import copy

MEDIA_SUFFIXES = ('.jpg', '.jpeg', '.png', '.svg', '.gif', '.tif',
    '.tiff', '.mp3', '.mp4', '.wmv', '.aac', '.webp', '.m3u', 
    '.m3u8', '.avi', '.mov', '.asf', '.rm', '.mpeg', '.mpg', '.qt',
    '.ram', '.dat', '.rmvb', '.ra', '.viv', '.asf', '.iso', '.bin',
    '.exe', '.img', '.tao', '.dao', '.cif', '.fcd', '.swf', '.flash', 
    '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.pdf')

autofill_schema = lambda url_list: ['http:'+each if each.startswith('//') else each for each in url_list]

def geturls(uri: str, headers: dict, autofill=False, proxy=False, http_proxy='', https_proxy=''):
    try:
        if proxy:
            raw = requests.get(uri,headers=headers,proxies={'http': http_proxy, 'https': https_proxy}).text
        else:
            raw = requests.get(uri, headers=headers).text
    except:
        return []
    raw_list = list(raw)
    urls = []

    for i, chr in enumerate(raw_list):
        if chr == '"':
            raw_list[i] = "'"
    lines = ''.join(raw_list).split('\n')
    # print(lines)

    keywords = ["'//", "'http://", "'https://"]
    for keyword in keywords:
        for line in lines:
            while line.find(keyword) != -1 and line.find("'",len(keyword)) != -1:
                urls.append(keyword[1:]+line[line.find(keyword)+len(keyword):line.find("'",line.find(keyword)+1)])
                line = line[line.find("'",line.find(keyword)+1):]

    # print(urls)
    if autofill:
        return autofill_schema(urls)
    else:
        return urls

def geturls_recur(url_key:str, uri: str, **other_para_of_geturls):
    urls = set()

    def core(uri: str, **other_para_of_geturls):
        nonlocal urls
        try:
            current_urls = list(filter(lambda url: url_key in url, set(geturls(uri, **other_para_of_geturls)).difference(urls)))
            print(f'current_urls = {current_urls}')
            if current_urls:
                urls = urls.union(current_urls)
                for each in current_urls:
                    mark = True
                    for suffix in MEDIA_SUFFIXES:
                        if each.endswith(suffix) or each.endswith(suffix.upper()):
                            mark = False
                            break
                    if mark:
                        under = core(each, **other_para_of_geturls)
                        if under:   urls = urls.union(under)
            else:
                print(f'Layer returned: {urls}')
        except TypeError:
            pass

    return core(uri, **other_para_of_geturls)

if __name__ == '__main__':
    result = list(geturls_recur('rdfz.cn', 'https://www.rdfz.cn', headers={'User-Agent': 'curl/7.29.0'}, autofill=True, proxy=False))
    with open('result.txt', 'w') as fil:
        print(*result, file=fil, sep='\n')
