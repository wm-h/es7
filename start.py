from op import es
import indices

if __name__ == '__main__':
    es.init_indices()
    # indices.init_data()
    print(indices.CONTENT.query_data_by_id(1))
    print(indices.CONTENT.search_data_by_post({
        "_source": False,  # 是否返回_source
        "query": {
            "multi_match": {  # 同一个关键字（分词），多字段查询
                "query": "9",
                "fields": ["title.standard"]
            }
        }
    }))
    print(indices.CONTENT.search_data_by_post({
        "_source": False,  # 是否返回_source
        "query": {
            "terms": {  # 同一个字段，多关键词查询（不分词）
                "title": ["内容1000", "内容10001"],
            }
        }
    }))
    print(indices.CONTENT.search_data_by_post({
        "query": {
            "query_string": {
                # 多条件模糊匹配  详见官方文档https://www.elastic.co/guide/en/elasticsearch/reference/7.9/query-dsl-query-string-query.html#query-string-syntax
                "query": "(title:201 OR author:200) AND (tag:content)"  # 支持类似语法  对每一个搜索词都做分词
            }
        }
    }))
    print(indices.CONTENT.search_data_by_post({
        "_source": False,  # 是否返回_source
        "query": {
            "bool": {
                "must": [  # 必须匹配，多条件AND查询，为空或者不传时查询所有
                    # match对搜索词分词，命中任意分词即可
                    # match_phrase对搜索词分词 若搜索字段是text，则搜索词分词结果必须在text字段分词中都包含，而且顺序必须相同，而且必须都是连续的
                    # match_phrase对搜索词分词 若搜索字段是keyword，搜索词必须与字段值完全一致
                    # term 不对搜索词分词 keyword字段必须与搜索词完全匹配，text字段分词结果必须有与搜索词一致的结果
                    # {"match": {"title": "101"}},  # 搜索词分词后，进行匹配查找
                    # {"match_phrase": {"author": "作者101"}},  # match_phrase的分词结果必须在text字段分词中都包含，而且顺序必须相同，而且必须都是连续的
                ],
                "must_not": [  # 必须不匹配，在must结果中多条件OR过滤，为空或者不传时不过滤
                    # {"match": {"title": "101"}},
                    # {"match": {"author": "103"}}
                ],
                "should": [  # 至少匹配一个，在must_not结果中OR过滤，为空或者不传时不过滤
                    # {"match": {"title": "101"}},
                    # {"match": {"title": "102"}},
                    # {"match": {"title": "103"}}
                ],
                "filter": [  # 在should结果中，按条件AND筛选，为空或者不传时不过滤
                    # {"term": {"title": "101"}},
                    # {"term": {"author": "101"}}
                ]
            }
        }
    }))
