import os
import time
from datetime import datetime
import sys
import getpass # for getting username
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

path = ''

# folder definition
pictures_folder = 'Pictures'
documents_folder = 'Documents'
compressed_archives_folder = 'Archives'
sounds_and_music_folder = 'Sounds'
videos_folder = 'Videos'
executables_folder = 'Executables'
other_files_folder = 'Other'

# extentions definition
image_extentions =                ['.png', '.jpg', '.jpeg', '.jpg_large', '.webp', '.gif', '.tiff', '.psd', '.bmp', '.heif', '.indd', '.svg']
document_extentions =             ['.doc', '.docx', '.html', '.htm', '.odt', '.pdf', '.xls', '.xlsx', '.ods', '.ppt', '.pptx', '.txt', '.ppsx']
compressed_archive_extentions =   ['.zip', '.tar', '.xz', '.tgz', '.gz', '.rar', '.jar', '.iso', '.vsix']
sound_and_music_file_extentions = ['.m4a', '.flac', '.mp3', '.wav', '.wma', '.aac']
video_file_extentions =           ['.mp4', '.avi', '.webm', '.mkv', '.flv', '.vob', '.ogv', '.ogg', '.avi', '.mov']
executable_file_extentions =      ['.exe', '.bin', '.AppImage']

ignore_extentions =               ['.crdownload', '.part', '.download', '.tmp', '.filepart', '.opdownload', '.!ut', '.bc!', '.dwl', '.asd',
                                   '.wbk', '.swp', '.swo', '.lk', '.gz.tmp']

# checks if a folder exists. If not the folder will be created
def createFolder(path, folder_name):
    if not os.path.exists(path+folder_name):
        os.makedirs(path+folder_name)
        print("created "+folder_name+" folder")

def checkDefaultDirectories(path):
    createFolder(path, pictures_folder)
    createFolder(path, documents_folder)
    createFolder(path, compressed_archives_folder)
    createFolder(path, sounds_and_music_folder)
    createFolder(path, videos_folder)
    createFolder(path, executables_folder)
    createFolder(path, other_files_folder)

def moveBasedOnExtention(currentTime, file_path, move_folder, extention_list):
    file_data = os.path.splitext(os.path.basename(file_path))

    for extention in extention_list:
        if file_data[1] == extention:
            print(currentTime+": moving {} to ".format(file_data[0]+file_data[1])+move_folder)
            os.rename(file_path, path+move_folder+"/"+file_data[0]+file_data[1])
            moved = True
            break

class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        currentTime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        for filename in os.listdir(path):
            f = os.path.join(path, filename)

            if os.path.isfile(f):
                moveBasedOnExtention(currentTime, f, pictures_folder,               image_extentions);
                moveBasedOnExtention(currentTime, f, documents_folder,              document_extentions);
                moveBasedOnExtention(currentTime, f, compressed_archives_folder,    compressed_archive_extentions);
                moveBasedOnExtention(currentTime, f, sounds_and_music_folder,       sound_and_music_file_extentions);
                moveBasedOnExtention(currentTime, f, videos_folder,                 video_file_extentions);
                moveBasedOnExtention(currentTime, f, executables_folder,            executable_file_extentions);

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '/home/'+getpass.getuser()+'/Downloads/'
    print("\033[33mworking directory: \033[0m"+path)

    checkDefaultDirectories(path)
    
    # set up observer
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    # run programm indefinently except if Ctrl+C is pressed
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
