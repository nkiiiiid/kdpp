# kdpp 
kivydev plugins platform

## install 

`pip install https://github.com/nkiiiiid/kdpp/releases/download/1.0/kdpp-1.0-py2-none-any.whl`

or 

download whl from release in this repo


#### run this tool in your project dir

#### 请在项目目录下运行本工具


## 0x01 常用命令

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

## 0x02 插件开发流程



-  插件使用python编写，插件平台kdpp.nt文件配置的全部环境变量可以供插件使用，环境变量调用方法：
```
import os
ndk_dir = os.environ['ndk_dir']
```
目前可以使用的环境变量就是上面提到的env区块。

- 插件可以按照普通py脚本形式实现任意功能，如果需要额外的环境变量支持，可以在本repo提issue，我会在下次更新中择优添加。

- 插件开发完毕后上传到网络，将地址提供给我，我会添加到`plugs-list-file`当中，按照以下格式提供：  
 `插件文件名，插件功能描述，插件下载地址  ` 


enjoy!

![](https://i.imgur.com/h5TYad8.png)
