# Customer Churn Analysis

## 📌 Project Overview
This project analyzes customer churn data to uncover insights into which customers are more likely to leave a subscription service. Using **Python (pandas, matplotlib)**, the project demonstrates data cleaning, aggregation, visualization, and interpretation of results.

The goal is to showcase beginner-to-intermediate Python data analytics skills in a real-world business context.

---

## 🛠 Tools & Skills
- **Python** (pandas, matplotlib)
- **Data Cleaning & Transformation**
- **Exploratory Data Analysis (EDA)**
- **Visualization & Reporting**
- **GitHub Portfolio Project**

---

## 📊 Dataset
The dataset used is based on the [Telco Customer Churn Dataset](https://www.kaggle.com/datasets/blastchar/telco-customer-churn).

**Key Columns:**
- `Churn` – whether the customer left (Yes/No)  
- `Contract` – month-to-month, one-year, or two-year contracts  
- `Tenure` – how long the customer has been with the service (months)  
- `MonthlyCharges` – customer’s monthly payment  

---

## ❓ Key Questions
1. What percentage of customers are churning overall?  
2. How does churn vary by contract type?  
3. Do longer-tenured customers have lower churn?  
4. How do monthly charges relate to churn behavior?  

---

## 📈 Results

**Overall churn rate:** **26.54%**

**Churn by contract type:**
- **Month-to-month:** 42.71% churn rate  
- **One year:** 11.27% churn rate  
- **Two year:** 2.83% churn rate  

**Average tenure (months):** 32.37  
**Average monthly charges:** $64.76  

**Visualization:**  
![Churn Distribution](images/churn_distribution.png)

---

## 🚀 How to Run
1. Clone this repo.  
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Run the analysis script:
    ```bash
   python src/churn_analysis.py
4. Results will print in the console and the churn distribution chart will save to /images

---

## 💡 Key Insights
- Customers on month-to-month contracts are much more likely to churn compared to one- or two-year contracts.
- Longer tenure is strongly correlated with customer retention.
- Higher churn rates appear in customers paying higher monthly charges.

---

## 📬 About Me
I’m Eddie Grafiada, a Data Analyst with 7+ years of experience in SQL, Tableau, and data-driven decision making in the clean energy sector. Currently building a portfolio of Python analytics projects to transition into data engineering and cloud analytics roles.

📧 [sykeiv@gmail.com](mailto:sykeiv@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/eddie-grafiada-3805342bb/)
🔗 [GitHub](https://github.com/Eggie-G)


