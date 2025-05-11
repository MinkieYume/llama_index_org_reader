import chromadb
import os

from pathlib import Path

from llama_index.core import VectorStoreIndex
from llama_index.core import Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from deepseek_tokenizer import ds_token

from org_roam_db_reader import OrgRoamDbReader

def get_storage_context_chroma(store_path):
    chroma_client = chromadb.PersistentClient(path=default_store_path)
    chroma_collection = chroma_client.get_or_create_collection("OrgRoamNodes")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return storage_context

if __name__ == '__main__':
    defalt_db_path = "~/.emacs.d/org-roam.db"
    defalt_db_path = os.path.expanduser(defalt_db_path)
    default_store_path = db_file = str(Path.cwd() / "chroma_db")

    Settings.tokenzier = ds_token
    Settings.embed_model = OllamaEmbedding(model_name="bge-m3")
    
    org_roam_reader = OrgRoamDbReader()
    documents = org_roam_reader.load_data(defalt_db_path)

    parser = SentenceSplitter(chunk_size=2048,chunk_overlap=20)
    print("正在切分节点...")
    nodes = parser.get_nodes_from_documents(documents)
    print(f"节点数：{len(nodes)}")
    storage_context = get_storage_context_chroma(default_store_path)
    print("正在构建索引并生成 embedding...")
    index = VectorStoreIndex(nodes,storage_context=storage_context)
    print("正在持久化索引...")
    index.storage_context.persist()
    print("完成！")
