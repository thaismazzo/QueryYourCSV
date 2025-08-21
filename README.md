# QueryYourCSV

QueryYourCSV is a project focused on using the **Text to SQL** technique to analyze .csv databases.  
It allows users to input natural language queries and extract valuable information out of them.

---

## 📝 Description

This project transforms natural language commands into SQL queries, which makes it easier to explore databases without writing SQL manually or performing long sheet equations.

---

## 🚀 How to Use

### 1. Clone the repository
```bash
git clone https://github.com/your_username/TextToSql.git
cd TextToSql
```
### 2. Insert .env with your OPENAI_API_KEY. Please be aware that you can change the model of your preference on the folder core/model.py
### 3. Open your Docker Engine
### 4. In the terminal of your project, inside TextToSql folder, run:
```bash
docker build -t meu_app_streamlit .
docker run -it --rm -p 8501:8501 meu_app_streamlit
```
### 5. Open the link for your localhost, usually: http://localhost:8501/
### 6. You will then see the frontend of our application. Input the provided .csv file and have fun asking questions and exploring your database with natural language :)