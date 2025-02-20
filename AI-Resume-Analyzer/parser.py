import spacy
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from PyPDF2 import PdfReader
from docx import Document
import json
import re

class ResumeParser:
    def __init__(self):
        # Load SpaCy model
        self.nlp = spacy.load("en_core_web_sm")
        
        # Download required NLTK data
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('maxent_ne_chunker')
        nltk.download('words')
        
        # Load skills database
        with open('models/skills.json', 'r') as f:
            self.skills_db = json.load(f)

    def extract_text(self, filepath):
        """Extract text from PDF or DOCX files"""
        if filepath.endswith('.pdf'):
            reader = PdfReader(filepath)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        elif filepath.endswith('.docx'):
            doc = Document(filepath)
            text = " ".join([paragraph.text for paragraph in doc.paragraphs])
        return text

    def extract_name(self, text):
        """Extract name using SpaCy NER"""
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        return None

    def extract_email(self, text):
        """Extract email using regex"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else None

    def extract_skills(self, text):
        """Extract skills by matching against skills database"""
        found_skills = []
        tokens = word_tokenize(text.lower())
        
        for skill in self.skills_db:
            if skill.lower() in tokens:
                found_skills.append(skill)
        
        return list(set(found_skills))

    def extract_education(self, text):
        """Extract education details using NER and pattern matching"""
        education = []
        doc = self.nlp(text)
        
        # Define education-related keywords
        edu_keywords = ['bachelor', 'master', 'phd', 'degree', 'diploma']
        
        for sent in doc.sents:
            if any(keyword in sent.text.lower() for keyword in edu_keywords):
                education.append(sent.text.strip())
        
        return education

    def parse(self, filepath):
        """Main parsing function"""
        text = self.extract_text(filepath)
        
        return {
            'name': self.extract_name(text),
            'email': self.extract_email(text),
            'skills': self.extract_skills(text),
            'education': self.extract_education(text),
            'raw_text': text
        }