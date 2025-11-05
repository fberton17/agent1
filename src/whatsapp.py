import httpx
from .config import WA_ACCESS_TOKEN, WA_PHONE_NUMBER_ID

WA_BASE = "https://graph.facebook.com/v20.0"

async def send_whatsapp_text(to_phone: str, text: str):
    """
    Envía un mensaje de texto por WhatsApp Cloud API.
    
    Args:
        to_phone: número de teléfono (sin +, ej: "59891234567")
        text: mensaje a enviar (se trunca a 4000 caracteres)
    
    Returns:
        dict: respuesta JSON de la API de WhatsApp
        
    Raises:
        ValueError: si faltan credenciales de configuración
        httpx.HTTPStatusError: si la API retorna un error HTTP
    """
    # Validar configuración
    if not WA_ACCESS_TOKEN:
        raise ValueError("WA_ACCESS_TOKEN no está configurado en .env")
    if not WA_PHONE_NUMBER_ID:
        raise ValueError("WA_PHONE_NUMBER_ID no está configurado en .env")
    
    # Validar entrada
    if not to_phone or not text:
        raise ValueError("to_phone y text son requeridos")
    
    url = f"{WA_BASE}/{WA_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WA_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "text",
        "text": {"body": text[:4000]}
    }
    
    async with httpx.AsyncClient(timeout=15) as client:
        try:
            r = await client.post(url, headers=headers, json=payload)
            r.raise_for_status()
            return r.json()
        except httpx.HTTPStatusError as e:
            error_detail = f"Error {e.response.status_code}"
            try:
                error_body = e.response.json()
                error_detail += f": {error_body}"
            except:
                error_detail += f": {e.response.text}"
            print(f"Error enviando WhatsApp a {to_phone}: {error_detail}")
            raise
        except httpx.RequestError as e:
            print(f"Error de conexión enviando WhatsApp a {to_phone}: {e}")
            raise

