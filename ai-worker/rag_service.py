import chromadb
from chromadb.utils import embedding_functions
from ai_analyst import ai_analyst

class FinancialRAGService:
    def __init__(self):
        # 1. Initialize persistent ChromaDB vector store
        self.chroma_client=chromadb.PersistentClient(path="./chroma_db")

        # 2. Get or create collection for AML typologies and past audit cases
        self.collection=self.chroma_client.get_or_create_collection(
            name="aml_investigation_knowledge",
            metadata={"hnsw:space":"cosine"}
        )

        self._seed_initial_aml_knowledge()

    def _seed_initial_aml_knowledge(self):
        """
        Seeds standard RBI/FIU-IND Anti-Money Laundering typologies and past fraud case studies.
        """
        # If collection already has records, don't re-seed
        if self.collection.count()>0:
            print(f">> [RAG Service] Loaded {self.collection.count()} AML case files from ChromaDB.")
            return
        cases=[
            {
                "id": "CASE-101",
                "text": "Structuring and Smurfing: Account received multiple deposits of ₹49,000 within 2 hours to circumvent the mandatory ₹50,000 PAN reporting threshold under Section 139A. Funds immediately transferred to third-party accounts.",
                "category": "SMURFING_STRUCTURING",
                "risk": "HIGH"
            },
            {
                "id": "CASE-102",
                "text": "Account Takeover (ATO): Dormant savings account in Pune suddenly accessed at 02:45 AM from an overseas IP address. Immediate full-balance wire transfer attempted to an offshore crypto exchange.",
                "category": "ACCOUNT_TAKEOVER",
                "risk": "CRITICAL"
            },
            {
                "id": "CASE-103",
                "text": "Money Mule Activity: Student savings account with typical monthly volume of ₹1,500 suddenly received inward RTGS credit of ₹4,50,000 followed by multiple rapid cash ATM withdrawals in different locations.",
                "category": "MULE_ACCOUNT",
                "risk": "HIGH"
            },
            {
                "id": "CASE-104",
                "text": "Cyber Fraud / Phishing Proceeds: Victim tricked into AnyDesk remote access. Instant high-velocity UPI transfers of ₹95,000 routed to multiple merchant payment aggregators.",
                "category": "PHISHING_CYBER_FRAUD",
                "risk": "CRITICAL"
            },
            {
                "id": "CASE-105",
                "text": "Trade-based Layering: Multiple invoices settled with cross-border international wire transfers for luxury goods with mismatched beneficiary PAN details.",
                "category": "LAYERING",
                "risk": "HIGH"
            }
        ]

        # Add to ChromaDB vector collection
        self.collection.add(
            ids=[c["id"] for c in cases],
            documents=[c["text"] for c in cases],
            metadatas=[{"category": c["category"],"risk":c["risk"]} for c in cases]
        )
        print(">> [RAG Service] Ingestion complete. Vectors stored in ChromaDB.")

    def add_audit_record(self,tx_id:int,account_id:int,summary:str,risk_level:str):
        """
        Dynamically adds live audited transactions into the vector database.
        """
        doc_id=f"TX-AUDIT-{tx_id}"
        self.collection.add(
            ids=[doc_id],
            documents=[summary],
            metadatas={"account_id":account_id,"risk":risk_level}
        )

    def search_similar_cases(self,query:str,top_k:int=2)->list[dict]:
        """
        Performs semantic vector search using Cosine Similarity.
        """
        results=self.collection.query(
            query_texts=[query],
            n_results=top_k
        )

        matches=[]
        if results and "documents" in results and results["documents"]:
            docs=results["documents"][0]
            metas=results["metadatas"][0]
            ids=results["ids"][0]
            distances=results["distances"][0] if "distances" in results else [0]*len(docs)

            for doc_id,doc,meta,dist in zip(ids,docs,metas,distances):
                matches.append({
                    "case_id":doc_id,
                    "description":doc,
                    "category":meta.get("category","AUDIT"),
                    "risk":meta.get("risk","UNKNOWN"),
                    "similarity_score":round(1.0-dist,3)
                })
        return matches
    def investigate_analyst_query(self,query:str,top_k:int=2)->dict:
        """
        Complete RAG Pipeline:
        1. Semantic Retrieval: Finds closest historical AML cases.
        2. Prompt Augmentation: Feeds retrieved cases to Gemini LLM.
        3. Generation: Gemini synthesizes an expert compliance answer.
        """
        # Step 1: Retrieve relevant context
        similar_cases=self.search_similar_cases(query,top_k=2)

        context_blocks = "\n".join([
            f"- [{c['case_id']}] {c['description']} (Category: {c['category']}, Risk: {c['risk']})"
            for c in similar_cases
        ])

        # Step 2: Augment prompt with retrieved private bank intelligence
        prompt = f"""
        You are a Senior AML Investigator and Financial Intelligence Analyst at BNP Paribas.
        An analyst is asking this investigative question:
        "{query}"
        Here are the most relevant historical fraud cases and typologies retrieved from our secure bank database:
        {context_blocks}
        Based strictly on these retrieved historical patterns and regulatory standards (RBI & PMLA):
        1. Identify the matching financial crime pattern.
        2. Explain the modus operandi (how the criminal operates).
        3. Recommend immediate investigative next steps (e.g. STR filing, freeze orders, EDD).
        Keep your answer concise, professional, and authoritative.
        """
        # Step 3: LLM Generation
        ai_response = "Unable to contact Gemini. Based on retrieved records, this query matches: " + context_blocks
        if ai_analyst.client:
            try:
                resp = ai_analyst.client.models.generate_content(
                    model='gemini-3.5-flash-lite',
                    contents=prompt
                )
                if resp and resp.text:
                    ai_response = resp.text.strip()
            except Exception as e:
                ai_response = f"LLM Generation fallback: {e}\nRetrieved evidence:\n{context_blocks}"
        return {
            "query": query,
            "retrieved_precedents": similar_cases,
            "investigative_assessment": ai_response
        }

    def ingest_live_incident(self, case_id: str, description: str, category: str, risk: str = "HIGH"):
        """Dynamically ingests a newly blocked/flagged transaction into ChromaDB."""
        self.collection.add(
            ids=[case_id],
            documents=[description],
            metadatas=[{
                "case_id": case_id,
                "category": category,
                "risk": risk
            }]
        )
        print(f">> [RAG Service] Dynamic Incident ingested into ChromaDB: {case_id}")

# Singleton instance
rag_service = FinancialRAGService()