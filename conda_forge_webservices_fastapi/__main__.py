if __name__ == "__main__":
    import os

    import uvicorn

    uvicorn.run(
        "conda_forge_webservices_fastapi.webapp:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
    )
