import os
from collections.abc import Iterable


async def search_in_resource(object_name):
    folder = []
    for file_structure_object in os.walk('resources'):
        if isinstance(file_structure_object, Iterable):
            folder.append(file_structure_object)
