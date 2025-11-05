"""
Vercel serverless function handler for WhatsApp → HA Agent.
"""
from mangum import Mangum
from src.app import app as fastapi_app

# Create Mangum handler for Vercel serverless functions
# Mangum wraps FastAPI app to work with AWS Lambda/Vercel runtime
mangum_handler = Mangum(fastapi_app, lifespan="off")

# Export handler for Vercel
# Vercel's Python runtime expects a handler function that receives (event, context)
def handler(event, context):
    """
    Handler function for Vercel serverless functions.
    This is the entry point that Vercel calls.
    
    Args:
        event: The event object containing request data
        context: The context object (not used but required by Vercel)
    
    Returns:
        Response from the FastAPI app
    """
    return mangum_handler(event, context)

# Vercel also checks for 'app' function, so export it as well
app = handler
