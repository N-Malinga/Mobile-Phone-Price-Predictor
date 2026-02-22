# Sri Lankan iPhone Price Predictor

This project is a Machine Learning application developed for the MSc in AI Machine Learning module. It predicts the market price of iPhones in Sri Lanka based on local data collected from e-commerce listings.

## Project Overview
- **Objective**: Collect a local dataset, apply a new machine learning algorithm, and evaluate using XAI.
- **Algorithm**: XGBoost Regressor (chosen for its superior performance over standard models on tabular data).
- **Data Source**: Real-world local listings (anonymized for privacy).

## Technical Stack
- **Backend**: FastAPI (Python)
- **Frontend**: React.js
- **Machine Learning**: XGBoost, Scikit-learn, SHAP (XAI)
- **Deployment**: Docker & Docker Compose

## How to Run the Project
Ensure you have **Docker Desktop** installed on your machine.

1. **Clone the repository**:
   ```bash
   git clone <your-repo-link>
   cd iphone-price-predictor
   ```

2. **Launch the application using Docker**:
   ```bash
   docker-compose up --build
   ```

3. **Access the system**:
   - **Frontend UI**: http://localhost:3000
   - **API Documentation**: http://localhost:8000/docs

## Project Structure

```text
iphone-price-predictor/
│
├── backend/                   # FastAPI backend server
│   ├── ExplainableAI.py       # SHAP explanations integration
│   ├── main.py                # FastAPI endpoints
│   ├── preprocess.py          # Data preprocessing logic
│   ├── scraper.py             # Data collection script
│   ├── training.py            # Model training script
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile             # Backend docker configuration
│   └── *.csv, *.pkl           # Datasets and saved models
│
├── frontend/                  # React.js frontend application
│   ├── src/
│   │   ├── App.jsx            # Main React component
│   │   ├── main.jsx           # Entry point
│   │   └── index.css          # Styling
│   ├── package.json           # Node.js dependencies
│   ├── vite.config.js         # Vite configuration
│   └── Dockerfile             # Frontend docker configuration
│
├── docker-compose.yml         # Docker compose configuration
└── README.md                  # Project documentation
```
