import configparser
import json
import os
import pathlib


class TestData(object):
    pass


class DataLoader:
    base_path = str(pathlib.Path(__file__).parent.parent.absolute()) + "/resources/data/"

    @classmethod
    def get_data_from_ini_file(cls, data_file_name):
        data_resources_file_path = DataLoader.base_path + data_file_name
        current_env = os.getenv('env')
        data = TestData()

        if data_file_name is not None:
            parser = configparser.ConfigParser()
            parser.read(data_resources_file_path)

            config_section_values = parser[current_env]

            for key in config_section_values:
                _property = config_section_values.get(key)
                setattr(data, key, _property)

        return data

    @classmethod
    def get_data_from_txt_file(cls, data_file_name):
        data_resources_file_path = DataLoader.base_path + data_file_name
        with open(file=data_resources_file_path, mode="r", encoding='UTF-8') as f:
            data = f.read()
        return data

    @classmethod
    def get_data_from_json_file(cls, data_file_name):
        data_resources_file_path = DataLoader.base_path + data_file_name
        with open(file=data_resources_file_path, mode="r", encoding='UTF-8') as f:
            data = json.load(f)
        return data
