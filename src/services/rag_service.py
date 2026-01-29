from pathlib import Path
from typing import Optional

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings



DATA_DIR = Path("data")
UPLOAD_DIR = DATA_DIR / "uploads"
INDEX_DIR = DATA_DIR / "faiss_index"


class RAGService:
    """
    RAG service using LangChain FAISS abstraction.
    Works even if native faiss is unavailable on Windows.
    """

    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vectorstore: Optional[FAISS] = None

        if INDEX_DIR.exists():
            try:
                self.vectorstore = FAISS.load_local(
                    str(INDEX_DIR),
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
            except Exception:
                self.vectorstore = None

    def build_index(self, file_path: str) -> None:
        try:
            from langchain_community.vectorstores import FAISS
        except ImportError:
            raise RuntimeError(
                "FAISS is required for the retriever but is not installed "
                "in this environment."
            )

        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(file_path)

        # Load document
        if path.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(path))
        else:
            loader = TextLoader(str(path), encoding="utf-8")

        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
        chunks = splitter.split_documents(documents)

        self.vectorstore = FAISS.from_documents(
            chunks,
            self.embeddings
        )

        self.vectorstore.save_local(str(INDEX_DIR))

    def retrieve_context(self, query: str, k: int = 3) -> str:
        if not self.vectorstore:
            return ""

        docs = self.vectorstore.similarity_search(query, k=k)
        return "\n\n".join(doc.page_content for doc in docs)


rag_service = RAGService()
