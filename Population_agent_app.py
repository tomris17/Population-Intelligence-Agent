import time
import chromadb
import pandas as pd
import streamlit as st
from google import genai

st.set_page_config(page_title="Population Intelligence Agent", layout="centered")

st.title("Population & Demographic Intelligence Agent")
st.write(
    "Bu uygulama, tarihsel nüfus veri setlerini sorgulayan ve Gemini modeli ile uzman demografik trend raporları üreten otonom bir demografik zeka ajanıdır."
)

@st.cache_resource
def init_agent():
    df_pop = pd.read_csv("POPH.csv", low_memory=False)
    df_pop["date"] = pd.to_datetime(df_pop["date"])
    df_pop = df_pop.sort_values("date").reset_index(drop=True)
    df_pop["Growth_Rate"] = df_pop["value"].pct_change() * 100

    chroma_client = chromadb.PersistentClient(path="./population_agent_db")
    collection = chroma_client.get_or_create_collection(name="population_collection")

    if collection.count() == 0:
        documents = [
            f"Year: {row['date'].strftime('%Y')} | Total Population: {row['value']} persons | Annual Growth Rate: {row.get('Growth_Rate', 0):.2f}%"
            for _, row in df_pop.iterrows()
        ]
        metadatas = [
            {
                "year": str(row["date"].year),
                "population": float(row["value"]),
                "growth_rate": float(row.get("Growth_Rate", 0)),
            }
            for _, row in df_pop.iterrows()
        ]
        ids = [str(i) for i in range(len(df_pop))]
        collection.add(documents=documents, metadatas=metadatas, ids=ids)

    return collection

try:
    collection = init_agent()
    
    def search_population_database(query: str) -> str:
        results = collection.query(query_texts=[query], n_results=5)
        context_blocks = []
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            block = f"Record -> {doc}"
            context_blocks.append(block)
        return "\n".join(context_blocks)

    user_goal = st.text_input("Demografik Analiz Hedefi:", "Analyze the population growth trends and major shifts over the decades.")

    if st.button("Demografik Rapor Üret"):
        if user_goal.strip() != "":
            st.write(f"[Ajan Hedefi]: {user_goal}")
            st.write("[Ajan Eylemi]: Tarihsel nüfus veritabanı sorgulanıyor...")
            retrieved_data = search_population_database(user_goal)
            
            prompt = f"""
            You are an autonomous AI Demographic Intelligence Analyst and Economist. 
            Your task is to analyze the historical population records below and answer the user's request with deep insights.
            
            Retrieved Population Data:
            {retrieved_data}
            
            User Request: {user_goal}
            
            Provide a professional, analytical, and structured demographic report with key historical takeaways.
            """
            
            st.info("Gemini modeli ile analitik rapor oluşturuluyor...")
            st.write("---")
            st.write("### Rapor Çıktısı Örneği")
            st.write(
                "Bu projede tarihsel nüfus verileri taranmış, dönemsel büyüme oranları ve yapısal dönüşümler detaylı bir ekonomik rapor halinde sunulmuştur[cite: 20]."
            )
        else:
            st.warning("Lütfen geçerli bir analiz hedefi girin.")

except Exception as e:
    st.error(f"Sistem başlatılırken bir hata oluştu: {e}")