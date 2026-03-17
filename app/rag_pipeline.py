# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
# from app.embeddings import get_embedding
# from app.document_processor import process_file
# from app.llm import generate_answer


# class RAGPipeline:

#     def __init__(self):
#         self.documents = []
#         self.embeddings = []

#     async def ingest_document(self, filename, content):
#         chunks = process_file(filename, content)

#         for chunk in chunks:
#             emb = get_embedding(chunk)
#             self.documents.append(chunk)
#             self.embeddings.append(emb)

#         return {"chunks": len(chunks)}

#     async def query(self, question, top_k=3):

#         if len(self.embeddings) == 0:
#             return {
#                 "question": question,
#                 "answer": "❌ No documents uploaded yet. Please upload a report first.",
#                 "sources": []
#             }

#         q_emb = get_embedding(question)

#         sims = cosine_similarity([q_emb], self.embeddings)[0]
#         top_idx = np.argsort(sims)[-top_k:][::-1]

#         context = "\n".join([self.documents[i] for i in top_idx])

#         answer = generate_answer(question, context)

#         return {
#             "question": question,
#             "answer": answer,
#             "sources": [self.documents[i] for i in top_idx]
#         }

#     async def list_documents(self):
#         return {"total_chunks": len(self.documents)}

#     async def delete_document(self, doc_id):
#         return {"message": "Not implemented"}

#     async def health_check(self):
#         return "running"






# from app.document_processor import extract_text, chunk_text
# from app.embeddings import get_embedding
# from app.llm import generate_answer

# from sklearn.metrics.pairwise import cosine_similarity


# class RAGPipeline:

#     def __init__(self):
#         self.documents = []
#         self.embeddings = []

#     async def ingest_document(self, filename, content):
#         text = extract_text(content, filename)
#         chunks = chunk_text(text)

#         for chunk in chunks:
#             emb = get_embedding(chunk)
#             self.documents.append(chunk)
#             self.embeddings.append(emb)

#         return {
#             "message": "Document processed successfully",
#             "chunks": len(chunks)
#         }

#     async def query(self, question, top_k=5):

#         # ❌ If no data
#         if len(self.embeddings) == 0:
#             return {
#                 "answer": "⚠ No documents uploaded yet.",
#                 "sources": []
#             }

#         # ✅ Step 1: embed question
#         q_emb = get_embedding(question)

#         # ✅ Step 2: similarity
#         sims = cosine_similarity([q_emb], self.embeddings)[0]

#         # ✅ Step 3: get top indexes
#         top_idx = sims.argsort()[-top_k:][::-1]

#         # ✅ Step 4: create top_chunks (IMPORTANT FIX)
#         top_chunks = []
#         for i in top_idx:
#             top_chunks.append(self.documents[i])

#         # ✅ Step 5: create context
#         context = "\n".join(top_chunks[:3])   # limit to top 3

#         # ✅ Step 6: generate answer
#         answer = generate_answer(question, context)

#         return {
#             "answer": answer,
#             "sources": top_chunks
#         }


# ---working version---

# from app.document_processor import extract_text, chunk_text
# from app.embeddings import get_embedding
# from app.llm import generate_answer
# from sklearn.metrics.pairwise import cosine_similarity


# class RAGPipeline:

#     def __init__(self):
#         self.documents = []
#         self.embeddings = []

#     # 🔥 FIXED: clears old data before new upload
#     async def ingest_document(self, filename, content):

#         # ✅ CLEAR OLD DATA (VERY IMPORTANT)
#         self.documents = []
#         self.embeddings = []

#         text = extract_text(content, filename)
#         chunks = chunk_text(text)

#         for chunk in chunks:
#             emb = get_embedding(chunk)
#             self.documents.append(chunk)
#             self.embeddings.append(emb)

#         return {
#             "message": "Document processed successfully",
#             "chunks": len(chunks)
#         }

#     async def query(self, question, top_k=5):

#         if len(self.embeddings) == 0:
#             return {
#                 "answer": "⚠ No documents uploaded yet.",
#                 "sources": []
#             }

#         # 🔹 Step 1: embed question
#         q_emb = get_embedding(question)

#         # 🔹 Step 2: similarity search
#         sims = cosine_similarity([q_emb], self.embeddings)[0]

#         # 🔹 Step 3: top chunks
#         top_idx = sims.argsort()[-top_k:][::-1]
#         top_chunks = [self.documents[i] for i in top_idx]

#         # 🔹 Step 4: build context
#         context = "\n".join(top_chunks[:3])

#         # 🔥 STEP 5: SEVERITY HANDLING (ROBUST)
#         q = question.lower()
#         text = context.lower()

#         if any(word in q for word in ["severe", "sever", "serious", "danger", "critical"]):

#             score = 0

#             if "glucose" in text:
#                 score += 1
#             if "cholesterol" in text:
#                 score += 1
#             if "ldl" in text:
#                 score += 1
#             if "hdl" in text:
#                 score += 1
#             if "hemoglobin" in text:
#                 score += 1

#             if score >= 4:
#                 return {
#                     "answer": "🔴 High concern. Multiple abnormal values detected. Consult a doctor immediately.",
#                     "sources": top_chunks
#                 }
#             elif score >= 2:
#                 return {
#                     "answer": "🟡 Moderate concern. Some abnormal values detected. Medical attention recommended.",
#                     "sources": top_chunks
#                 }
#             else:
#                 return {
#                     "answer": "🟢 Mild concern. No serious abnormalities.",
#                     "sources": top_chunks
#                 }

#         # 🔹 Step 6: LLM for other queries
#         answer = generate_answer(question, context)

#         return {
#             "answer": answer,
#             "sources": top_chunks
#         }


from app.document_processor import extract_text, chunk_text
from app.embeddings import get_embedding
from app.llm import generate_answer
from sklearn.metrics.pairwise import cosine_similarity


class RAGPipeline:

    def __init__(self):
        self.documents = []
        self.embeddings = []

    async def ingest_document(self, filename, content):
        self.documents = []
        self.embeddings = []

        text = extract_text(content, filename)

        if not text or not text.strip():
            return {
                "error": "Could not extract text. Please upload a text-based PDF or TXT file."
            }

        chunks = chunk_text(text)

        for chunk in chunks:
            emb = get_embedding(chunk)
            self.documents.append(chunk)
            self.embeddings.append(emb)

        return {
            "message": f"Document processed successfully ({len(chunks)} chunks)",
            "chunks": len(chunks)
        }

    async def query(self, question, top_k=5):

        if not self.embeddings:
            return {
                "answer": "⚠️ No document uploaded yet. Please upload your medical report first.",
                "sources": []
            }

        q_emb = get_embedding(question)
        sims = cosine_similarity([q_emb], self.embeddings)[0]

        top_idx = sims.argsort()[-top_k:][::-1]
        top_chunks = [self.documents[i] for i in top_idx]

        context = "\n\n---\n\n".join(top_chunks[:3])

        answer = generate_answer(question, context)

        return {
            "answer": answer,
            "sources": top_chunks[:3]
        }