import uvicorn
import os


def main():
    host = "127.0.0.1"
    port = 8000

    print(f"OpenAPI docs: https://{host}:{port}/docs")
    print(f"OpenAPI redoc: https://{host}:{port}/admin")
    
    

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    uvicorn.run(
        "app.app:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True,
        ssl_certfile=os.path.join(BASE_DIR, "certs/api.local.stats.pem"),
        ssl_keyfile=os.path.join(BASE_DIR, "certs/api.local.stats-key.pem"),
    )
if __name__ == "__main__":
    main()
