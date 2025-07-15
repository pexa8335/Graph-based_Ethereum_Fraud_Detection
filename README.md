# FraudGraphML: Blockchain Fraud Detection System


## 📋 Overview

FraudGraphML is a comprehensive blockchain fraud detection system that combines machine learning with graph-based analysis to identify suspicious activities and fraudulent transactions on the Ethereum network. The system employs a hybrid approach, utilizing both traditional machine learning techniques and graph network analysis to provide real-time fraud detection and visualization.

## 🏗️ System Architecture

The project is structured into four main components:

### 1. Machine Learning Model (ML Model/)
- **Training Process**: 
  - Jupyter notebooks for model training and evaluation
  - Uses historical transaction data for fraud pattern recognition
  - Implements advanced ML algorithms (RandomForest, etc.)
  - Features both supervised learning and anomaly detection techniques

- **API Handling**: 
  - FastAPI-based REST API for model serving
  - Endpoints for transaction analysis and fraud prediction
  - Real-time processing of wallet addresses and transactions
  - Returns prediction probabilities and explanatory features

### 2. Graph Analysis System (Graph/)
- **Transaction Network Visualization**:
  - Interactive network graphs using PyVis
  - Visual representation of transaction patterns
  - Color-coded nodes based on fraud probability
  - Edge weights representing transaction values

- **Features**:
  - Real-time graph generation
  - Interactive node exploration
  - Direct links to Etherscan for transaction verification
  - Asynchronous processing for improved performance

### 3. Frontend Interface (FE_Novaledger/)
- **User Interface**:
  - TypeScript-based frontend
  - Interactive dashboard for result visualization
  - Real-time transaction monitoring
  - Risk assessment displays

- **Features**:
  - Address analysis interface
  - Transaction history visualization
  - Risk score display
  - Explainable AI visualizations

### 4. RAG Chatbot System (RAG_Chatbot/)
- **Knowledge Base**:
  - Comprehensive documentation
  - Blockchain anomaly detection information
  - System usage guides
  - Technical explanations

## 🔧 Technical Stack

- **Languages**:
  - Python (95.7% - ML & Graph Analysis)
  - TypeScript (1.8% - Frontend)
  - Jupyter Notebooks (Model Development)
  - PowerShell (0.6% - Scripts)

- **Key Libraries & Frameworks**:
  - FastAPI (API Development)
  - PyVis (Graph Visualization)
  - aiohttp (Async HTTP Client)
  - NetworkX (Graph Analysis)

## 🔍 Key Features

1. **Fraud Detection**:
   - Real-time transaction analysis
   - Machine learning-based prediction
   - Probability scoring for suspicious activities
   - Explainable AI results

2. **Graph Analysis**:
   - Interactive transaction network visualization
   - Node relationship analysis
   - Pattern detection in transaction flows
   - Visual risk indicators

3. **API Integration**:
   - RESTful API endpoints
   - Blockchain data retrieval
   - Real-time wallet analysis
   - Etherscan integration

4. **User Interface**:
   - Interactive dashboard
   - Transaction monitoring
   - Risk assessment visualization
   - Historical analysis tools

## 🚀 Getting Started

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/pexa8335/FraudGraphML.git
   cd FraudGraphML
   ```

2. **Install Dependencies**:
   ```bash
   # Set up Python environment
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt

   # Set up Frontend
   cd FE_Novaledger
   npm install
   ```

3. **Environment Setup**:
   ```bash
   # Create .env file
   ETHERSCAN_API_KEY=your_api_key
   FRAUD_API_URL=http://127.0.0.1:8000/analyze
   ```

4. **Run the System**:
   ```bash
   # Start ML API
   cd ML\ Model/API_Handling
   uvicorn main_api:app --reload

   # Start Frontend
   cd FE_Novaledger
   npm run dev
   ```

## 📊 System Flow

1. User inputs an Ethereum address for analysis
2. System retrieves transaction history via Etherscan API
3. ML model processes the address and related transactions
4. Graph analysis generates interactive network visualization
5. Results are displayed with fraud probability and explanations
6. User can explore transaction patterns and related addresses

## 🔐 Security Features

- Fraud probability thresholds:
  - High Risk: > 0.6
  - Medium Risk: 0.4 - 0.6
  - Low Risk: < 0.4

## 📈 Performance

- Asynchronous processing for multiple addresses
- Real-time transaction analysis
- Interactive visualization rendering
- Scalable API architecture

## 📚 Documentation

Detailed documentation is available in the RAG_Chatbot/knowledge_docs directory, covering:
- Blockchain anomaly detection methods
- System architecture details
- API specifications
- Usage guidelines

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests for any enhancements.

## 📄 License

MIT License

Copyright (c) 2025 FraudGraphML Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 👥 Authors

## 👥 Technical Team & Contributors

### Project Leadership & Architecture
**Phan Duc Anh** (@pexa8335)
- Project Lead & System Architect
- Core responsibilities:
  - Project management and team coordination
  - Machine learning architecture design
  - System architecture optimization
  - ML model development and implementation
  - Technical decision-making and roadmap planning

### RAG Architecture Team
**Nguyen Duc Phu**
- RAG Architecture Engineer
- Core responsibilities:
  - RAG system architecture development
  - Multi-agent system implementation
  - Knowledge base optimization

**Le Nu Khanh Linh**
- RAG Systems Engineer
- Core responsibilities:
  - Multi-agent RAG coordination
  - RAG performance optimization
  - Knowledge retrieval systems

### Development Team
**Vo Van Quoc**
- Full-Stack Development Engineer
- Core responsibilities:
  - Frontend development (TypeScript/React)
  - Backend API implementation
  - System integration
  - UI/UX implementation

**Tran Thai Tuong**
- Graph Systems Engineer
- Core responsibilities:
  - Graph architecture design
  - Network visualization implementation
  - Real-time graph rendering
  - Interactive visualization features

### Contact
For technical inquiries, please contact:
- Project Lead: [@pexa8335](https://github.com/pexa8335)
- Repository: [https://github.com/pexa8335/FraudGraphML](https://github.com/pexa8335/FraudGraphML)

Last Updated: 2025-07-15
