import streamlit as st
import requests


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ANRO AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# BACKEND CONFIGURATION
# ============================================================

BACKEND_URL = "http://127.0.0.1:8000"


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "access_token" not in st.session_state:

    st.session_state.access_token = None


if "user" not in st.session_state:

    st.session_state.user = None


if "current_document_id" not in st.session_state:

    st.session_state.current_document_id = None


if "current_document_name" not in st.session_state:

    st.session_state.current_document_name = None


if "chat_history" not in st.session_state:

    st.session_state.chat_history = []


# ============================================================
# AUTHENTICATION HELPERS
# ============================================================

def get_auth_headers():

    token = st.session_state.get(
        "access_token"
    )

    if not token:

        return {}

    return {

        "Authorization":
            f"Bearer {token}"

    }


def logout_user():

    st.session_state.access_token = None

    st.session_state.user = None

    st.session_state.current_document_id = None

    st.session_state.current_document_name = None

    st.session_state.chat_history = []

    st.rerun()


# ============================================================
# BACKEND HEALTH CHECK
# ============================================================

def check_backend():

    try:

        response = requests.get(
            f"{BACKEND_URL}/health",
            timeout=5,
        )

        return response.status_code == 200

    except requests.RequestException:

        return False


# ============================================================
# API GET HELPER
# ============================================================

def api_get(
    endpoint,
    authenticated=False,
):

    try:

        headers = (
            get_auth_headers()
            if authenticated
            else {}
        )

        response = requests.get(

            f"{BACKEND_URL}{endpoint}",

            headers=headers,

            timeout=30,

        )

        return response


    except requests.RequestException as error:

        st.error(
            f"Backend connection error: {error}"
        )

        return None


# ============================================================
# API ERROR HELPER
# ============================================================

def show_api_error(response):

    try:

        error_data = response.json()

        st.error(
            f"Request failed: "
            f"{response.status_code}"
        )

        st.json(
            error_data
        )

    except Exception:

        st.error(

            f"Request failed with status "
            f"code {response.status_code}."

        )


# ============================================================
# LOGIN / REGISTER SCREEN
# ============================================================

if not st.session_state.access_token:

    st.title(
        "🧠 Welcome to ANRO AI"
    )

    st.write(
        "Intelligent Document Intelligence & RAG Platform"
    )

    st.divider()


    tab_login, tab_register = st.tabs(

        [
            "🔐 Login",
            "📝 Register",
        ]

    )


    # ========================================================
    # LOGIN
    # ========================================================

    with tab_login:

        st.subheader(
            "🔐 Login to ANRO AI"
        )

        login_email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="login_email",
        )

        login_password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password",
        )


        if st.button(
            "🚀 Login",
            use_container_width=True,
            key="login_button",
        ):

            if not login_email.strip():

                st.warning(
                    "Please enter your email."
                )

            elif not login_password:

                st.warning(
                    "Please enter your password."
                )

            else:

                try:

                    with st.spinner(
                        "Authenticating..."
                    ):

                        response = requests.post(

                            f"{BACKEND_URL}"
                            "/api/auth/login",

                            json={

                                "email":
                                    login_email.strip(),

                                "password":
                                    login_password,

                            },

                            timeout=30,

                        )


                    if response.status_code == 200:

                        data = response.json()


                        st.session_state.access_token = (

                            data.get(
                                "access_token"
                            )

                        )


                        st.session_state.user = (

                            data.get(
                                "user",
                                {}
                            )

                        )


                        if st.session_state.access_token:

                            st.success(
                                "✅ Login successful!"
                            )

                            st.rerun()

                        else:

                            st.error(
                                "Login successful, "
                                "but access token was not returned."
                            )


                    else:

                        show_api_error(
                            response
                        )


                except requests.RequestException as error:

                    st.error(

                        f"Backend connection error: "
                        f"{error}"

                    )


    # ========================================================
    # REGISTER
    # ========================================================

    with tab_register:

        st.subheader(
            "📝 Create ANRO AI Account"
        )

        register_name = st.text_input(
            "Full Name",
            placeholder="Enter your full name",
            key="register_name",
        )

        register_email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="register_email",
        )

        register_password = st.text_input(
            "Password",
            type="password",
            placeholder="Minimum 6 characters",
            key="register_password",
        )


        if st.button(
            "📝 Create Account",
            use_container_width=True,
            key="register_button",
        ):

            if not register_name.strip():

                st.warning(
                    "Please enter your full name."
                )

            elif not register_email.strip():

                st.warning(
                    "Please enter your email."
                )

            elif len(register_password) < 6:

                st.warning(
                    "Password must contain "
                    "at least 6 characters."
                )

            else:

                try:

                    with st.spinner(
                        "Creating account..."
                    ):

                        response = requests.post(

                            f"{BACKEND_URL}"
                            "/api/auth/register",

                            json={

                                "full_name":
                                    register_name.strip(),

                                "email":
                                    register_email.strip(),

                                "password":
                                    register_password,

                            },

                            timeout=30,

                        )


                    if response.status_code == 201:

                        st.success(

                            "✅ Account created successfully! "
                            "Please login."

                        )


                    else:

                        show_api_error(
                            response
                        )


                except requests.RequestException as error:

                    st.error(

                        f"Backend connection error: "
                        f"{error}"

                    )


    st.stop()


# ============================================================
# LOGGED-IN USER
# ============================================================

current_user = st.session_state.get(
    "user",
    {}
)

user_name = current_user.get(
    "full_name",
    "User",
)

user_email = current_user.get(
    "email",
    "",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #888888;
        margin-bottom: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title(
        "🧠 ANRO AI"
    )

    st.success(
        f"👤 Welcome, {user_name}"
    )

    st.caption(
        user_email
    )

    st.caption(
        "Intelligent Document Intelligence Platform"
    )

    st.divider()


    # ========================================================
    # NAVIGATION
    # ========================================================

    page = st.radio(

        "Navigation",

        [

            "📊 Dashboard",

            "📄 Documents",

            "🔎 Semantic Search",

            "🤖 Ask ANRO AI",

            "💬 Conversation",

        ],

    )


    st.divider()


    # ========================================================
    # ACTIVE DOCUMENT
    # ========================================================

    st.subheader(
        "📄 Active Document"
    )


    if st.session_state.current_document_id:

        st.success(
            "Document Ready"
        )

        if st.session_state.current_document_name:

            st.caption(

                f"📌 "
                f"{st.session_state.current_document_name}"

            )

        st.code(

            st.session_state.current_document_id,

            language="text",

        )

    else:

        st.warning(
            "No document selected."
        )

        st.caption(
            "Please ingest a document first."
        )


    st.divider()


    # ========================================================
    # LOGOUT
    # ========================================================

    if st.button(

        "🚪 Logout",

        use_container_width=True,

    ):

        logout_user()


    st.divider()

    st.caption(
        "ANRO AI v1.0.0"
    )

    st.caption(
        "FastAPI + JWT + RAG + ChromaDB + Ollama"
    )


# ============================================================
# DASHBOARD
# ============================================================

if page == "📊 Dashboard":

    st.markdown(

        '<div class="main-title">'
        '🧠 ANRO AI'
        '</div>',

        unsafe_allow_html=True,

    )


    st.markdown(

        '<div class="subtitle">'
        'Intelligent Document Intelligence & RAG Platform'
        '</div>',

        unsafe_allow_html=True,

    )


    st.info(

        f"👋 Welcome to ANRO AI, "
        f"**{user_name}**!"

    )


    backend_online = check_backend()


    if backend_online:

        st.success(
            "🟢 ANRO AI Backend is Online"
        )

    else:

        st.error(
            "🔴 ANRO AI Backend is Offline"
        )


    st.divider()


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(

            "Backend",

            "Online"
            if backend_online
            else "Offline",

        )


    with col2:

        response = api_get(
            "/api/search/count"
        )

        if response and response.status_code == 200:

            data = response.json()

            st.metric(

                "Indexed Chunks",

                data.get(
                    "total_chunks",
                    0,
                ),

            )

        else:

            st.metric(
                "Indexed Chunks",
                "N/A",
            )


    with col3:

        response = api_get(

            "/api/documents/"
            "supported-formats"

        )


        if response and response.status_code == 200:

            data = response.json()

            formats = data.get(

                "supported_extensions",

                [],

            )

            st.metric(

                "File Formats",

                len(formats),

            )

            if formats:

                st.caption(

                    f"Supported: "
                    f"{', '.join(formats)}"

                )

        else:

            st.metric(

                "File Formats",

                "N/A",

            )


    with col4:

        response = api_get(
            "/api/rag/status"
        )


        if response and response.status_code == 200:

            data = response.json()

            st.metric(

                "RAG System",

                "Ready",

            )

            st.caption(

                f"Model: "
                f"{data.get('model', 'Unknown')}"

            )

        else:

            st.metric(

                "RAG System",

                "N/A",

            )


    st.divider()


    st.subheader(
        "🚀 ANRO AI System"
    )


    st.write(

        """
        ANRO AI is an intelligent document intelligence
        platform that allows users to upload documents,
        generate embeddings, perform semantic search,
        and ask questions using Retrieval-Augmented Generation.
        """

    )


    st.info(

        """
        **ANRO AI Pipeline**

        📄 Document
        →
        🧹 Cleaning
        →
        ✂️ Chunking
        →
        🧠 Embeddings
        →
        🗄️ ChromaDB
        →
        🔎 Retrieval
        →
        🤖 Ollama LLM
        →
        💬 RAG Answer
        """

    )


# ============================================================
# DOCUMENTS
# ============================================================

elif page == "📄 Documents":

    st.title(
        "📄 Document Management"
    )


    st.write(

        f"Upload documents to ANRO AI, "
        f"**{user_name}**."

    )


    if st.session_state.current_document_id:

        st.success(
            "✅ Active document is ready for RAG."
        )

        st.write(

            f"**File:** "
            f"{st.session_state.current_document_name}"

        )

        st.code(

            st.session_state.current_document_id,

            language="text",

        )

    else:

        st.info(
            "No document is currently active."
        )


    st.divider()


    uploaded_file = st.file_uploader(

        "Choose a document",

        type=[

            "txt",

            "pdf",

            "docx",

        ],

    )


    if uploaded_file:

        st.info(

            f"Selected: "
            f"{uploaded_file.name}"

        )


        if st.button(

            "🚀 Ingest Document",

            use_container_width=True,

        ):

            try:

                files = {

                    "file": (

                        uploaded_file.name,

                        uploaded_file.getvalue(),

                        uploaded_file.type,

                    )

                }


                with st.spinner(

                    "Processing document..."

                ):

                    response = requests.post(

                        f"{BACKEND_URL}"
                        "/api/documents/ingest",

                        files=files,

                        headers=get_auth_headers(),

                        timeout=120,

                    )


                if response.status_code == 200:

                    data = response.json()

                    result = data.get(

                        "result",

                        {},

                    )


                    document_id = result.get(

                        "document_id"

                    )


                    if document_id:

                        st.session_state.current_document_id = (

                            document_id

                        )


                        st.session_state.current_document_name = (

                            result.get(

                                "filename",

                                uploaded_file.name,

                            )

                        )


                        st.success(

                            "✅ Document ingested successfully!"

                        )


                        st.info(

                            "📄 This document is now active "
                            "for RAG questions."

                        )


                        st.write(
                            "**Document ID:**"
                        )


                        st.code(

                            document_id,

                            language="text",

                        )


                        st.subheader(

                            "📊 Ingestion Details"

                        )


                        col1, col2, col3 = st.columns(3)


                        with col1:

                            st.metric(

                                "Characters",

                                result.get(

                                    "characters",

                                    0,

                                ),

                            )


                        with col2:

                            st.metric(

                                "Total Chunks",

                                result.get(

                                    "total_chunks",

                                    0,

                                ),

                            )


                        with col3:

                            st.metric(

                                "Status",

                                result.get(

                                    "status",

                                    "Unknown",

                                ),

                            )


                        with st.expander(

                            "🔍 View Complete Ingestion Response"

                        ):

                            st.json(

                                data

                            )


                    else:

                        st.error(

                            "❌ Document ingested, "
                            "but document_id was not returned."

                        )

                        st.json(

                            data

                        )


                elif response.status_code == 401:

                    st.error(

                        "🔐 Your login session is invalid "
                        "or expired. Please login again."

                    )

                    logout_user()


                else:

                    show_api_error(

                        response

                    )


            except requests.RequestException as error:

                st.error(

                    f"Backend connection error: "
                    f"{error}"

                )


    st.divider()


    st.subheader(
        "📚 Supported Formats"
    )


    response = api_get(

        "/api/documents/"
        "supported-formats"

    )


    if response and response.status_code == 200:

        st.json(

            response.json()

        )

    else:

        st.warning(

            "Unable to load supported formats."

        )


# ============================================================
# SEMANTIC SEARCH
# ============================================================

elif page == "🔎 Semantic Search":

    st.title(
        "🔎 Semantic Document Search"
    )


    query = st.text_input(

        "Enter your search query",

        placeholder="What is Python?",

    )


    top_k = st.slider(

        "Number of results",

        min_value=1,

        max_value=10,

        value=3,

    )


    if st.button(

        "🔍 Search Documents",

        use_container_width=True,

    ):

        if not query.strip():

            st.warning(

                "Please enter a search query."

            )

        else:

            try:

                with st.spinner(

                    "Searching documents..."

                ):

                    response = requests.post(

                        f"{BACKEND_URL}/api/search",

                        json={

                            "query":
                                query,

                            "top_k":
                                top_k,

                        },

                        headers=get_auth_headers(),

                        timeout=60,

                    )


                if response.status_code == 200:

                    data = response.json()


                    st.success(

                        f"Found "
                        f"{data.get('result_count', 0)} "
                        f"results."

                    )


                    for result in data.get(

                        "results",

                        [],

                    ):

                        with st.expander(

                            f"#{result.get('rank', '?')} "
                            f"Search Result"

                        ):

                            st.write(

                                result.get(

                                    "text",

                                    "",

                                )

                            )

                            st.caption(

                                f"Distance: "
                                f"{result.get('distance', 'N/A')}"

                            )

                            st.json(

                                result.get(

                                    "metadata",

                                    {},

                                )

                            )


                elif response.status_code == 401:

                    st.error(

                        "🔐 Authentication expired. "
                        "Please login again."

                    )

                    logout_user()


                else:

                    show_api_error(

                        response

                    )


            except requests.RequestException as error:

                st.error(

                    f"Backend connection error: "
                    f"{error}"

                )


# ============================================================
# RAG CHAT
# ============================================================

elif page == "🤖 Ask ANRO AI":

    st.title(
        "🤖 Ask ANRO AI"
    )


    st.write(

        f"Ask questions about your selected document, "
        f"**{user_name}**."

    )


    current_document_id = (

        st.session_state.get(

            "current_document_id"

        )

    )


    if current_document_id:

        st.success(

            "📄 Active document selected for RAG."

        )

        st.write(

            f"**Document:** "
            f"{st.session_state.current_document_name}"

        )

    else:

        st.warning(

            "⚠️ No active document found. "
            "Please ingest a document first."

        )


    rag_status_response = api_get(

        "/api/rag/status"

    )


    if (

        rag_status_response

        and rag_status_response.status_code == 200

    ):

        rag_status_data = (

            rag_status_response.json()

        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(

                "RAG Status",

                rag_status_data.get(

                    "status",

                    "Unknown",

                ),

            )


        with col2:

            st.metric(

                "LLM Provider",

                rag_status_data.get(

                    "llm_provider",

                    "Unknown",

                ),

            )


        with col3:

            st.metric(

                "Model",

                rag_status_data.get(

                    "model",

                    "Unknown",

                ),

            )


    st.divider()


    if st.button(

        "🗑️ Clear Chat",

    ):

        st.session_state.chat_history = []


        try:

            requests.delete(

                f"{BACKEND_URL}"
                "/api/rag/conversation",

                headers=get_auth_headers(),

                timeout=30,

            )

        except requests.RequestException:

            pass


        st.success(

            "Conversation cleared successfully."

        )


        st.rerun()


    # ========================================================
    # CHAT HISTORY
    # ========================================================

    for message in st.session_state.chat_history:

        with st.chat_message(

            message["role"]

        ):

            st.write(

                message["content"]

            )


    question = st.chat_input(

        "Ask ANRO AI a question..."

    )


    if question:

        if not current_document_id:

            st.error(

                "❌ No active document found. "
                "Please ingest a document first."

            )

            st.stop()


        with st.chat_message(

            "user"

        ):

            st.write(

                question

            )


        st.session_state.chat_history.append(

            {

                "role":
                    "user",

                "content":
                    question,

            }

        )


        try:

            with st.chat_message(

                "assistant"

            ):

                with st.spinner(

                    "ANRO AI is thinking..."

                ):

                    response = requests.post(

                        f"{BACKEND_URL}/api/rag/ask",

                        json={

                            "question":
                                question,

                            "document_id":
                                current_document_id,

                        },

                        headers=get_auth_headers(),

                        timeout=120,

                    )


                if response.status_code == 200:

                    data = response.json()


                    answer = data.get(

                        "answer",

                        "No answer received.",

                    )


                    st.write(

                        answer

                    )


                    citations = data.get(

                        "citations",

                        [],

                    )


                    if citations:

                        st.divider()

                        st.subheader(

                            "📚 Sources"

                        )


                        for citation in citations:

                            with st.expander(

                                f"Source "
                                f"{citation.get('source_number', '?')} "
                                f"• Chunk "
                                f"{citation.get('chunk_index', 'N/A')}"

                            ):

                                st.write(

                                    citation.get(

                                        "preview",

                                        "",

                                    )

                                )


                    st.session_state.chat_history.append(

                        {

                            "role":
                                "assistant",

                            "content":
                                answer,

                            "citations":
                                citations,

                            "analysis":
                                data.get(
                                    "analysis",
                                    {},
                                ),

                        }

                    )


                elif response.status_code == 401:

                    st.error(

                        "🔐 Authentication expired. "
                        "Please login again."

                    )

                    logout_user()


                else:

                    show_api_error(

                        response

                    )


        except requests.RequestException as error:

            st.error(

                f"Backend connection error: "
                f"{error}"

            )


# ============================================================
# CONVERSATION PAGE
# ============================================================

elif page == "💬 Conversation":

    st.title(

        "💬 Conversation Memory"

    )


    response = api_get(

        "/api/rag/conversation",

        authenticated=True,

    )


    if response and response.status_code == 200:

        data = response.json()


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(

                "Conversation ID",

                data.get(

                    "conversation_id",

                    "N/A",

                ),

            )


        with col2:

            st.metric(

                "Memory Size",

                data.get(

                    "memory_size",

                    0,

                ),

            )


        with col3:

            st.metric(

                "LLM Model",

                data.get(

                    "model",

                    "N/A",

                ),

            )


        st.divider()


        st.json(

            data

        )


    elif response and response.status_code == 401:

        st.error(

            "🔐 Authentication expired. "
            "Please login again."

        )

        logout_user()


    else:

        st.warning(

            "Conversation data unavailable."

        )


    st.divider()


    if st.button(

        "🗑️ Clear Conversation",

        use_container_width=True,

    ):

        try:

            response = requests.delete(

                f"{BACKEND_URL}"
                "/api/rag/conversation",

                headers=get_auth_headers(),

                timeout=30,

            )


            if response.status_code == 200:

                st.success(

                    "✅ Conversation cleared."

                )

                st.session_state.chat_history = []

                st.rerun()


            else:

                show_api_error(

                    response

                )


        except requests.RequestException as error:

            st.error(

                f"Backend connection error: "
                f"{error}"

            )