# from app.document_processor import extract_text, chunk_text
# from app.embeddings import get_embedding
# from app.llm import generate_answer
# from sklearn.metrics.pairwise import cosine_similarity


# class RAGPipeline:

#     def __init__(self):
#         self.documents = []
#         self.embeddings = []

#     async def ingest_document(self, filename, content):
#         self.documents = []
#         self.embeddings = []

#         text = extract_text(content, filename)

#         if not text or not text.strip():
#             return {
#                 "error": "Could not extract text. Please upload a text-based PDF or TXT file."
#             }

#         chunks = chunk_text(text)

#         for chunk in chunks:
#             emb = get_embedding(chunk)
#             self.documents.append(chunk)
#             self.embeddings.append(emb)

#         return {
#             "message": f"Document processed successfully ({len(chunks)} chunks)",
#             "chunks": len(chunks)
#         }

#     async def query(self, question, top_k=5):

#         if not self.embeddings:
#             return {
#                 "answer": "⚠️ No document uploaded yet. Please upload your medical report first.",
#                 "sources": []
#             }

#         q_emb = get_embedding(question)
#         sims = cosine_similarity([q_emb], self.embeddings)[0]

#         top_idx = sims.argsort()[-top_k:][::-1]
#         top_chunks = [self.documents[i] for i in top_idx]

#         context = "\n\n---\n\n".join(top_chunks[:3])

#         answer = generate_answer(question, context)

#         return {
#             "answer": answer,
#             "sources": top_chunks[:3]
#         }





# from app.document_processor import extract_text, chunk_text
# from app.embeddings import get_embedding
# from app.llm import generate_answer
# from endee import Endee, Precision

# ENDEE_INDEX = "medical_reports"
# DIMENSION = 384  # all-MiniLM-L6-v2 output size


# class RAGPipeline:

#     def __init__(self):
#         self.documents = []
#         try:
#             self.client = Endee()
#             self._setup_index()
#             self.use_endee = True
#             print("✅ Connected to Endee vector database")
#         except Exception as e:
#             print(f"⚠️ Endee not available ({e}), using in-memory fallback")
#             self.use_endee = False
#             self.embeddings = []

#     def _setup_index(self):
#         try:
#             indexes = self.client.list_indexes()
#             # Fix: handle both string list and object list
#             existing = [i if isinstance(i, str) else i.name for i in indexes]
#             if ENDEE_INDEX not in existing:
#                 self.client.create_index(
#                     name=ENDEE_INDEX,
#                     dimension=DIMENSION,
#                     space_type="cosine",
#                     precision=Precision.INT8
#                 )
#                 print(f"✅ Created Endee index: {ENDEE_INDEX}")
#             self.index = self.client.get_index(name=ENDEE_INDEX)
#         except Exception as e:
#             raise Exception(f"Endee index setup failed: {e}")

#     async def ingest_document(self, filename, content):
#         self.documents = []

#         text = extract_text(content, filename)
#         if not text or not text.strip():
#             return {"error": "Could not extract text. Please upload a text-based PDF or TXT file."}

#         chunks = chunk_text(text)

#         if self.use_endee:
#             try:
#                 # Clear old vectors by deleting and recreating index
#                 try:
#                     self.client.delete_index(ENDEE_INDEX)
#                 except:
#                     pass
#                 self.client.create_index(
#                     name=ENDEE_INDEX,
#                     dimension=DIMENSION,
#                     space_type="cosine",
#                     precision=Precision.INT8
#                 )
#                 self.index = self.client.get_index(name=ENDEE_INDEX)

#                 # Upsert chunks into Endee
#                 vectors = []
#                 for i, chunk in enumerate(chunks):
#                     emb = get_embedding(chunk)
#                     self.documents.append(chunk)
#                     vectors.append({
#                         "id": f"chunk_{i}",
#                         "vector": emb.tolist(),
#                         "meta": {"text": chunk, "index": i}
#                     })

#                 self.index.upsert(vectors)
#                 print(f"✅ Stored {len(chunks)} chunks in Endee")

#             except Exception as e:
#                 print(f"Endee upsert failed: {e}, using fallback")
#                 self.use_endee = False
#                 self.embeddings = [get_embedding(c) for c in chunks]
#         else:
#             self.embeddings = []
#             for chunk in chunks:
#                 emb = get_embedding(chunk)
#                 self.embeddings.append(emb)

#         return {
#             "message": f"Document processed successfully ({len(chunks)} chunks)",
#             "chunks": len(chunks),
#             "vector_db": "Endee" if self.use_endee else "In-Memory Fallback"
#         }

#     async def query(self, question, top_k=5):
#         if not self.documents:
#             return {
#                 "answer": "⚠️ No document uploaded yet. Please upload your medical report first.",
#                 "sources": []
#             }

#         q_emb = get_embedding(question)

#         if self.use_endee:
#             try:
#                 results = self.index.query(
#                     vector=q_emb.tolist(),
#                     top_k=min(top_k, len(self.documents))
#                 )
#                 top_chunks = []
#                 for r in results:
#                     idx = int(r.id.split("_")[1])
#                     if idx < len(self.documents):
#                         top_chunks.append(self.documents[idx])
#             except Exception as e:
#                 print(f"Endee query failed: {e}, using fallback")
#                 top_chunks = self._fallback_search(q_emb, top_k)
#         else:
#             top_chunks = self._fallback_search(q_emb, top_k)

#         context = "\n\n---\n\n".join(top_chunks[:3])
#         answer = generate_answer(question, context)

#         return {
#             "answer": answer,
#             "sources": top_chunks[:3]
#         }

#     def _fallback_search(self, q_emb, top_k):
#         from sklearn.metrics.pairwise import cosine_similarity
#         sims = cosine_similarity([q_emb], self.embeddings)[0]
#         top_idx = sims.argsort()[-top_k:][::-1]
#         return [self.documents[i] for i in top_idx]





from app.document_processor import extract_text, chunk_text
from app.embeddings import get_embedding
from app.llm import generate_answer
from endee import Endee, Precision

ENDEE_INDEX = "medical_reports"
DIMENSION = 384


class RAGPipeline:

    def __init__(self):
        self.documents = []
        self.embeddings = []
        try:
            self.client = Endee()
            self._setup_index()
            self.use_endee = True
            print("✅ Connected to Endee vector database")
        except Exception as e:
            print(f"⚠️ Endee not available ({e}), using in-memory fallback")
            self.use_endee = False

    def _setup_index(self):
        try:
            indexes = self.client.list_indexes()
            existing = [i if isinstance(i, str) else i.name for i in indexes]
            if ENDEE_INDEX not in existing:
                self.client.create_index(
                    name=ENDEE_INDEX,
                    dimension=DIMENSION,
                    space_type="cosine",
                    precision=Precision.INT8
                )
                print(f"✅ Created Endee index: {ENDEE_INDEX}")
            else:
                print(f"✅ Using existing Endee index: {ENDEE_INDEX}")
            self.index = self.client.get_index(name=ENDEE_INDEX)
        except Exception as e:
            # If conflict, just get the existing index
            try:
                self.index = self.client.get_index(name=ENDEE_INDEX)
                print(f"✅ Retrieved existing Endee index: {ENDEE_INDEX}")
            except Exception as e2:
                raise Exception(f"Endee index setup failed: {e2}")

    async def ingest_document(self, filename, content):
        self.documents = []
        self.embeddings = []

        text = extract_text(content, filename)
        if not text or not text.strip():
            return {"error": "Could not extract text. Please upload a text-based PDF or TXT file."}

        chunks = chunk_text(text)

        if self.use_endee:
            try:
                # Clear old vectors
                try:
                    self.client.delete_index(ENDEE_INDEX)
                except:
                    pass

                self.client.create_index(
                    name=ENDEE_INDEX,
                    dimension=DIMENSION,
                    space_type="cosine",
                    precision=Precision.INT8
                )
                self.index = self.client.get_index(name=ENDEE_INDEX)

                # Build vectors list
                vectors = []
                for i, chunk in enumerate(chunks):
                    emb = get_embedding(chunk)
                    self.documents.append(chunk)
                    vectors.append({
                        "id": f"chunk_{i}",
                        "vector": emb.tolist(),
                        "metadata": {"text": chunk, "index": str(i)}
                    })

                self.index.upsert(vectors)
                print(f"✅ Stored {len(chunks)} chunks in Endee")

            except Exception as e:
                print(f"Endee upsert failed: {e}, using fallback")
                self.use_endee = False
                self.documents = []
                self.embeddings = []
                for chunk in chunks:
                    emb = get_embedding(chunk)
                    self.documents.append(chunk)
                    self.embeddings.append(emb)
        else:
            for chunk in chunks:
                emb = get_embedding(chunk)
                self.documents.append(chunk)
                self.embeddings.append(emb)

        return {
            "message": f"Document processed successfully ({len(chunks)} chunks)",
            "chunks": len(chunks),
            "vector_db": "Endee" if self.use_endee else "In-Memory Fallback"
        }

    async def query(self, question, top_k=5):
        if not self.documents:
            return {
                "answer": "⚠️ No document uploaded yet. Please upload your medical report first.",
                "sources": []
            }

        q_emb = get_embedding(question)

        if self.use_endee:
            try:
                results = self.index.query(
                    vector=q_emb.tolist(),
                    top_k=min(top_k, len(self.documents))
                )
                top_chunks = []
                for r in results:
                    idx = int(r.id.split("_")[1])
                    if idx < len(self.documents):
                        top_chunks.append(self.documents[idx])

                if not top_chunks:
                    top_chunks = self._fallback_search(q_emb, top_k)

            except Exception as e:
                print(f"Endee query failed: {e}, using fallback")
                top_chunks = self._fallback_search(q_emb, top_k)
        else:
            top_chunks = self._fallback_search(q_emb, top_k)

        context = "\n\n---\n\n".join(top_chunks[:3])
        answer = generate_answer(question, context)

        return {
            "answer": answer,
            "sources": top_chunks[:3]
        }

    def _fallback_search(self, q_emb, top_k):
        from sklearn.metrics.pairwise import cosine_similarity
        if not self.embeddings:
            return self.documents[:top_k]
        sims = cosine_similarity([q_emb], self.embeddings)[0]
        top_idx = sims.argsort()[-top_k:][::-1]
        return [self.documents[i] for i in top_idx]