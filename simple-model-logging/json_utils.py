# -*- coding:utf-8 -*- 
__author__ = 'jiangjun'
__date__ = '2018/3/28 14:19 '

import json

import logging

# from utils.common_enum import ReturnEnum
# from utils.response import ResponseData

from utils.DateEncoder import DateEncoder

# Get an instance of a logger
logger = logging.getLogger('django')


class JsonUtils:

    @staticmethod
    def row_2_dict(row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
        return d

    @staticmethod
    def obj_2_json_str(obj):
        """
        对象转换为json字符串
        :return:
        """
        json_str = ''
        try:
            dic_data = obj.__dict__
            if dic_data.get('_state') is not None:
                dic_data.pop('_state')
            json_str = json.dumps(dic_data, ensure_ascii=False, cls=DateEncoder)
        except Exception as e:
            logger.error("转换json异常！", e)

        return json_str

    @staticmethod
    def json_str_2_dict(json_str):
        """
        json字符串转换为对象
        :return:
        """
        dict_data = json.loads(json_str, encoding='utf-8')
        return dict_data


# response_data = ResponseData(ReturnEnum.ERROR.value, '指定流程阶段不存在！')
#
# json_str = JsonUtils.obj_2_json_str(response_data)
# print(json_str)
#
# response = JsonUtils.json_str_2_obj(json_str)
# print(type(response))
# print(response)
#
# class_obj = ResponseData(response)
# print(type(class_obj))
# print(class_obj)

# from datetime import datetime
# from datetime import date
#
# d = {'now': datetime.now(), 'today': date.today(), 'i': 100, 'str': '哈哈乐视'}
# ds = json.dumps(d, cls=DateEncoder, ensure_ascii=False)
# print("ds type:", type(ds), "ds:", ds)
# l = json.loads(ds)
# print("l  type:", type(l), "ds:", l)

#{'_state': <django.db.models.base.ModelState object at 0x1115c54a8>, 'id': 37, 'create_time': datetime.datetime(2018, 4, 26, 17, 14, 18, 396593), 'update_time': datetime.datetime(2018, 4, 26, 17, 14, 18, 396623), 'project_name': '昆明市五华区麻园城中村电网改造二期项目', 'project_code': 'GDHY-2018-S-001-00010', 'project_area_id': 1, 'project_type_id': 1, 'project_level_id': 1, 'bidding_type_id': 1, 'batch': '0001', 'owner': '昆明供电局', 'invitation_address': '昆明', 'invitation_time': datetime.datetime(2018, 4, 9, 0, 0), 'build_year': '2018'}
