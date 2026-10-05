# Population & Demographic Intelligence Agent

[![Python](https://img.shields.io/badge/Python-3.13%2B-blue.svg)](https://www.python.org/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorSearch-orange.svg)](https://www.trychroma.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)](https://streamlit.io/)

This project builds an autonomous demographic intelligence agent that queries historical population datasets and uses Gemini models to generate expert population trend reports[cite: 20].

---

## Project Workflow
1. **Data Loading & Metric Computation**: Reading population dataset (`POPH.csv`), parsing datetime objects, sorting chronologically, and calculating annual growth rates (`Growth_Rate`)[cite: 20].
2. **Vector Indexing**: Storing historical population records and metadata into a persistent ChromaDB collection (`population_collection`)[cite: 20].
3. **Semantic Search & Retrieval**: Querying the vector database to extract relevant records and population statistics based on user goals[cite: 20].
4. **AI Intelligence Reporting**: Leveraging Google GenAI and Gemini models with specialized demographic analyst personas to output structured analytical reports[cite: 20].
5. **Web Application**: Interactive deployment interface built with Streamlit.

---

## Getting Started & Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/population-intelligence-agent.git](https://github.com/YOUR_USERNAME/population-intelligence-agent.git)
   cd population-intelligence-agent
