import httpx
from .config import HA_BASE_URL, HA_TOKEN, HA_TIMEOUT_MS

class HAClient:
    def __init__(self):
        # Validar configuración al inicializar
        if not HA_BASE_URL:
            raise ValueError("HA_BASE_URL no está configurado en .env")
        if not HA_TOKEN:
            raise ValueError("HA_TOKEN no está configurado en .env")
        
        self._headers = {
            "Authorization": f"Bearer {HA_TOKEN}",
            "Content-Type": "application/json"
        }
        self._timeout = HA_TIMEOUT_MS / 1000.0
        self._base_url = HA_BASE_URL.rstrip("/")

    async def call_service(self, domain: str, service: str, data: dict):
        """Llama a un servicio de Home Assistant."""
        url = f"{self._base_url}/api/services/{domain}/{service}"
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            try:
                r = await client.post(url, headers=self._headers, json=data)
                r.raise_for_status()
                return r.json()
            except httpx.HTTPStatusError as e:
                error_msg = f"Error {e.response.status_code}"
                try:
                    error_body = e.response.json()
                    error_msg += f": {error_body}"
                except:
                    error_msg += f": {e.response.text}"
                print(f"Error llamando servicio {domain}.{service}: {error_msg}")
                raise
            except httpx.RequestError as e:
                print(f"Error de conexión con Home Assistant: {e}")
                raise

    async def get_state(self, entity_id: str):
        """Obtiene el estado de una entidad de Home Assistant."""
        url = f"{self._base_url}/api/states/{entity_id}"
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            try:
                r = await client.get(url, headers=self._headers)
                r.raise_for_status()
                return r.json()
            except httpx.HTTPStatusError as e:
                error_msg = f"Error {e.response.status_code}"
                try:
                    error_body = e.response.json()
                    error_msg += f": {error_body}"
                except:
                    error_msg += f": {e.response.text}"
                print(f"Error obteniendo estado de {entity_id}: {error_msg}")
                raise
            except httpx.RequestError as e:
                print(f"Error de conexión con Home Assistant: {e}")
                raise

