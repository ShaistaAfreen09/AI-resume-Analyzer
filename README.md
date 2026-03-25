# AI Resume Analyzer

AI-powered system for automated resume screening using NLP and semantic similarity.

---

## Features

- Upload resumes (PDF/DOCX)
- Extract and process unstructured text
- Perform semantic matching with job descriptions
- Generate relevance scores
- Rank candidates automatically

---

## Tech Stack

- Python, Streamlit  
- SpaCy, NLTK  
- scikit-learn, Pandas  
- MySQL  

---

## Approach

- Text extraction and preprocessing  
- TF-IDF vectorization  
- Cosine similarity for semantic scoring  
- Rule-based + ML-driven ranking  

---

## 📸 Screenshots

![Screenshot](https://github.com/user-attachments/assets/a29c66bf-1c59-4099-83c2-ac981cb73bb2)
![Screenshot](https://github.com/user-attachments/assets/fd1cfa47-3388-4c4b-80d4-ec0bb7974f39)
![Screenshot](https://github.com/user-attachments/assets/78bcdfb0-efa4-4d53-9b1f-7680f22f6ab9)

---

## Future Work

- Transformer/LLM-based semantic matching  
- RAG-based resume evaluation  
- Batch processing pipeline  

---

## Run Locally

```bash
git clone https://github.com/ShaistaAfreen09/AI-resume-Analyzer.git
cd AI-resume-Analyzer
pip install -r requirements.txt
streamlit run app.py
