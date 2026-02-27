# GenAI Stack - No-Code/Low-Code AI Workflow Builder

A full-stack web application that enables users to visually create and interact with intelligent workflows using drag-and-drop components. Built with React.js, FastAPI, and PostgreSQL.

## 🚀 Features

- **Visual Workflow Builder**: Drag-and-drop interface using React Flow
- **Four Core Components**:
  - **User Query**: Entry point for user queries
  - **Knowledge Base**: Document processing with embeddings
  - **LLM Engine**: OpenAI GPT integration with web search
  - **Output**: Chat interface for responses
- **Real-time Chat**: Test workflows through interactive chat
- **Document Processing**: PDF text extraction and vector storage
- **Web Search Integration**: SerpAPI for real-time information
- **Responsive Design**: Modern, clean UI with Tailwind CSS

## 🏗️ Architecture

```
Frontend (React.js + React Flow)
    ↓
Backend (FastAPI)
    ↓
Database (PostgreSQL/Supabase)
    ↓
External Services (Gemini, OpenAI, SerpAPI, ChromaDB)
```

## 🛠️ Tech Stack

### Frontend
- **React.js** - UI framework
- **React Flow** - Drag-and-drop workflow builder
- **Tailwind CSS** - Styling
- **Lucide React** - Icons
- **Axios** - HTTP client

### Backend
- **FastAPI** - Python web framework
- **SQLAlchemy** - ORM
- **PostgreSQL** - Database
- **ChromaDB** - Vector store
- **PyMuPDF** - PDF processing

### External Services
- **OpenAI GPT** - Language model
- **OpenAI Embeddings** - Text embeddings
- **SerpAPI** - Web search
- **Supabase** - Database hosting

## 📦 Installation

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL or Supabase account
- Geminiai API key 
- OpenAI API key (optional)
- SerpAPI key (optional)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd genai-stack
```

### 2. Environment Setup
```bash
# Copy environment template
cp env.example .env

# Edit .env with your configuration
nano .env
```

Required environment variables:
```env
DATABASE_URL=postgresql://postgres:[PASSWORD]@[PROJECT-REF].supabase.co:5432/postgres
OPENAI_API_KEY=your_openai_api_key_here
SERP_API_KEY=your_serp_api_key_here
SECRET_KEY=your_secret_key_here
```

### 3. Install Dependencies
```bash
# Install all dependencies
npm run install:all

# Or install separately
npm install
cd frontend && npm install
cd ../backend && pip install -r requirements.txt
```

### 4. Database Setup
```bash
# Create database tables
cd backend
python -c "from database import engine; from models import Base; Base.metadata.create_all(bind=engine)"
```

### 5. Run the Application

#### Development Mode
```bash
# Run both frontend and backend
npm run dev

# Or run separately
npm run dev:frontend  # Frontend on http://localhost:3000
npm run dev:backend   # Backend on http://localhost:8000
```

#### Production Mode
```bash
# Build and run with Docker
docker-compose up --build
```

## 🐳 Docker Deployment

### Using Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Individual Dockerfiles
```bash
# Frontend only
docker build -f Dockerfile.frontend -t genai-stack-frontend .

# Backend only
docker build -f Dockerfile.backend -t genai-stack-backend .
```

## 🚀 Usage

### 1. Create a New Stack
- Click "New Stack" button
- Enter name and description
- Click "Create"

### 2. Build Your Workflow
- Drag components from the left panel to the canvas
- Connect components with edges
- Configure each component:
  - **User Query**: Set up query input
  - **Knowledge Base**: Upload documents, set API keys
  - **LLM Engine**: Configure model, prompt, temperature
  - **Output**: Set up response format

### 3. Test Your Workflow
- Click "Build Stack" to validate
- Click "Chat with Stack" to test
- Enter queries and see responses


### Supabase Setup
1. Create a new Supabase project
2. Get your database URL from Settings > Database
3. Update `DATABASE_URL` in `.env`

### OpenAI Setup 
1. Get API key from OpenAI platform
2. Add to `OPENAI_API_KEY` in `.env`

### SerpAPI Setup (Optional)
1. Get API key from SerpAPI
2. Add to `SERP_API_KEY` in `.env`



## 🎯 Roadmap

- [ ] User authentication
- [ ] Workflow templates
- [ ] Real-time collaboration
- [ ] Advanced analytics
- [ ] Custom components
- [ ] Workflow versioning
- [ ] Team management
- [ ] API rate limiting
- [ ] Caching layer
- [ ] Performance optimization

---

