About RPi GoPro Uploader
===
This collection of scripts makes it easy-ish to archive your footage.

For all .mp4 files on the camera, the utility will

1. Transcode the video to 480p 
    
    Shrinks the video to 854x480.  This step is meant to enable faster uploading and less bandwidth usage. The RPi is not the best tool for transcoding and so this can take a while for longer videos.

    This step is implemented as a simple wrapper around ffmpeg and can be easily customized.

2. Upload video to YouTube

    Automatically chooses a title based on the file datetime.  Title, tags, and description can be easily customized.

Provisioning RPi for GoPro file access
===

1. Install required tools 

    We use gphotofs for mounting the GoPro.  The utility gphoto2 also provides some handy tools for accessing the camera.

        sudo apt-get install gphoto2 gphotofs -y
        sudo apt-get install ffmpeg -y

2. Fix gphoto2/gphotofs on RPi

    Raspbian ships with version 2.4 of gphoto2/gphotofs.  This version adds some files that block some devices from being mountd appropriately with these utilities.  We must rename these files.  

    More information can be found here: https://www.raspberrypi.org/forums/viewtopic.php?t=70049&p=508638

    **Note:** v2.5 does not contain this bug, if you install it directly instead, then you do not need this step.

    Rename files:

        sudo mv /usr/share/gvfs/mounts/gphoto2.mount /usr/share/gvfs/mounts/gphoto2.mount.old
        sudo mv /usr/share/gvfs/remote-volume-monitors/gphoto2.monitor /usr/share/gvfs/remote-volume-monitors/gphoto2.monitor.old
        sudo mv /usr/lib/gvfs/gvfs-gphoto2-volume-monitor /usr/lib/gvfs/gvfs-gphoto2-volume-monitor.old

    **Note:** You may also have to give the `pi` username permissions to use both `gphotofs` and `umount`

    Reboot the RPi.

        sudo reboot

3. Install python requirements

        sudo pip install -r requirements.txt

Configuring scripts for YouTube
===

Get a Google `client_secrets.json` file from 

    https://code.google.com/apis/console#access

and put in the root directory where `gp_upload.py` will run.

**Note:** You will need to run the script manually at least once with a web browser available so that the project can download an OAuth token (will show up in `/scripts`).

**Note:** You will also need to enable the YouTube API for this project.

Running the script (once)
===

1. Connect GoPro to RPi (usb) and turn on GoPro

    The screen should display:

        USB Connected
        Camera Files Accessible

2. To execute the script run

        ./gp_upload.py

    You may want to run the script with `sudo` so that the RPi can be appropriately unmounted after the uploading has finished (or add /gopro_files to fstab).


Autodetecting GoPro + RPi connection
===



Customizing transcode wrapper
===
The transcode wrapper can be found at `utilities/transcode.py`.  The script calls subprocess.call(['ffmpeg']) with some stock parameters.  

See here for some boilerplate options:

    http://www.labnol.org/internet/useful-ffmpeg-commands/28490/


Acknowledgements
===

Uses `upload_video.py` example from https://code.google.com/p/youtube-api-samples/source/browse/samples/python/upload_video.py

