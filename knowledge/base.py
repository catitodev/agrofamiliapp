import os
import chromadb
from chromadb.config import Settings
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List


class KnowledgeBase:
    def __init__(self, persist_dir: str = None, collection_name: str = "agroecology"):
        self.persist_dir = persist_dir or os.getenv("CHROMA_PERSIST_DIR", "./knowledge/vectorstore")
        self.collection_name = collection_name
        self.embeddings = SentenceTransformerEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        self._client = None
        self._db = None

    def get_client(self):
        if self._client is None:
            self._client = chromadb.PersistentClient(path=self.persist_dir)
        return self._client

    def get_db(self):
        if self._db is None:
            self._db = Chroma(
                client=self.get_client(),
                collection_name=self.collection_name,
                embedding_function=self.embeddings
            )
        return self._db

    def load_documents(self, docs_dir: str = "./knowledge"):
        db = self.get_db()
        all_docs = []
        for root, _, files in os.walk(docs_dir):
            for f in files:
                if f.endswith((".txt", ".md")):
                    path = os.path.join(root, f)
                    with open(path, encoding="utf-8") as file:
                        content = file.read()
                        chunks = self.splitter.split_text(content)
                        for chunk in chunks:
                            all_docs.append(chunk)

        if all_docs:
            db.add_texts(all_docs)

    def search(self, query: str, k: int = 5) -> List[str]:
        db = self.get_db()
        results = db.similarity_search(query, k=k)
        return [r.page_content for r in results]


kb = KnowledgeBase()