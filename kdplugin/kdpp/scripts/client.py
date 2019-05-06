'''
Main Buildozer client
=====================

'''
#coding:u8
import sys
from kdpp import Kdpp, KdppCmdException, KdppException


def main():
    try:
        Kdpp().run_command(sys.argv[1:])
    except KdppCmdException:
        # don't show the exception in the command line. The log already show
        # the command failed.
        sys.exit(1)
    except KdppException as error:
        Kdpp().error('%s' % error)
        sys.exit(1)

if __name__ == '__main__':
    main()
