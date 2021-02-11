import src.util

log_file = open('error_log.txt', 'w', -1, 'utf-8')
print("========== ERROR LOG ==========", file=log_file)

def log(message):
    message = src.util.timestamp() + ' > ' + message
    print(message, file=log_file)
    print(message)
    
def extract_backupfile(backupfile_location) :
    import sqlite3
    import os
    import pathlib
    import shutil
    log("========== Extract Start!! ==========")
    targetdir = backupfile_location
    Manifest_location = pathlib.Path(str(backupfile_location) + "\\Manifest.db")
    def filepath(target):
        folder = target[:2]
        return pathlib.Path(str(targetdir) + r"\\" + folder + r"\\" + target)
    conn = sqlite3.connect(Manifest_location)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Files")
    r = cur.fetchall()
    total_count = len(r)
    for i in range(total_count) :
        target = r[i][0]
        if int(r[i][3]) == 1 :
            file_path = filepath(target)
            realativePath = pathlib.Path(r[i][2])
            file_new_name = realativePath.parts[-1]
            destination_path = r[i][1] + "/" + r[i][2]
            destination_path = list(pathlib.Path(destination_path).parts)
            destination_path.pop()
            destination_path = '/'.join(destination_path)

            if os.path.isdir(destination_path) :
                pass
            else :
                try :
                    cwd = os.getcwd() + "/extract_file/" + destination_path
                    cwd = pathlib.Path(cwd)
                    os.makedirs(cwd)
                except :
                    pass
            try :
                print(i, " / ", total_count, " / ", target, " / ", file_path)
                destination_path = os.getcwd() + "/extract_file/" + destination_path
                destination_path = pathlib.Path(destination_path)
                shutil.copyfile(file_path, os.path.join(destination_path, file_new_name))
            except :
                log("Copy Fail > " + str(destination_path) + " > " + str(file_new_name))
                pass
    print("Success Extract Files")
    log("========== Success Extract Files ==========")
    conn.close()