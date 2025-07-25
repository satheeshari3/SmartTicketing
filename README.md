⚙️ Smart Ticketing System

The Smart Ticketing System is a backend application that helps automate customer support. When a user submits a query, the system uses machine learning to classify the query (like billing, technical, or general) and then assigns it to an available support agent based on their current load.

It is built using FastAPI and MongoDB, and uses a simple machine learning model (TF-IDF + Logistic Regression) for classifying the queries.

## Features

- Classifies user queries into categories
- Assigns tickets to support agents based on workload
- Stores all data in MongoDB
- Simple and fast ML model
- FastAPI-powered backend

## Tech Stack

- FastAPI (Python framework for APIs)
- MongoDB (database)
- Motor (async driver for MongoDB)
- Scikit-learn (machine learning)
- TF-IDF + Logistic Regression (text classification)

## Folder Structure
SmartTicket/
├── app/
│   ├── main.py             # API entry point
│   ├── models.py           # Data models
│   ├── database.py         # MongoDB connection
│   ├── classifier.py       # ML logic
│   └── routes/
│       └── tickets.py      # API routes
├── data/
│   └── training_data.csv   # ML training data
├── requirements.txt        # Python dependencies
├── README.md               # Project info
└── .env                    # Environment variables
