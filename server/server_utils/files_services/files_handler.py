import os

objects_path_dict = {}


async def search_in_static(object_name, where_to_search='static'):
    if object_name in objects_path_dict.keys():
        return objects_path_dict[object_name]

    for server_object_name in os.listdir('static'):
        for data in os.listdir(f'{where_to_search}/{server_object_name}'):
            if object_name in data:
                objects_path_dict[object_name] \
                    = f"{where_to_search}/{server_object_name}/{object_name}"
    return objects_path_dict[object_name]
