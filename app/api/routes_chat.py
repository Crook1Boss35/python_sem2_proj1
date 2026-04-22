from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import get_chat_usecase, get_current_user_id
from app.core.errors import ExternalServiceError
from app.schemas.chat import ChatMessagePublic, ChatRequest, ChatResponse
from app.usecases.chat import ChatUseCase

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    user_id: int = Depends(get_current_user_id),
    usecase: ChatUseCase = Depends(get_chat_usecase),
) -> ChatResponse:
    try:
        answer = await usecase.ask(
            user_id=user_id,
            prompt=payload.prompt,
            system=payload.system,
            max_history=payload.max_history,
            temperature=payload.temperature,
        )
        return ChatResponse(answer=answer)
    except ExternalServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(e),
        ) from e


@router.get("/history", response_model=list[ChatMessagePublic])
async def get_history(
    limit: int = Query(default=50, ge=1, le=200),
    user_id: int = Depends(get_current_user_id),
    usecase: ChatUseCase = Depends(get_chat_usecase),
) -> list[ChatMessagePublic]:
    messages = await usecase.get_history(user_id=user_id, limit=limit)
    return [ChatMessagePublic.model_validate(message) for message in messages]


@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
async def clear_history(
    user_id: int = Depends(get_current_user_id),
    usecase: ChatUseCase = Depends(get_chat_usecase),
) -> None:
    await usecase.clear_history(user_id=user_id)
