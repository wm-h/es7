from elasticsearch7 import Elasticsearch, exceptions
import settings
from importlib import import_module


class EsClient:
    def __init__(self):
        self.conn = Elasticsearch(["localhost:9200"])

    def init_indices(self):
        for index_class_path in settings.INDICES:
            path, index_class_name = index_class_path.rsplit(".", 1)
            model = import_module(path)
            index_class = getattr(model, index_class_name)
            index_body_map = index_class.get_mappings_and_settings()
            index_name = index_class.get_index_name()
            exist = self.conn.indices.exists(index=index_name)
            if exist:
                # 更新已经存在的index的mapping
                # 注意：不可修改type，analyzer，search_analyzer等涉及到分词搜索的字段参数，只能新增字段，新增fields等，且不能删除已存在的字段
                self.conn.indices.put_mapping(index=index_name, body=index_body_map.get("mappings"))

                # self.conn.indices.put_settings(index=index_name, body=index_body_map.get("settings"))
                # 不能修改settings中已经存在的analysis等涉及到分词的字段，原样设置也不行，只能新增
                # 可修改index字段，即修改分片信息
            else:
                # 创建index
                self.conn.indices.create(index=index_name, body=index_body_map)


es = EsClient()
