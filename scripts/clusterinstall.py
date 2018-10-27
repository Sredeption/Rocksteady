#!/usr/bin/env python
# Copyright (c) 2010 Stanford University
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR(S) DISCLAIM ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL AUTHORS BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import sys
import os
from common import *
from subprocess import Popen, PIPE

def getObjDir():
    git_ref = Popen(['git', 'symbolic-ref', '-q', 'HEAD'], stdout=PIPE)
    sed = Popen(['sed', '-e', 's,refs/heads/,.,'], stdin=git_ref.stdout, stdout=PIPE)
    git_ref.stdout.close()
    output,err = sed.communicate()
    return 'obj%s' % output.strip()

def newWorkDir(host, workDir):
    return Popen(['ssh', host, 'rm -rf %s && mkdir -p %s' % (workDir, workDir)])

def install(host, workDir, rc_path, obj_dir):
    binary_process = Popen(['scp', '-r', '%s/%s' % (rc_path, obj_dir), '%s:%s/obj' % (host, workDir)])
    script_process = Popen(['scp', '-r', '%s/scripts' % rc_path, '%s:%s/scripts' % (host, workDir)])
    return [binary_process, script_process]

if __name__ == '__main__':
    install_path = '/home/hkucs/ramcloud-target'
    script_path = os.path.split(os.path.realpath(__file__))[0]
    rc_path = script_path.split('/scripts')[0]
    print(rc_path)
    obj_dir = getObjDir()
    obj_path = '%s/%s' % (rc_path, obj_dir)
    print(script_path)
    print(obj_path)
    
    hosts = getHosts()
    setup_processes = [newWorkDir(name, install_path) for (name, ip, no) in hosts]
    # watiing for directory setup
    for p in setup_processes:
        p.wait()
    install_processes = [install(name, install_path, rc_path, obj_dir) for (name, ip, no) in hosts]
    # watiing for install finish
    for processes in install_processes:
        for p in processes:
            p.wait()
