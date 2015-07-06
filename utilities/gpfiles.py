import os
import subprocess
import shutil

class GPFiles(object):
  def __init__(self, mnt_path=None):
    self._mnt_path = 'gopro_files'
    if mnt_path is not None:
      self._mnt_path = mnt_path

  def __enter__(self):
    self._init_fs()
    
    if not self._valid_mount():
      self._teardown_fs()
      return None

    return self

  def __exit__(self, type, value, traceback):
    self._teardown_fs()

  def _init_fs(self):
    if not os.path.exists(self._mnt_path):
      os.mkdir(self._mnt_path)

    subprocess.call(['gphotofs', self._mnt_path])

  def _teardown_fs(self):
    # may have to run script with sudo to execute this command
    subprocess.call(['umount', self._mnt_path])

  def _valid_mount(self):
    try:
      result = subprocess.check_call(['ls', self._mnt_path])
      return True
    except:
      print 'Unable to access mounted photofs at {}'.format(self._mnt_path)
      return False

  def files(self):
    for subdir, dirs, gp_files in os.walk(self._mnt_path):
      for f in gp_files: 
        if f.lower().endswith('.mp4'):
          yield os.path.join(subdir, f)
