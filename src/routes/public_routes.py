from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, responses, Depends

from src.core.containers import Container
from src.services.orchestration.shortened_url.url_retrieval_abstract import AbstractUrlRetrievalOrchestrator

router = APIRouter(
    tags=['public_routes'],
)

@router.get("/{short_code}")
@inject
async def get_long_url(short_code: str,
                       url_retrieval_orchestrator: AbstractUrlRetrievalOrchestrator \
                               = Depends(Provide[Container.url_retrieval_orchestrator]),
                       ):
    long_url = await url_retrieval_orchestrator.retrieve_url(short_code)
    return responses.RedirectResponse(long_url)
