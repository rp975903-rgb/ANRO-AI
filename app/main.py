from fastapi import FastAPI


from app.api.routes_documents import (
    router as documents_router
)


from app.api.routes_search import (
    router as search_router
)


from app.api.routes_rag import (
    router as rag_router
)


from app.api.routes_auth import (
    router as auth_router
)


# ============================================================
# CREATE FASTAPI APPLICATION
# ============================================================

app = FastAPI(

    title="ANRO AI",

    description=(

        "ANRO AI is an intelligent "

        "document intelligence and "

        "Retrieval-Augmented Generation "

        "platform."

    ),

    version="1.0.0"

)


# ============================================================
# REGISTER AUTHENTICATION ROUTES
# ============================================================

app.include_router(

    auth_router

)


# ============================================================
# REGISTER DOCUMENT ROUTES
# ============================================================

app.include_router(

    documents_router

)


# ============================================================
# REGISTER SEARCH ROUTES
# ============================================================

app.include_router(

    search_router

)


# ============================================================
# REGISTER RAG ROUTES
# ============================================================

app.include_router(

    rag_router

)


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {

        "success":

            True,

        "name":

            "ANRO AI",

        "version":

            "1.0.0",

        "status":

            "running",

        "message":

            "ANRO AI API is running successfully."

    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():

    return {

        "success":

            True,

        "status":

            "healthy",

        "service":

            "ANRO AI"

    }


# ============================================================
# API INFORMATION
# ============================================================

@app.get("/api")
def api_information():

    return {

        "success":

            True,

        "application":

            "ANRO AI",

        "version":

            "1.0.0",

        "modules": {

            "authentication":

                "/api/auth",

            "documents":

                "/api/documents",

            "search":

                "/api/search",

            "rag":

                "/api/rag"

        },

        "documentation":

            "/docs",

        "health":

            "/health"

    }


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    import uvicorn


    uvicorn.run(

        "app.main:app",

        host="127.0.0.1",

        port=8000,

        reload=True

    )