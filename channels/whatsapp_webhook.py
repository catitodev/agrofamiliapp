from flask import Flask, request, jsonify
import os
import hmac
import hashlib
import httpx

app = Flask(__name__)

TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_WEBHOOK_AUTH = os.getenv("TWILIO_WEBHOOK_AUTH", "")


def validate_twilio_request(request):
    if TWILIO_AUTH_TOKEN:
        auth_header = request.headers.get("Authorization", "")
        expected = f"Basic {TWILIO_AUTH_TOKEN}"
        return auth_header == expected
    return True


@app.route("/webhook/whatsapp", methods=["POST"])
def whatsapp_webhook():
    if not validate_twilio_request(request):
        return "Unauthorized", 401

    from_number = request.form.get("From", "")
    body = request.form.get("Body", "")

    user_id = from_number.replace("whatsapp:", "")

    try:
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(
            httpx.AsyncClient().post(
                "http://backend:8000/chat",
                json={"text": body, "user_id": user_id},
                timeout=30
            )
        )
        data = response.json()
        reply = data.get("response", "Desculpe, erro de conexão.")
    except Exception:
        reply = "Erro ao processar mensagem. Tente novamente."

    from flask import make_response
    resp = make_response(f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply}</Message>
</Response>""")
    resp.headers["Content-Type"] = "text/xml"
    return resp


@app.route("/webhook/twilio/status", methods=["POST"])
def twilio_status():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)