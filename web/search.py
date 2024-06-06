# from fastapi import APIRouter
# from service import search as search 
# from model.resource import Resource
# from model.airesults import AIResults

# router = APIRouter(prefix="/search")


# @router.get("/{query}")
# def get_search(query) -> list[Resource]:
#     return search.get_query(query)


# @router.get("/summary/{query}")
# def get_query_summary(query) -> AIResults:
#     return search.get_query_summary(query)


# @router.get("/qa/{query}")
# def get_query_qa(query) -> AIResults:
#     return search.get_qa_from_query(query)
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from service import search as search 
from model.resource import Resource
from model.airesults import AIResults

router = APIRouter(prefix="/search")

def get_search(query) -> list[Resource]:
    return search.get_query(query)
def get_query_summary(query) -> AIResults:
    return search.get_query_summary(query)
def get_query_qa(query) -> AIResults:
    return search.get_qa_from_query(query)

@router.websocket("/ws/{query}")
async def websocket_search(websocket: WebSocket, query: str):
    await websocket.accept()
    try:
        results = search.get_query(query)
        await websocket.send_json([result.dict() for result in results])
    except Exception as e:
        await websocket.send_json({"error": str(e)})
    finally:
        await websocket.close()


@router.websocket("/ws/summary/{query}")
async def websocket_query_summary(websocket: WebSocket, query: str):
    await websocket.accept()
    
    try:
        result = search.get_query_summary(query)
        await websocket.send_json(result.dict())
    except Exception as e:
        await websocket.send_json({"error": str(e)})
    finally:
        await websocket.close()


@router.websocket("/ws/qa/{query}")
async def websocket_query_qa(websocket: WebSocket, query: str):
    await websocket.accept()
    try:
        result = search.get_qa_from_query(query)
        await websocket.send_json(result.dict())
    except Exception as e:
        await websocket.send_json({"error": str(e)})
    finally:
        await websocket.close()
