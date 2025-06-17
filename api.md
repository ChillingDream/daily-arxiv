用户相关

URL: ```/users```
Method: ```GET```
```python
Response: {
    "usernames": list[str]
}
```

关键词匹配查询

URL: ```/query```  
Method: ```POST```
```python
Request: {
    "query": list[str],
    "start_time": int (timestamp),
    "end_time": int (timestamp),
    "start_index": int,
    "end_index": int (inclusive)
}
Response: {
    "articles": [{
        "arxiv_id": str,
        "added_time": int(timestamp),
        "submitted_time": int(timestamp),
        "title": str,
        "abstract": str,
        "authors": list[str],
    }]
}
```

用户关键词获取

URL: ```/keywords```  
Method: ```GET```
```python
Request: {
    "username": str
}
Response: {
    "keywords": list[str]
}
```

用户关键词设置  
URL: ```/keywords```  
Method: ```POST```
```python
Request: {
    "username": str,
    "keywords": list[str]
}
Response: {
    "success": bool
}
```

用户已读论文获取  
URL: ```/users/read_papers```  
Method: ```GET```
```python
Request: {
    "username": str,
}
Response: {
    "arxiv_ids": list[str]
}
```

用户已读论文设置  
URL: ```/users/read_papers```  
Method: ```POST```
```python
Request: {
    "username": str,
    "arxiv_ids": list[str]
}
Response: {
    "success": bool
}
```

用户收藏论文获取  
URL: ```/users/favorite_papers```  
Method: ```GET```
```python
Request: {
    "username": str,
}
Response: {
    "arxiv_ids": list[str]
}
```

用户收藏论文设置  
URL: ```/users/favorite_papers```  
Method: ```POST```
```python
Request: {
    "username": str,
    "arxiv_ids": list[str]
}
Response: {
    "success": bool
}
```

论文分析
URL: ```/analysis```
Method: ```POST```
```python
Request: {
    "arxiv_id": str,
    "section": str
}
Response: {
    "analysis": str
}