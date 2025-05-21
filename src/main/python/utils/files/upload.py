from rclone_python import rclone

def upload_folder(source_path, remote_path, drive='onedrive', replace=False):
    if replace:
        rclone.copy(source_path, f'{drive}:{remote_path}', args=['--create-empty-src-dirs'])
    else:
        rclone.copy(source_path, f'{drive}:{remote_path}', ignore_existing=True, args=['--create-empty-src-dirs'])