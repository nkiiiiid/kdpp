#coding:u8
try:
    from urllib.error import URLError
    from urllib.request import urlopen
except ImportError:
    from urllib2 import URLError
    from urllib2 import urlopen
    
import re
import ssl

class NetCrawl(object):
    def __init__(self, **kw):
        ssl._create_default_https_context = ssl._create_unverified_context
        super(NetCrawl,self).__init__(**kw)

        
    def decode_page(self, page_bytes, charsets=('utf-8',)):
        page_html = None
        for charset in charsets:
            try:
                page_html = page_bytes.decode(charset)
                break
            except UnicodeDecodeError:
                pass
                # logging.error('Decode:', error)
        return page_html


    def get_page_html(self, seed_url, retry_times=3, charsets=('utf-8',)):
        page_html = None
        try:
            page_html = self.decode_page(urlopen(seed_url).read(), charsets)
        except URLError:
            if retry_times > 0:
                return get_page_html(seed_url, retry_times=retry_times - 1,
                                     charsets=charsets)
        return page_html


    def get_matched_parts(self, page_html, pattern_str, pattern_ignore_case=re.I):
        pattern_regex = re.compile(pattern_str, pattern_ignore_case)
        return pattern_regex.findall(page_html) if page_html else []


    def start_crawl(self, seed_url, match_pattern): 
        page_html = self.get_page_html(seed_url, charsets=('utf-8', 'gbk', 'gb2312'))
        target_list = self.get_matched_parts(page_html, match_pattern)
        return target_list

        
    def get_plugs_list(self, plugs_list):  
        plugs_list = plugs_list[0].split(';')
        plugs_list = plugs_list[1:-1]
        for i,j in enumerate(plugs_list):
            j = j[1:] if j.startswith('\n') else j
            plugs_list[i]=j
        return plugs_list


if __name__ == '__main__':
    netc = NetCrawl()
    target_list = netc.start_crawl('https://raw.githubusercontent.com/nkiiiiid/kdpp/master/plugs-list-file.txt',r'begin[\s\S]*ends')
    plugs_list = netc.get_plugs_list(target_list)
    print plugs_list