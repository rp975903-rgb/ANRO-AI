
import subprocess
import sys
import time
import webbrowser
import requests
from pathlib import Path




# ============================================================
# ANRO - UNIFIED APPLICATION LAUNCHER
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

BACKEND_URL = "http://127.0.0.1:8000"
FRONTEND_URL = "http://localhost:8501"

backend_process = None
frontend_process = None


# ============================================================
# CHECK BACKEND
# ============================================================

def check_backend():

    try:

        response = requests.get(
            f"{BACKEND_URL}/health",
            timeout=2,
        )

        return response.status_code == 200

    except requests.RequestException:

        return False


# ============================================================
# MAIN
# ============================================================

def main():

    global backend_process
    global frontend_process


    print()
    print("=" * 60)
    print("🧠 ANRO")
    print("🚀 Starting Application...")
    print("=" * 60)
    print()


    # ========================================================
    # FRONTEND FILE
    # ========================================================

    frontend_file = (
        PROJECT_ROOT
        / "frontend"
        / "streamlit_app.py"
    )


    if not frontend_file.exists():

        print(
            "❌ ERROR: Streamlit frontend file not found."
        )

        print(
            frontend_file
        )

        return


    # ========================================================
    # START FASTAPI BACKEND
    # ========================================================

    print(
        "🔄 Starting FastAPI Backend..."
    )


    backend_process = subprocess.Popen(

        [

            sys.executable,

            "-m",

            "uvicorn",

            "app.main:app",

            "--host",

            "127.0.0.1",

            "--port",

            "8000",

        ],

        cwd=str(PROJECT_ROOT),

    )


    print(
        "✅ FastAPI process started."
    )


    # ========================================================
    # WAIT FOR BACKEND
    # ========================================================

    print(
        "⏳ Waiting for Backend..."
    )


    backend_ready = False


    for _ in range(20):

        time.sleep(1)


        if check_backend():

            backend_ready = True

            break


    if backend_ready:

        print()
        print(
            "🟢 FastAPI Backend is ONLINE"
        )

        print(
            f"🌐 Backend: {BACKEND_URL}"
        )

        print(
            f"📚 Swagger: {BACKEND_URL}/docs"
        )


    else:

        print()
        print(
            "🔴 WARNING: Backend health check failed."
        )

        print(
            "The backend process may have an error."
        )


    # ========================================================
    # START STREAMLIT FRONTEND
    # ========================================================

    print()
    print(
        "🔄 Starting Streamlit Frontend..."
    )


    frontend_process = subprocess.Popen(

        [

            sys.executable,

            "-m",

            "streamlit",

            "run",

            str(frontend_file),

            "--server.port",

            "8501",

            "--server.address",

            "localhost",

        ],

        cwd=str(PROJECT_ROOT),

    )


    print(
        "✅ Streamlit Frontend started."
    )

    print(
        f"🖥️ Frontend: {FRONTEND_URL}"
    )


    # ========================================================
    # WAIT FOR STREAMLIT
    # ========================================================

    time.sleep(5)


    # ========================================================
    # OPEN BROWSER ONLY ONCE
    # ========================================================

    print()
    print(
        "🌐 Opening ANRO..."
    )


    webbrowser.open_new(
        FRONTEND_URL
    )


    # ========================================================
    # FINAL STATUS
    # ========================================================

    print()
    print("=" * 60)
    print("🎉 ANRO IS RUNNING!")
    print("=" * 60)
    print()
    print(
        f"🚀 Backend  : {BACKEND_URL}"
    )
    print(
        f"📚 Swagger  : {BACKEND_URL}/docs"
    )
    print(
        f"🖥️ Frontend : {FRONTEND_URL}"
    )
    print()
    print(
        "💡 Press CTRL+C to stop everything."
    )
    print("=" * 60)


    # ========================================================
    # KEEP APPLICATION RUNNING
    # ========================================================

    try:

        while True:

            # Check if backend crashed

            if (
                backend_process
                and backend_process.poll()
                is not None
            ):

                print()
                print(
                    "🔴 Backend process stopped."
                )

                break


            # Check if frontend crashed

            if (
                frontend_process
                and frontend_process.poll()
                is not None
            ):

                print()
                print(
                    "🔴 Frontend process stopped."
                )

                break


            time.sleep(2)


    except KeyboardInterrupt:

        print()
        print(
            "🛑 Shutting down ANRO..."
        )


    finally:

        # ====================================================
        # STOP FRONTEND
        # ====================================================

        if (
            frontend_process
            and frontend_process.poll()
            is None
        ):

            frontend_process.terminate()


        # ====================================================
        # STOP BACKEND
        # ====================================================

        if (
            backend_process
            and backend_process.poll()
            is None
        ):

            backend_process.terminate()


        print(
            "✅ Frontend stopped."
        )

        print(
            "✅ Backend stopped."
        )

        print(
            "👋 ANRO shutdown complete."
        )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()

