def exact_match(collection, keywords: list[str], restrictions: list[dict] = None):
    '''
    Find all articles whose title or abstract contains at least one of the keywords.
    '''
    find_expression = {
        "$or": [
            {"title": {"$regex": f".*{'|'.join(keywords)}.*", "$options": "i"}},
            {"abstract": {"$regex": f".*{'|'.join(keywords)}.*", "$options": "i"}}
        ]
    }
    if restrictions is not None:
        find_expression = {"$and": [*restrictions, find_expression]}
    return list(collection.find(find_expression))