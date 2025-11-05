from smolagents import CodeAgent, Tool, tool
from .tools import turn_on_lights, turn_off_lights, set_brightness, get_light_state
from .config import DEFAULT_AREA

SYSTEM_PROMPT = f"""
Eres un agente domótico que controla luces a través de Home Assistant.
Dispones de estas herramientas: turn_on_lights(area, brightness?, color?),
turn_off_lights(area), set_brightness(area, brightness), get_light_state(area).

Reglas:
- El usuario habla en español rioplatense. Interpreta frases como "prendé", "apagá", "subí al 50%", "color azul".
- Si el usuario no especifica área, usa por defecto el área '{DEFAULT_AREA}'.
- brightness es 0-100. Si el usuario dice "al 60%" mapea a brightness=60.
- Colores aceptados: azul, rojo, verde, blanco/blanca, cálida, fría.
- Responde corto, confirma la acción realizada.
- Si no entiendes, pide una aclaración concreta, pero intentá resolver con supuestos razonables.
"""

TOOLS = [turn_on_lights, turn_off_lights, set_brightness, get_light_state]

def build_agent(llm="openai/gpt-4o-mini"):
    """
    llm: puedes cambiar al modelo que prefieras compatible con smolagents.
    Requiere variables de entorno del proveedor (p. ej., OPENAI_API_KEY).
    """
    agent = CodeAgent(
        tools=TOOLS,
        system_prompt=SYSTEM_PROMPT,
        model=llm,
        # temperature 0.2 para ser más determinista con comandos domóticos
        temperature=0.2,
        max_steps=4,  # como mucho 4 llamadas a herramientas
    )
    return agent

