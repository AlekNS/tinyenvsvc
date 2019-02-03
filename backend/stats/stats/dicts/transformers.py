# -*- coding: utf-8 -*-
def transform_dictionary_response(rows):
    for row in rows:
        yield {'name': row['name']}
