import mysql.connector
from mysql.connector import Error
import json
from config import DB_CONFIG

class Database:
    def __init__(self):
        self.connection = self.connect()
        self.create_tables()

    def connect(self):
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    def create_tables(self):
        try:
            cursor = self.connection.cursor()
            
            # Create resumes table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS resumes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    email VARCHAR(255),
                    raw_text TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create skills table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS skills (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    resume_id INT,
                    skill VARCHAR(255),
                    FOREIGN KEY (resume_id) REFERENCES resumes(id)
                )
            """)
            
            # Create education table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS education (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    resume_id INT,
                    education_detail TEXT,
                    FOREIGN KEY (resume_id) REFERENCES resumes(id)
                )
            """)
            
            self.connection.commit()
            
        except Error as e:
            print(f"Error creating tables: {e}")

    def store_resume(self, parsed_data):
        try:
            cursor = self.connection.cursor()
            
            # Insert main resume data
            cursor.execute("""
                INSERT INTO resumes (name, email, raw_text)
                VALUES (%s, %s, %s)
            """, (parsed_data['name'], parsed_data['email'], parsed_data['raw_text']))
            
            resume_id = cursor.lastrowid
            
            # Insert skills
            for skill in parsed_data['skills']:
                cursor.execute("""
                    INSERT INTO skills (resume_id, skill)
                    VALUES (%s, %s)
                """, (resume_id, skill))
            
            # Insert education
            for edu in parsed_data['education']:
                cursor.execute("""
                    INSERT INTO education (resume_id, education_detail)
                    VALUES (%s, %s)
                """, (resume_id, edu))
            
            self.connection.commit()
            return resume_id
            
        except Error as e:
            print(f"Error storing resume: {e}")
            return None

    def get_resume(self, resume_id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            # Get main resume data
            cursor.execute("""
                SELECT * FROM resumes WHERE id = %s
            """, (resume_id,))
            resume_data = cursor.fetchone()
            
            if not resume_data:
                return None
            
            # Get skills
            cursor.execute("""
                SELECT skill FROM skills WHERE resume_id = %s
            """, (resume_id,))
            skills = [row['skill'] for row in cursor.fetchall()]
            
            # Get education
            cursor.execute("""
                SELECT education_detail FROM education WHERE resume_id = %s
            """, (resume_id,))
            education = [row['education_detail'] for row in cursor.fetchall()]
            
            resume_data['skills'] = skills
            resume_data['education'] = education
            
            return resume_data
            
        except Error as e:
            print(f"Error retrieving resume: {e}")
            return None