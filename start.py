from op import es
import indices

if __name__ == '__main__':
    es.init_indices()
    # indices.init_data()
    # indices.CONTENT.update_by_query({
    #     "script": {
    #         # 注意：给某个字段添加fields属性后，更新该字段值即可使得新加的fields参数生效
    #         "source": "ctx._source.tag=ctx._source.tag"
    #     }
    # })

    # 常用的搜索
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
            "terms": {  # 同一个字段，多关键词（不分词）查询
                "title": ["内容1000", "内容10001"],
            }
        }
    }))
    print(indices.CONTENT.search_data_by_post({
        "query": {
            "query_string": {
                # 多条件模糊匹配
                # 详见官方文档https://www.elastic.co/guide/en/elasticsearch/reference/7.9/query-dsl-query-string-query.html#query-string-syntax
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
                "filter": [  # 在should结果中，按条件AND筛选，为空或者不传时不过滤   filter过滤之后，不返回score
                    # {"term": {"title": "101"}},
                    # {"term": {"author": "101"}}
                ]
            }
        }
    }))

    # 排序
    print(indices.CONTENT.search_data_by_post({
        "query": {
            "match_all": {}
        },
        "sort": {  # 单字段排序
            # text类型默认禁止聚合排序等操作；
            # keyword类型可以直接用于聚合排序等
            # mapping时给text类型的字段添加参数fielddata=true即可开启聚合排序
            # mapping时给text类型的字段添加fields参数，设置type=keyword，即可用改fields参数用于聚合排序
            # fielddata 说明文档 https://www.elastic.co/guide/en/elasticsearch/reference/7.9/fielddata.html
            "tap": "desc"
        }
    }))
    print(indices.CONTENT.search_data_by_post({
        "query": {
            "match_all": {}
        },
        "sort": [  # 多字段排序
            # _score可以直接用于聚合排序，_id目前也支持，但是在未来的版本也会禁止
            # {"_score": "desc"},
            # {"tap": "desc"},
            {"tag.keyword": "desc"}
        ]
    }))

    # 分页
    print(indices.CONTENT.search_data_by_post({
        # es默认最多只能查询10000条数据，修改方式如下：
        # 1、修改全部索引设置
        # preserve_existing=true只对已存在的索引设置
        # preserve_existing=false所有的索引都引用改设置，新增的也是
        # PUT _all/_settings?preserve_existing=true'
        # {
        #   "index.max_result_window" : "10000000"
        # }
        # 2、修改单个索引设置
        # PUT index1/_settings?preserve_existing=true'
        # {
        #   "index.max_result_window" : "10000000"
        # }

        # es默认返回total最大值为10000，修改如下如下：
        # GET index1/_search
        # {
        #     "track_total_hits": 1000000,
        #     "query": {}
        # }

        "size": 10,  # 应该显示的数量
        "from": 10,  # 跳过的数量 基于排序
        "sort": {
            "tap": "desc"
        },
        "query": {
            "match": {"tag": "tag"}
        }
    }))
