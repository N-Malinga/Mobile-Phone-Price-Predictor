# Sri Lankan iPhone Price Predictor

[cite_start]This project is a Machine Learning application developed for the MSc in AI Machine Learning module[cite: 134]. [cite_start]It predicts the market price of iPhones in Sri Lanka based on local data collected from e-commerce listings[cite: 212, 213].

## Project Overview
- [cite_start]**Objective**: Collect a local dataset, apply a new machine learning algorithm, and evaluate using XAI[cite: 135].
- [cite_start]**Algorithm**: XGBoost Regressor (chosen for its superior performance over standard models on tabular data)[cite: 151, 157].
- [cite_start]**Data Source**: Real-world local listings (anonymized for privacy)[cite: 213, 221].

## Technical Stack
- [cite_start]**Backend**: FastAPI (Python) [cite: 246]
- [cite_start]**Frontend**: React.js [cite: 196]
- [cite_start]**Machine Learning**: XGBoost, Scikit-learn, SHAP (XAI) [cite: 171, 240]
- [cite_start]**Deployment**: Docker & Docker Compose [cite: 246]

## How to Run the Project
Ensure you have **Docker Desktop** installed on your machine.

1. **Clone the repository**:
   ```bash
   git clone <your-repo-link>
   cd iphone-price-predictor

2. **Launch the application using Docker**:

    docker-compose up --build

3. **Access the system**:

    Frontend UI: http://localhost:3000
    API Documentation: http://localhost:8000/docs

