from op import es


class Field:
    def __init__(
            self,
            name,
            default=None,
            field_type="text",
            analyzer="my_ik_max_word",
            search_analyzer="my_ik_smart",
            fields=None
    ):
        self.name = name
        self.default = default
        self.type = field_type
        self.analyzer = analyzer
        self.search_analyzer = search_analyzer
        self.fields = fields

    def get_map(self):
        m = {
            "type": self.type
        }

        if self.type == "text":
            m["analyzer"] = self.analyzer
            m["search_analyzer"] = self.search_analyzer

        if self.fields is not None and type(self.fields) == dict:
            m["fields"] = {}
            for k, v in self.fields.items():
                if not isinstance(v, Field):
                    raise Exception("excepted obj of class Field")
                # field = Field(v.get("type"), v.get("analyzer"), v.get("search_analyzer"))
                m["fields"][k] = v.get_map()
        return m


class IndexBase:

    @classmethod
    def get_mappings_and_settings(cls):
        mappings = {}
        for field in cls.__dict__.values():
            if isinstance(field, Field):
                mappings[field.name] = field.get_map()
        return {
            "settings": {
                "analysis": {
                    "analyzer": {
                        "my_ik_max_word": {
                            "type": "custom",
                            "tokenizer": "ik_max_word",
                            "char_filter": ["html_strip"],
                        },
                        "my_ik_smart": {
                            "type": "custom",
                            "tokenizer": "ik_smart",
                            "char_filter": ["html_strip"],
                        }
                    }
                }
            },
            "mappings": {
                "properties": mappings
            }
        }

    @classmethod
    def _es_index_doc(cls, index_name, id, doc, **kwargs):
        res = es.conn.create(index=index_name, id=id, body=doc)
        print(res)

    @classmethod
    def create_doc(cls, **kwargs):
        """
        :param kwargs: index doc, cls的类型为Field的属性的名为key,要记录的值为value
        :return: doc map
        """
        if kwargs.get("index_name"):
            kwargs.pop("index_name")

        m = {
            "id": 0
        }
        for k, v in cls.__dict__.items():
            if k == "index_name":
                continue
            if type(v) == classmethod:
                continue
            if k.startswith("__"):
                continue
            if kwargs.get(k) is None:
                if isinstance(v, Field):
                    m[k] = v.default
                    continue
                else:
                    raise Exception(f"excepted field '{k}'")
            m[k] = kwargs.get(k)
            if not m.get("id"):
                raise Exception(f"""unexpected field value 'id={m["id"]}'""")

        cls._es_index_doc(index_name=cls.get_index_name(), id=m.get("id"), doc=m)
        return m

    @classmethod
    def get_index_name(cls):
        if hasattr(cls, "index_name"):
            return cls.index_name
        return cls.__name__.lower()

    @classmethod
    def search_data_by_post(cls, body):
        return es.conn.search(index=cls.get_index_name(), body=body)

    @classmethod
    def query_data_by_id(cls, id):
        return es.conn.get(index=cls.get_index_name(), id=id)


# 定义一个index类后，需要在settings.INDICES中添加类的路径，才能启用

class CONTENT(IndexBase):
    index_name = "content1"  # 自定义index名,不定义则使用类名小写为index名
    id = Field(name="id", field_type="long", default=0)
    title = Field(name="title", default="",
                  fields={"standard": Field(name="standard", analyzer="standard", search_analyzer="standard")})
    author = Field(name="author", default="")
    tag = Field(name="tag", default="")


def init_data():
    for i in range(200, 300):
        CONTENT.create_doc(id=i, title=f"内容-标题{i}", author=f"作者{i}", tag="tag tag content")
