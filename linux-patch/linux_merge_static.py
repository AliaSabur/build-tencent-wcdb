#!/usr/bin/env python3
import os
import shutil
import time
import subprocess
import hashlib
import tempfile
import glob

from typing import List
from typing import Dict


def libtool_libs_linux(src_libs, dst_lib):
    """Linux 专用静态库合并函数"""
    # 创建临时工作目录（自动清理）
    with tempfile.TemporaryDirectory() as tmp_dir:
        # 合并所有目标文件到临时目录
        for src_lib in src_libs:
            # 解压每个库的所有 .o 文件到临时目录
            subprocess.run(
                ['ar', 'x', os.path.abspath(src_lib)],
                cwd=tmp_dir,
                check=True
            )
        
        # 获取所有解压出的目标文件
        obj_files = [os.path.join(tmp_dir, f) for f in os.listdir(tmp_dir)]
        
        # 创建新的静态库
        subprocess.run(
            ['ar', 'cr', os.path.abspath(dst_lib)] + obj_files,
            check=True
        )
        
        # 生成符号索引
        subprocess.run(['ranlib', dst_lib], check=True)
    
    return os.path.exists(dst_lib)

    
def main():
    # ssl_lib = 'openssl/openssl_lib_linux_x64/libssl.a'
    # crypto_lib = 'openssl/openssl_lib_linux_x64/libcrypto.a'
    
    dst_lib = 'src/build/libWCDB_merged.a'
    
    src_libs = glob.glob('src/build/*.a')
    # src_libs.append(ssl_lib)
        
    if not libtool_libs_linux(src_libs, dst_lib):
        return False

if __name__ == '__main__':
    main()
