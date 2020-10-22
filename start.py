from op import es
import indices

if __name__ == '__main__':
    es.init_indices()
    # indices.init_data()
    print(indices.CONTENT.query_data_by_id(1))
    print(indices.CONTENT.search_data_by_post({
        "_source": False,  # 是否返回_source
        "query": {
            "multi_match": {  # 同一个关键字，多字段查询
                "query": "9",
                "fields": ["title.standard"]
            }
        }
    }))
    print(indices.CONTENT.search_data_by_post({
        "_source": False,  # 是否返回_source
        "query": {
            "terms": {  # 同一个字段，多关键词查询
                "title": ["1", "2"],
            }
        }
    }))
    print(indices.CONTENT.search_data_by_post({
        "_source": False,  # 是否返回_source
        "query": {
            "bool": {
                "must": [  # 必须匹配，多条件AND查询，为空或者不传时查询所有
                    # {"match": {"title": "101"}},
                    # {"match": {"author": "作者"}},
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
