
# 🤖 AI Resume Analyzer

AI Resume Analyzer is a Streamlit-based web app that helps candidates and recruiters analyze resumes against job descriptions.  
It uses **Groq LLM API (LLaMA 3)** to compare resumes and job descriptions, providing:

- ✅ JD Match Percentage  
- 🔑 Matched & Missing Keywords  
- 🧠 Profile Summary of strengths & weaknesses  
- 📊 Visual comparison tables  
- 📂 Save results to database & export as CSV  

---

## 🚀 Features

- Upload a **Resume (PDF)** and paste a **Job Description**.
- Automatic **Resume vs JD analysis** using Groq LLM.
- Shows **JD match percentage** like an ATS (Applicant Tracking System).
- Extracts **Matched & Missing keywords**.
- Provides a concise **Profile Summary**.
- Save all analyses into a **SQLite database**.
- Download results as **CSV reports** (single analysis or all analyses).
- Sidebar to view the **latest 10 analyses**.

---

## 🛠️ Tech Stack

- [Python](https://www.python.org/)  
- [Streamlit](https://streamlit.io/)  
- [SQLite](https://www.sqlite.org/) (local DB for storing analyses)  
- [Groq API](https://groq.com/) (LLM - LLaMA 3)  
- [PyPDF2](https://pypi.org/project/PyPDF2/) (PDF text extraction)  
- [Pandas](https://pandas.pydata.org/) (data handling)  

---

## 📂 Project Structure

```

├── app.py          # Main Streamlit app
├── db.py           # SQLite database functions
├── requirements.txt # Dependencies
└── README.md       # Documentation

````

---

## ⚙️ Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/ai-resume-analyzer.git
   cd ai-resume-analyzer
````

2. **Create & activate virtual environment (optional but recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   * Create a `.env` file in the root directory.
   * Add your Groq API key:

     ```
     GROQ_API_KEY=your_api_key_here
     ```

---

## ▶️ Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

Then open your browser at **[http://localhost:8501](http://localhost:8501)**

---

## 📊 Example Workflow

1. Upload your **Resume (PDF)**.
2. Paste the **Job Description**.
3. Click **Analyze** 🚀.
4. Get:

   * 🎯 JD Match %
   * 🔑 Keywords matched & missing
   * 🧠 Profile Summary
   * 📊 Download CSV Report
5. Access past analyses via sidebar & export full database as CSV.

---

## 🗄️ Database

* Uses **SQLite** (`resume_analysis.db`).
* Stores:

  * Resume File Name
  * Job Role
  * JD Match %
  * Matched Keywords
  * Missing Keywords
  * Profile Summary
  * Created Timestamp

---

## 📌 Future Improvements

* Support for **DOCX resumes**.
* Advanced **visualizations & charts**.
* Multi-user support with authentication.
* Option to connect to **MySQL / PostgreSQL**.

---

## 🤝 Contributing

Pull requests are welcome! If you’d like to contribute, fork the repo and create a PR.

---

## 📜 License

This project is licensed under the MIT License.

---

👨‍💻 **Author**: [Your Name](https://github.com/your-username)

```