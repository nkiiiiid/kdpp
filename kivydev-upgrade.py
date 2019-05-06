#coding:u8

import os
ndk_dir = os.environ['ndk_dir']

print('clean p4a dist/build/packages')
os.system('p4a clean_all')

print('install/upgrade p4a dependencies')
os.system('sudo apt-get install -y git ant unzip virtualenv ccache autoconf libtool cmake')

print('uninstall p4a')
os.system('echo y | pip uninstall python-for-android')

print('install new p4a')
os.system('pip install git+https://github.com/kivy/python-for-android.git@master')

print('download 17c ndk')
os.system('wget -P'+' '+ndk_dir+' '+'https://dl.google.com/android/repository/android-ndk-r17c-linux-x86_64.zip')

print('unzip ndk')
os.system('echo y | unzip'+' '+ndk_dir+ '/' + 'android-ndk-r17c-linux-x86_64.zip' + ' -d ' + ndk_dir)

print('upgrade complete')

