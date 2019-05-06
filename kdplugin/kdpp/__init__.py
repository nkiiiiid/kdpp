#coding:u8
'''
Kdpp
=========

Generic package environment plugin platform for kivydev64.

'''

__version__ = '1.0'


import os
import re
import sys
import select
import codecs
import textwrap
from sys import stdout, stderr, exit
from re import search
from os.path import join, exists, dirname, realpath, splitext, expanduser
from os import environ, unlink, walk, sep, listdir, makedirs
from copy import copy
from shutil import copyfile, rmtree, copytree, move
import socket
socket.setdefaulttimeout(30)

try:
    from urllib.request import FancyURLopener
    from configparser import SafeConfigParser
except ImportError:
    from urllib import FancyURLopener
    from ConfigParser import SafeConfigParser

try:
    #终端颜色
    import colorama
    colorama.init()
    RESET_SEQ = colorama.Fore.RESET + colorama.Style.RESET_ALL
    COLOR_SEQ = lambda x: x  # noqa: E731
    BOLD_SEQ = ''
    if sys.platform == 'win32':
        BLACK = colorama.Fore.BLACK + colorama.Style.DIM
    else:
        BLACK = colorama.Fore.BLACK + colorama.Style.BRIGHT
    RED = colorama.Fore.RED
    BLUE = colorama.Fore.CYAN
    ORANGE = colorama.Fore.YELLOW
    USE_COLOR = 'NO_COLOR' not in environ

except ImportError:
    if sys.platform != 'win32':
        RESET_SEQ = "\033[0m"
        COLOR_SEQ = lambda x: "\033[1;{}m".format(30 + x)  # noqa: E731
        BOLD_SEQ = "\033[1m"
        BLACK = 0
        RED = 1
        ORANGE = 3
        BLUE = 4
        USE_COLOR = 'NO_COLOR' not in environ
    else:
        RESET_SEQ = ''
        COLOR_SEQ = ''
        BOLD_SEQ = ''
        RED = BLUE = BLACK = ORANGE = 0
        USE_COLOR = False
        print("check")
        
# error, info, debug
LOG_LEVELS_C = (RED, BLUE, BLACK, ORANGE)
LOG_LEVELS_T = 'EID'
SIMPLE_HTTP_SERVER_PORT = 8000
IS_PY3 = sys.version_info[0] >= 3

LOGO = '''
 _          _                 
| | __   __| |  _ __    _ __  
| |/ /  / _` | | '_ \  | '_ \ 
|   <  | (_| | | |_) | | |_) |
|_|\_\  \__,_| | .__/  | .__/ 
               |_|     |_|    
                              
'''

class KdppURL(FancyURLopener):
    version = (
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36')

class KdppDld(object):
    def urlretrieve(self, url, filename, report_hook):
        try:
            opener = KdppURL()
            opener.retrieve(url, filename, report_hook)
        except socket.timeout:
            count = 1
            while count <= 5:
                try:
                    opener.retrieve(url, filename, report_hook)
                    break
                except socket.timeout:
                    print('重新加载')
                    count +=1
            if count > 5:
                print('下载失败')

        
    def download(self, url, filename, cwd=None):
        def report_hook(index, blksize, size):
            if size <= 0:
                progression = '{0} bytes'.format(index * blksize)
            else:
                progression = '{0:.2f}%'.format(
                        index * blksize * 100. / float(size))

            stdout.write('- 下载 {}\r'.format(progression))
            stdout.flush() 
        if cwd:
            filename = join(cwd, filename)
        if exists(filename):
            unlink(filename)
        print('下载 {0}'.format(url))
        self.urlretrieve(url, filename, report_hook)

                

class KdppException(Exception):
    pass


class KdppCmdException(KdppException):
    pass


class Kdpp(object):

    ERROR = 0
    INFO = 1
    DEBUG = 2
    TITLE = 3

    standard_cmds = ('distclean', 'update', 'debug', 'release',
                     'deploy', 'run', 'serve')

    def __init__(self, filename='kdpp.nt'):
        super(Kdpp, self).__init__()
        self.environ = {}
        self.ntfilename = filename
        self.config = SafeConfigParser(allow_no_value=True)
        self.config.getdefault = self._get_config_default

        self.plug_dir = join(dirname(__file__), 'plugins')
        self.mkdir(self.plug_dir)
        
        self.download = KdppDld().download

        
    def check_kdpp_nt(self):
        if not exists(self.ntfilename):
            copyfile(join(dirname(__file__), 'kdpp.nt'), 'kdpp.nt')
        try:
            self.config.read(self.ntfilename, "utf-8")
        except TypeError:
            self.config.read(self.ntfilename)
        self.check_configuration_tokens()    

    
    def check_p4a(self):
        if not exists('.p4a'):
            copyfile(join(dirname(__file__), 'default.p4a'), '.p4a')

    
    def check_configuration_tokens(self):
        '''检查配置文件是否正确.
        '''
        self.info('检查kdpp.nt文件.')
        get = self.config.getdefault
        errors = []
        adderror = errors.append

        self.upgrade = get('app', 'kivydev.upgrade', '')
        self.envtokens = self.config.options('env')
        
        if not self.upgrade:
            adderror('找不到[app] "kivydev.upgrade" ')

        if not self.envtokens:
            adderror('找不到[env] tokens ')
        else:
            for i in self.envtokens:
                os.environ[i] = get('env',i)
                #print(i,os.environ[i]) 
        
            
        if errors:
            self.error('kdpp.nt存在{0}个错误 '.format(
                len(errors)))
            for error in errors:
                print(error)
            exit(1)

            
    def run_default(self):
        self.title(LOGO)
        self.error('请确保在项目目录下运行本命令')
        print('使用 "kdpp help"查看用法"')
        exit(0)


    def run_command(self, args):
        while args:
            if not args[0].startswith('-'):
                break
            arg = args.pop(0)

            if arg in ('-h', '--help'):
                self.check_kdpp_nt()
                self.usage()
                exit(0)

            elif arg == '--version':
                print('kdpp {0}'.format(__version__))
                exit(0)

        if not args:
            self.run_default()
            return

        command, args = args[0], args[1:]
        cmd = 'cmd_{0}'.format(command)

        if hasattr(self, cmd):
            getattr(self, cmd)(*args)
            return


    def usage(self):
        self.title(LOGO)
        print('用法:')
        print('    kdpp <命令>...')
        print('')
        print('可用的命令:')
        cmds = [x for x in dir(self) if x.startswith('cmd_')]
        for cmd in cmds:
            name = cmd[4:]
            meth = getattr(self, cmd)
            if not meth.__doc__:
                continue
            doc = [x for x in
                    meth.__doc__.strip().splitlines()][0].strip()
            print('  {0:<18} {1}'.format(name, doc))

    
    def cmd_init(self, *args):
        '''生成kdpp.nt
        '''
        if exists('kdpp.nt'):
            self.error('错误：已经存在kdpp.nt.')
            exit(1)
        copyfile(join(dirname(__file__), 'kdpp.nt'), 'kdpp.nt')
        self.info('信息：kdpp.nt创建完毕')

    
    def cmd_help(self, *args):
        '''显示帮助
        '''
        self.usage()

    def cmd_go(self, *args):
        '''运行p4a apk
        '''
        self.buildapk(*args)

    def cmd_kdupgrade(self, *args):
        '''升级打包环境
        '''
        self.kdupgrade()
    
    def cmd_getplugs(self, *args):
        '''获取插件列表
        '''
        self.getplugs()
        
    def cmd_runplug(self, *args):
        '''运行插件, kdpp runplug pluginfilename
        '''
        self.check_kdpp_nt()
        if not args:
            self.error("错误：缺少参数")
            exit(1)
        os.system('python' + ' ' + self.plug_dir + '/' + args[0] + '.py')

    
    def buildapk(self,*args):
        self.check_p4a()
        os.system('p4a apk') 
        
    def kdupgrade(self, *args):
        self.check_kdpp_nt()
        plug_name = 'kivydev-upgrade'
        plug_full_name = self.plug_dir + '/' + plug_name + '.py'
        if not exists(plug_full_name):
            plug_url = 'https://raw.githubusercontent.com/nkiiiiid/kdpp/master/kivydev-upgrade.py'
            self.download(plug_url, plug_full_name)
        os.system('python' + ' ' + plug_full_name)
    
    def getplugs(self, *args):
        from kdpp.tools.netcrawl import NetCrawl
        netc = NetCrawl()
        target_list = netc.start_crawl('https://raw.githubusercontent.com/nkiiiiid/kdpp/master/plugs-list-file.txt',r'begin[\s\S]*ends')
        plugs_list = netc.get_plugs_list(target_list)
        for i in plugs_list:print i[:-2]
        try:
            plugnum = raw_input("输入要安装的插件序号：")
        except:
            plugnum = input("输入要安装的插件序号：")
        try:
            plugnum = int(plugnum)
        except:
            self.error('输入错误')
            exit(1)    
        if plugnum-1 in range(len(plugs_list)):
            plug_url = plugs_list[plugnum-1].split(',')[-1]
            plug_name = plugs_list[plugnum-1].split(',')[1]
            self.download(plug_url, self.plug_dir + '/' + plug_name + '.py')
        else:
            self.error('超出序号范围')

    
    def log(self, level, msg):
        if USE_COLOR:
            color = COLOR_SEQ(LOG_LEVELS_C[level])
            print(''.join((RESET_SEQ, color, msg, RESET_SEQ)))
        else:
            print('{} {}'.format(LOG_LEVELS_T[level], msg))


    def info(self, msg):
        self.log(self.INFO, msg)
    
    def error(self, msg):
        self.log(self.ERROR, msg)
    
    def title(self, msg):
        self.log(self.TITLE, msg)
    

    def _get_config_default(self, section, token, default=None):
        if not self.config.has_section(section):
            return default
        if not self.config.has_option(section, token):
            return default
        return self.config.get(section, token)

    def mkdir(self, dn):
        if exists(dn):
            return
        self.info('创建目录 {0}'.format(dn))
        makedirs(dn)

    def rmdir(self, dn):
        if not exists(dn):
            return
        self.info('删除目录 {}'.format(dn))
        rmtree(dn)