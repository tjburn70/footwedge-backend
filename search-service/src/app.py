import os
from typing import List, Optional

from fastapi import FastAPI, Body, Query
from fastapi.middleware.cors import CORSMiddleware
from elasticsearch import Elasticsearch

from service import SearchService
from constants import QueryType


SEARCH_ENGINE_URI = os.environ.get('SEARCH_ENGINE_URI')
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
es_client = Elasticsearch(hosts=[SEARCH_ENGINE_URI])


@app.get('/health')
async def health():
    return "Welcome to Search Service"


@app.get('/indices')
async def get_all_indexes():
    return SearchService(es_client=es_client).get_indices()


@app.post('/{index}')
async def create_index(index: str, body: Optional[dict] = Body(None)):
    return SearchService(es_client=es_client).create_index(index=index, body=body)


@app.delete('/{index}')
async def delete_index(index: str):
    return SearchService(es_client=es_client).delete_index(index=index)


@app.get('/{index}')
async def search_index(index: str, q: str, query_type: QueryType, field: List[str] = Query(...)):
    search_service = SearchService(es_client=es_client)
    return search_service.full_text_search(
        index=index,
        query_type=query_type,
        text=q,
        fields=field,
    )


@app.get('/{index}/documents')
async def get_all_documents(index: str):
    return SearchService(es_client=es_client).get_all_documents(index=index)


@app.get('/{index}/documents/{document_id}')
async def get_document(index: str, document_id: str):
    return SearchService(es_client=es_client).get_document(index=index, document_id=document_id)


@app.put('/{index}/documents')
async def add_document(index: str, payload: dict = Body(..., embed=True), _id: str = Body(..., embed=True)):
    search_service = SearchService(es_client=es_client)
    return search_service.add_document(
        index=index,
        payload=payload,
        document_id=_id,
    )


@app.put('/{index}/documents/{document_id}/add/{nested_property}')
async def update_doc_nested_property(
        index: str,
        document_id: str,
        nested_property: str,
        payload: dict = Body(...)
):
    search_service = SearchService(es_client=es_client)
    return search_service.add_to_nested_property(
        index=index,
        document_id=document_id,
        nested_property=nested_property,
        nested_property_body=payload,
    )


@app.delete('/{index}/documents/{document_id}')
async def delete_document(index: str, document_id: str):
    return SearchService(es_client=es_client).delete_document(index=index, document_id=document_id)
