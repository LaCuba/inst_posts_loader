import json


async def safe_sse(generator):
    try:
        async for event in generator:
            yield event
    except Exception as e:
        yield f"{{event: error,\ndata: {json.dumps({'error': str(e)})}\n\n}}"
