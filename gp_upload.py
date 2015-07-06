#!/usr/bin/python
'''
Upload (YouTube) and transcode all GoPro videos.
'''
import os
import subprocess
from optparse import OptionParser
from datetime import datetime

from utilities.gpfiles import GPFiles
from utilities import transcode

def get_file_ts(file_path):
  statbuf = os.stat(file_path)
  return statbuf.st_mtime

def ts_to_dt_string(file_ts):
  '''
  Assume timestamps on fs are in local timezone.
  '''
  dt = datetime.fromtimestamp(file_ts)
  return dt.strftime("%A, %d. %B %Y %I:%M%p")

def dt_string_to_outfile_path(dt_string):
  return '_'.join(dt_string.split(' ')) + '.mp4'

def video_attributes(dt_string):
  vattr = {
    'title': '{} 854x480 -- GoPro'.format(dt_string),
    'description': 'Bike commute on {}'.format(dt_string),
  }
  return vattr

def process_gopro(options):
  with GPFiles() as gopro:
    # Loop through each video file
    for file_path in gopro.files():
      # File timestamp
      file_ts = get_file_ts(file_path)

      # Get time of last_modified as string
      dt_string = ts_to_dt_string(file_ts)

      print 'GoPro Processing'
      print 'File:', file_path
      print 'Datetime:', dt_string
      print '---'

      # Transcode video
      if options.transcode:
        print 'Transcoding...'
        # Get outfile path
        out_file_path = dt_string_to_outfile_path(dt_string)
        
        # Run FFMPEG
        transcode.shrink(file_path, out_file_path)
      else:
        # No Transcoding
        out_file_path = file_path

      # Use datetime string to generate title and description
      vattr = video_attributes(dt_string)

      # Upload video
      print 'Uploading to YouTube...'
      subprocess.call(['scripts/upload_video.py',
                      '--file', out_file_path,
                      '--title', vattr['title'],
                      '--description', vattr['description']])

      # Delete local transcoded video
      if options.transcode and os.path.exists(out_file_path):
        os.remove(out_file_path)

      # Delete GoPro video
      if options.remote_delete and os.path.exists(file_path):
        os.remove(file_path)


if __name__ == '__main__':
  parser = OptionParser()
  parser.add_option("-t", "--transcode-off", dest="transcode", help="disable transcoding",
    default=True, action="store_false")
  parser.add_option("-d", "--remote-delete", dest="remote_delete", help="delete files on GoPro",
    default=False, action="store_true")
  (options, args) = parser.parse_args()

  # Run processing
  process_gopro(options)