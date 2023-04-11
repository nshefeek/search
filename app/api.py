from fastapi import APIRouter, Depends, HTTPException, Query

from elasticsearch import Elasticsearch

from app import config

router = APIRouter()

def get_es_client():
    """Get the dependency for ES client."""
    es_client = Elasticsearch(
        config.ELASTICSEARCH_HOST,
        http_auth=(config.ELASTICSEARCH_USER, config.ELASTICSEARCH_PASSWORD),
    )

    try:
        yield es_client
    finally:
        es_client.close()


@router.get('/search')
async def search(
    query: str = Query(alias="q"),
    es_client: Elasticsearch = Depends(get_es_client)
):
    if len(query.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail="Please provide a valid query",
        )
    
    search_query = {
        "query": {"multi_match": {
            "query": query,
            "type": "most_fields",
            "operator": "and",
            "fields": [
                "title^3",
                "title.ngrams",
                "keywords^2",
                "keywords.ngrams",
                "is_organic"
            ],
        }
    }
    }
    
    results = es_client.search(
        index="product",
        body=search_query,
        size=1000
    )
    return results
