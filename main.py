import uvicorn

def main():
    host = "127.0.0.1"
    port = 8000
    
    print(f"OpenAPI docs: http://{host}:{port}/docs")
    print(f"OpenAPI redoc: http://{host}:{port}/admin")
    
    uvicorn.run("app.app:app", host="127.0.0.1", port=8000, log_level="info", reload=True)

if __name__ == "__main__":
    main()