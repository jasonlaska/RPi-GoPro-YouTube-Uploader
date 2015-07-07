import os
import subprocess

'''
Could make this as configurable as desired.
'''

def shrink(in_file_path, out_file_path):
  subprocess.call(['avconv',
                  '-i', in_file_path,
                  '-s', '854x480',
                  '-strict', 'experimental',
                  '-c:a', 'copy',
                  out_file_path])