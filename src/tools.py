from typing import List, Optional, Tuple
from smolagents import tool
from .ha_client import HAClient
from .mapping import get_entities_for_area, COLOR_MAP

ha = HAClient()

def _validate_area(area: str) -> Tuple[bool, str]:
    """
    Valida que el área tenga luces mapeadas.
    Retorna (is_valid, error_message)
    """
    entities = get_entities_for_area(area)
    if not entities:
        return False, f"No hay luces mapeadas para el área '{area}'."
    return True, ""

@tool
async def turn_on_lights(area: str, brightness: Optional[int] = None, color: Optional[str] = None) -> str:
    """
    Enciende luces en un área. brightness es 0-100 (se escala a 0-255).
    color admite: 'azul','rojo','verde','blanco/blanca','cálida','fría', etc.
    """
    is_valid, error_msg = _validate_area(area)
    if not is_valid:
        return error_msg
    
    entities = get_entities_for_area(area)
    data = {"entity_id": entities}
    if brightness is not None:
        data["brightness_pct"] = max(0, min(100, int(brightness)))
    if color:
        cm = COLOR_MAP.get(color.lower())
        if cm:
            data.update(cm)
    
    try:
        await ha.call_service("light", "turn_on", data)
        desc = f"Luces encendidas en {area}"
        if brightness is not None:
            desc += f" al {data['brightness_pct']}%"
        if color:
            desc += f" color {color}"
        return desc
    except Exception as e:
        return f"Error encendiendo luces en {area}: {str(e)}"

@tool
async def turn_off_lights(area: str) -> str:
    """
    Apaga luces en un área.
    """
    is_valid, error_msg = _validate_area(area)
    if not is_valid:
        return error_msg
    
    entities = get_entities_for_area(area)
    try:
        await ha.call_service("light", "turn_off", {"entity_id": entities})
        return f"Luces apagadas en {area}"
    except Exception as e:
        return f"Error apagando luces en {area}: {str(e)}"

@tool
async def get_light_state(area: str) -> str:
    """
    Devuelve estado resumido de las luces de un área.
    """
    is_valid, error_msg = _validate_area(area)
    if not is_valid:
        return error_msg
    
    entities = get_entities_for_area(area)
    states = []
    try:
        for e in entities:
            st = await ha.get_state(e)
            states.append(f"{e} => {st.get('state')}")
        return "; ".join(states)
    except Exception as e:
        return f"Error obteniendo estado de luces en {area}: {str(e)}"

@tool
async def set_brightness(area: str, brightness: int) -> str:
    """
    Ajusta brillo (0-100) de las luces del área.
    """
    is_valid, error_msg = _validate_area(area)
    if not is_valid:
        return error_msg
    
    entities = get_entities_for_area(area)
    brightness_pct = max(0, min(100, int(brightness)))
    try:
        await ha.call_service("light", "turn_on", {"entity_id": entities, "brightness_pct": brightness_pct})
        return f"Brillo en {area} ajustado a {brightness_pct}%"
    except Exception as e:
        return f"Error ajustando brillo en {area}: {str(e)}"

