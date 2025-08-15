import uvicorn
import os

if __name__ == "__main__":
    # Get port from environment variable or default to 8001
    port = int(os.getenv("PORT", 8001))
    
    # Run the uvicorn server
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
