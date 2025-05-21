import utils.files.check as check_utils
import utils.files.search as search_utils
import utils.files.basics as file_basics
import utils.files.path as path_utils
import utils.files.upload as upload_utils
import utils.data.list as list_utils


if __name__ == '__main__':
    source_path = 'generated_dataset'
    remote_path = 'papers storage/sigspatial2024-outlier-dataset'
    # remote_path = 'TEMP'
    upload_utils.upload_folder(source_path, remote_path,replace=True)
