# kdpp 
kivydev plugins platform

## install 

`pip install https://github.com/nkiiiiid/kdpp/releases/download/1.0/kdpp-1.0-py2-none-any.whl`

or 

download whl from release in this repo


#### run this tool in your project dir

#### 请在项目目录下运行本工具


##常用命令

`kdpp init`

在当前目录下生成kdpp.nt配置文件，内容默认如下：

```
[app]

# (int) 是否升级打包环境（0=否，1=是）
kivydev.upgrade = 0


[env]

# (str) 定义环境变量
sdk_dir = ~/andr
ndk_dir = ~/andr
build_dir = ~/.local/share/python-for-android
```

app区块暂时没用，没用实现功能，但是不能删除。

env定义环境变量，定义了三个变量：

sdk_dir，Android sdk所在目录 

ndk_dir, ndk所在目录 

build_dir, python-for-android的build/dist/package所在目录

如果你要在自己的虚拟机里使用本工具，可以修改这三个变量为你的虚拟机的相应目录。


`kdpp kdupgrade`

升级虚拟机环境

`kdpp getplugs`

获取插件列表，并且选择安装插件

`kdpp go`

打包apk

`kdpp runplug plugfilename`

运行插件，比如 `kdpp runplug kivydev-upgrade`

`kdpp rmplug pluginfilename`

删除插件，比如 `kdpp rmplug kivydev-upgrade`

`kdpp help`

查看帮助



enjoy!

![](https://i.imgur.com/h5TYad8.png)
