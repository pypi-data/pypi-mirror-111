import os


class FileManager:

    def remove_files_and_dirs_ignore_case(self, path, files_to_remove, dirs_to_remove):
        for f in os.listdir(path):
            f_path = os.path.join(path, f)
            if os.path.isfile(f_path) and f.lower() in files_to_remove:
                os.remove(f_path)

            if os.path.isdir(f_path) and f.lower() in dirs_to_remove:
                os.system("rm -rf " + f_path)
