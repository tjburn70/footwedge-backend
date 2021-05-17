from typing import Dict, List

import elasticsearch
from fastapi import HTTPException

from constants import QueryType


def search_query_factory(query_type: QueryType, fields: List[str], text: str) -> Dict:
    if query_type == QueryType.MATCH:
        field = fields[0]
        return {
            query_type: {
                field: {'query': text}
            }
        }
    elif query_type == QueryType.MULTI_MATCH:
        return {
            query_type: {
                'query': text,
                'fields': fields or ['*'],
            }
        }
    elif query_type == QueryType.WILDCARD:
        field = fields[0]
        return {
            query_type: {
                field: {
                    "value": f"{text}*",
                    "boost": 1.0,
                    "rewrite": "constant_score"
                }
            }
        }


class SearchService:

    def __init__(self, es_client: elasticsearch.Elasticsearch):
        self.es_client = es_client

    def get_indices(self):
        results = self.es_client.cat.indices()
        return results

    def create_index(self, index: str, body: dict = None):
        try:
            resp = self.es_client.indices.create(
                index=index,
                body=body,
            )
            return resp
        except elasticsearch.exceptions.RequestError as req_exc:
            raise HTTPException(status_code=400, detail=req_exc.info)

    def delete_index(self, index: str):
        try:
            resp = self.es_client.indices.delete(
                index=index,
            )
            return resp
        except elasticsearch.exceptions.NotFoundError as exc:
            raise HTTPException(status_code=404, detail=exc.info)

    def full_text_search(self, index: str, query_type: QueryType, text: str, fields: List[str]):
        query = search_query_factory(
            query_type=query_type,
            fields=fields,
            text=text,
        )
        results = self.es_client.search(
            index=index,
            body={"query": query}
        )
        return results["hits"]

    def get_document(self, index: str, document_id: str):
        try:
            return self.es_client.get(index=index, id=document_id)
        except elasticsearch.exceptions.NotFoundError as exc:
            raise HTTPException(status_code=404, detail=exc.info)

    def get_all_documents(self, index: str):
        body = {"query": {"match_all": {}}}
        results = self.es_client.search(body=body, index=index)
        return results.get('hits')

    def add_document(self, index: str, payload: dict, document_id: str):
        if not self.es_client.indices.exists(index=index):
            error_message = f"Index: '{index}' not found"
            raise HTTPException(status_code=404, detail=error_message)
        if self.es_client.exists(index=index, id=document_id):
            error_message = f"The document with id: {document_id} already exists in the index: {index}"
            raise HTTPException(status_code=409, detail=error_message)

        return self.es_client.index(index=index, id=document_id, body=payload)

    def add_to_nested_property(self, index: str, document_id: str, nested_property: str, nested_property_body: dict):
        nested_property_singular = nested_property.rstrip("s")
        script = f"ctx._source.{nested_property}.add(params.{nested_property_singular})"
        body = {
            "script": {
                "source": script,
                "params": {
                    nested_property_singular: nested_property_body
                }
            }
        }
        return self.es_client.update(
            index=index,
            id=document_id,
            body=body
        )

    def delete_document(self, index: str, document_id: str):
        return self.es_client.delete(
            index=index,
            id=document_id,
        )
