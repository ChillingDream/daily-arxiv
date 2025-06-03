def exact_match(collection, keywords: list[str], restrictions: list[dict] = None):
    """
    Find all articles whose title or abstract contains at least one of the keywords.
    Phrase-level exact match.
    """
    find_expression = {
        "$text": {
            "$search": " ".join(['"' + x + '"' for x in keywords]),
            "$caseSensitive": False,
            "$diacriticSensitive": False
        }
    }

    if restrictions is not None:
        find_expression = {"$and": [*restrictions, find_expression]}
    return list(collection.find(find_expression))
