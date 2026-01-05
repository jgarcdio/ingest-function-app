import json

import azure.functions as func
from pydantic import ValidationError

from logger.logging import configure_logging
from models.enqueue import EnqueueReq, EnqueueResp
from services.enqueue_service import enqueue_app

logger = configure_logging()

app = func.FunctionApp()

@app.route(route="enqueue", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
def enqueue_function(req: func.HttpRequest) -> func.HttpResponse:
    logger.info("Solicitud recibida en /enqueue")

    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({"detail": "JSON inválido"}),
            mimetype="application/json",
            status_code=400,
        )

    try:
        enqueue_req = EnqueueReq(**body)
    except ValidationError as ex:
        return func.HttpResponse(
            ex.json(),
            mimetype="application/json",
            status_code=422,
        )

    try:
        payload = enqueue_app(enqueue_req.app)
        resp = EnqueueResp(status="queued", payload=payload)

        return func.HttpResponse(
            resp.model_dump_json(),
            mimetype="application/json",
            status_code=200,
        )

    except ValueError as ex:
        return func.HttpResponse(
            json.dumps({"detail": str(ex)}),
            mimetype="application/json",
            status_code=400,
        )

    except Exception as ex:
        logger.error(f"Error inesperado: {ex}")
        return func.HttpResponse(
            json.dumps({"detail": "Error interno del servidor"}),
            mimetype="application/json",
            status_code=500,
        )
