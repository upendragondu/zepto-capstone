# Zepto Capstone Project

## Overview

This project consists of three modules:

### Module 1: Data Pipeline

* Scraped book information from an online bookstore.
* Cleaned and transformed the data.
* Stored the data in SQLite.
* Executed SQL queries for analysis.

### Module 2: Machine Learning Analytics

* Performed Exploratory Data Analysis (EDA) on the Titanic dataset.
* Built classification models:

  * Logistic Regression
  * Decision Tree
  * Random Forest
* Evaluated models using:

  * Accuracy
  * Precision
  * Recall
  * F1 Score
  * ROC-AUC
* Applied:

  * Class Weight Balancing
  * SMOTE
  * GridSearchCV
* Built a regression model for Fare prediction.
* Saved and reloaded trained models.

### Module 3: Support Assistant

* Created policy documents.
* Generated embeddings using Sentence Transformers.
* Stored embeddings in ChromaDB.
* Built a retrieval system.
* Implemented intent classification.
* Used LangGraph for workflow management.
* Built a FastAPI application.
* Added prompt engineering with few-shot examples.

## Technologies Used

* Python
* Pandas
* NumPy
* Scikit-Learn
* SQLite
* FastAPI
* ChromaDB
* Sentence Transformers
* LangGraph
* Matplotlib
* Seaborn

## Results

Random Forest achieved approximately 81% accuracy on Titanic classification.

## Run FastAPI

```bash
uvicorn support_assistant.api:app --reload
```

## API Documentation

Open:

http://127.0.0.1:8000/docs
