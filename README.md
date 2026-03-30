# JTA Take-Home Exercise — Data Dashboard

A full stack data dashboard built with **Vue 3** and **FastAPI**, consuming data from the [DummyJSON API](https://dummyjson.com). The app provides interactive analytics on users and products through charts, maps, tables, and AI-powered search.

---

## Live Demo

- **Frontend:** https://jta-take-home-exercise.vercel.app
- **Backend API docs:** https://jta-take-home-exercise.onrender.com/docs

> The Render free tier sleeps after 15 minutes of inactivity. The first request may take 30–60 seconds to wake up.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Vue 3, Vue Router, Chart.js, D3.js, PrimeVue, Axios |
| Backend | FastAPI, Pydantic, httpx |
| Data source | DummyJSON API |
| Deployment | Vercel (frontend), Render (backend) |

---

## Local Setup

### Prerequisites

- Python 3.10+
- Node.js 18+

### 1. Clone the repository

```bash
git clone https://github.com/your-username/jta-take-home-exercise.git
cd jta-take-home-exercise
```

### 2. Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv venv

# macOS/Linux:
source venv/bin/activate

# Windows (PowerShell):
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file inside `backend/` with the following content:

```
DUMMYJSON_BASE_URL=https://dummyjson.com
ANTHROPIC_API_KEY=your_api_key_here  # API key provided by email
```

```bash
# Start the server
uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`.
API docs available at `http://localhost:8000/docs`.

### 3. Frontend

```bash
cd frontend

# Install dependencies
npm install
```

Create a `.env.development` file inside `frontend/` with the following content:

```
VITE_API_URL=http://localhost:8000
```

```bash
# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`.

> Make sure the backend is running before starting the frontend.

---

## Project Structure

```
jta-take-home-exercise/
├── backend/
│   ├── main.py                  # FastAPI app, CORS config
│   ├── requirements.txt
│   ├── .env                     # Not committed — see Local Setup
│   ├── data/
│   │   └── universities.json    # Static university location data
│   ├── external/                # External API calls (DummyJSON + universities)
│   ├── schemas/                 # Pydantic models (user, product)
│   ├── services/                # Business logic and aggregations
│   └── routers/                 # API endpoints (users, products, search)
└── frontend/
    └── src/
        ├── main.js              # App entry point
        ├── router/              # Vue Router routes
        ├── services/api.js      # Axios instance and API calls
        ├── composables/         # Data-fetching logic (useHome, useUsers, useProducts)
        ├── components/          # Reusable UI components
        │   ├── charts/          # Chart.js and D3.js chart components
        │   └── tables/          # Aggregation table components
        └── views/               # Page components
            ├── HomeView.vue
            ├── users/
            └── products/
```

---

## Key Features

- **Home** — summary stats, review rating charts, product aggregation table, review aggregation by user segment, AI-powered natural language search
- **Users** — geographic map (address / company / university), segment distribution chart, full users table with cascading filters
- **Products** — aggregation table with total inventory value, top/bottom products chart, full products table with "needs attention" toggle
- **User profile** — personal info, reviews, and content-based product suggestions
- **Product profile** — full product details and reviews

---

## Analytical Decisions

**Low stock threshold:** Products are flagged as "needs attention" when stock is below `minimumOrderQuantity` or `availabilityStatus` is Low/Out of Stock. Using MOQ as a threshold proxy is a heuristic — a real system would use a reorder point formula requiring demand rate and lead time data not available here.

**User–product review linking:** DummyJSON has no foreign key between users and products. Reviews were cross-referenced by `reviewerEmail` against user emails, with a confirmed 100% match rate across 582 reviews and 208 users.

**University location data:** DummyJSON does not include university addresses. A static `universities.json` was created with city, state, and postal code for all 49 universities in the dataset.

**Product suggestions:** Content-based scoring using overlap between the user's reviewed categories, brands, and tags, weighted by product rating and boosted by behaviour from users of the same gender and age group. No ML is used.