# 🚀 AWS Market Intelligence Pipeline (AI-Driven)

Este proyecto demuestra un pipeline de datos End-to-End diseñado para la ingesta, filtrado y análisis
de grandes volúmenes de datos económicos (INEGI DENUE - 460k+ registros). El sistema transforma datos crudos
almacenados en la nube en Insights Estratégicos para consultoría de Sales Performance Management (SPM)
utilizando Inteligencia Artificial Generativa.


This project demonstrates an **end-to-end data pipeline** designed for the ingestion, filtering, and analysis of large-scale economic datasets (INEGI DENUE - 460k+ records). The system transforms raw cloud-stored data into **Strategic Insights** for **Sales Performance Management (SPM)** consulting by leveraging Generative Artificial Intelligence.


## 🛠️ Architecture & Tech Stack
* **Cloud Provider:** Amazon Web Services (AWS).
* **Storage:** Amazon S3 (Data Lake / Raw Storage).
* **Compute:** AWS Lambda (Serverless Python 3.13).
* **AI Engine:** Amazon Bedrock (Anthropic Claude 3 Haiku).
* **Communication:** AWS Function URLs for real-time interaction.
* **Security:** IAM Role-based access & Environment Variables.


Key Engineering Features

1. High-Performance Streaming
The system processes a **460,000+ row CSV** file using `codecs` and `csv.DictReader` in a **streaming mode**. This ensures the Lambda function maintains a low memory footprint and avoids timeouts, allowing for cost-effective processing of large datasets on-the-fly.

2. Fuzzy Search & Normalization
Implemented a custom text normalization engine that handles Spanish accents and case sensitivity, ensuring robust data matching regardless of user input or source formatting.

3. Context-Aware GenAI Insights
Instead of generic summaries, the pipeline uses a specialized system prompt to act as a **Senior SPM Consultant**. It identifies specific market opportunities, territory potential, and sales incentive challenges based on the filtered data.

4. Security & Portability
* **Abstraction:** Infrastructure details (Buckets/File names) are handled via **Environment Variables**.
* **Sanitization:** Input parameters are sanitized to prevent prompt injection and infrastructure exposure.

---

## 🚀 Live Demo
The pipeline is exposed via a secure **Function URL**. You can trigger different market analysis reports by modifying the URL parameters:

👉 **[[YOUR_LAMBDA_URL_HERE](https://govi7vlwvs2fohkk4ckcox2dvm0oudpj.lambda-url.us-east-1.on.aws/?sector=Energia&estado=Mexico)]?sector=Energia&estado=Mexico**

---

## 📂 Repository Structure
* `lambda_function.py`: Core logic for S3 streaming, data filtering, and Bedrock inference.
* `upload_to_s3.py`: Local utility script for efficient data ingestion into AWS S3.
* `.gitignore`: Configured to exclude large datasets (.csv) and virtual environments (.venv).

---

🎯 About the Developer
**Esteban Rojano** *Data Architecture & AI Solutions Specialist* Focusing on transforming complex datasets into actionable business intelligence.

Architecture follows IAM best practices (least privilege), uses environment variables
for infrastructure abstraction, and implements input sanitization to prevent prompt injection.