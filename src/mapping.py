from typing import List, Optional, Dict

# Mapeo MVP: área → lista de entity_ids (luego puedes auto-descubrir desde HA)
AREA_MAP: Dict[str, List[str]] = {
    "living": ["light.living_ceiling", "light.living_lamp"],
    "dormitorio": ["light.bedroom_ceiling"],
    "cocina": ["light.kitchen"]
}

# Alias/variantes en español rioplatense
AREA_ALIASES = {
    "living": ["living", "estar", "sala"],
    "dormitorio": ["dormitorio", "cuarto", "pieza", "habitación", "habitacion"],
    "cocina": ["cocina", "kitchen"]
}

COLOR_MAP = {
    "blanco": {"color_temp_kelvin": 4000},
    "blanca": {"color_temp_kelvin": 4000},
    "cálida": {"color_temp_kelvin": 2700},
    "calida": {"color_temp_kelvin": 2700},
    "fría": {"color_temp_kelvin": 5000},
    "fria": {"color_temp_kelvin": 5000},
    "azul": {"rgb_color": [0, 0, 255]},
    "rojo": {"rgb_color": [255, 0, 0]},
    "verde": {"rgb_color": [0, 255, 0]},
}

def normalize_area(text: str) -> Optional[str]:
    """
    Normaliza un texto a un área canónica usando los alias.
    Retorna el nombre canónico del área o None si no se encuentra.
    """
    if not text:
        return None
    
    t = text.lower().strip()
    
    # Primero verificar si ya es un área canónica
    if t in AREA_MAP:
        return t
    
    # Buscar en los alias
    for canonical, variants in AREA_ALIASES.items():
        if t == canonical or any(v == t for v in variants):
            return canonical
    
    return None

def get_entities_for_area(area: str) -> List[str]:
    return AREA_MAP.get(area, [])

