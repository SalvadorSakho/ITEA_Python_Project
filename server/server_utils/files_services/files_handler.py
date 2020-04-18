import os
import shutil

objects_path_dict = {}


async def search_in_static(object_name, where_to_search='static'):
    if object_name in objects_path_dict.keys():
        return objects_path_dict[object_name]

    for server_object_name in os.listdir('static'):
        for data in os.listdir(f'{where_to_search}/{server_object_name}'):
            if object_name in data:
                objects_path_dict[object_name] \
                    = f"{where_to_search}/{server_object_name}/{object_name}"
                break
    return objects_path_dict[object_name]


async def create_folder(folder_path):
    if not os.path.exists(f"{folder_path}"):
        os.makedirs(f"{folder_path}")


async def compress_descriptions(path):
    shutil.make_archive(
        os.path.realpath(path), 'zip'
        , os.path.realpath(path)
    )
    shutil.rmtree(os.path.realpath(path), ignore_errors=True)
    return f'{os.path.realpath(path)}.zip'

