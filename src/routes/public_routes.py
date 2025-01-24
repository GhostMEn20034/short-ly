from typing import Annotated
from fastapi import APIRouter, responses, Depends, status

from src.dependencies.orchestration_services.url_retrieval_orchestrator import get_url_retrieval_orchestrator
from src.services.orchestration.shortened_url.url_retrieval_abstract import AbstractUrlRetrievalOrchestrator


router = APIRouter(
    tags=['public_routes'],
)


@router.get("/{short_code}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def get_long_url(short_code: str,
                       url_retrieval_orchestrator: Annotated[
                           AbstractUrlRetrievalOrchestrator, Depends(get_url_retrieval_orchestrator)],
                       ):
    long_url, cache_status = await url_retrieval_orchestrator.retrieve_url(short_code)

    return responses.RedirectResponse(long_url, headers={"X-Cache-Status": cache_status})
