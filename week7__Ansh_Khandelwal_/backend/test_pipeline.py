import os
from rag_engine import RAGEngine

def main():
    print("=== InsightRAG Pipeline Test ===")
    
    # 1. Create a dummy knowledge base document
    data_dir = "./data"
    os.makedirs(data_dir, exist_ok=True)
    
    test_file = os.path.join(data_dir, "about_insightrag.txt")
    facts = (
        "InsightRAG is an advanced Retrieval-Augmented Generation system built in 2026. "
        "It is designed to solve LLM hallucination problems by grounding responses in private documents. "
        "InsightRAG uses hybrid search which combines semantic vector embeddings from Chroma DB "
        "and lexical keyword search using BM25. The dense retriever uses the sentence-transformers/all-MiniLM-L6-v2 "
        "model to embed text. After gathering candidates, a Cross-Encoder model (ms-macro-MiniLM-L-6-v2) "
        "reranks the document chunks to ensure the most relevant contexts are fed to the generator. "
        "InsightRAG default model configuration uses the newly announced Google gemini-3.1-flash-lite LLM model "
        "to synthesize the final responses, ensuring extremely fast generation speeds and cost efficiency."
    )
    
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(facts)
    print(f"Created sample text file: {test_file}")

    # 2. Initialize the Engine
    engine = RAGEngine(data_dir=data_dir, db_dir="./chroma_db", metadata_file="./metadata.json")

    # 3. Ingest document
    print("\nIngesting document...")
    res = engine.ingest_document(test_file, chunk_size=300, chunk_overlap=50)
    print(f"Ingestion response: {res}")

    # 4. Perform Retrieval
    query = "What LLM model does InsightRAG use by default, and what are its search methods?"
    print(f"\nQuerying retrieval: '{query}'")
    retrieved = engine.retrieve(
        query=query, 
        retrieval_type="hybrid", 
        top_k=2,
        use_reranker=True
    )
    
    print("\nRetrieved & Re-ranked Chunks:")
    for idx, doc in enumerate(retrieved):
        print(f"[{idx+1}] File: {doc['metadata'].get('source')} (Score: {doc['score']:.4f})")
        print(f"    Text: {doc['content']}")

    # 5. Generate Answer
    print("\nGenerating answer...")
    ans_res = engine.generate_answer(
        query=query,
        context_docs=retrieved,
        model_name="gemini-3.1-flash-lite"
    )
    
    print("\nGenerated Response:")
    print(ans_res["answer"])
    print(f"Model used: {ans_res['model_used']}")

if __name__ == "__main__":
    main()
