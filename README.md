# RealPlanner
A route planning app for realtors

## 📖 Purpose & Overview

The RealPlanner App is designed to help real estate professionals efficiently plan and execute house tours with clients. It enables realtors to manage property visit details, automatically generate optimized routes based on location and open hours, and present a mobile-friendly, shareable schedule. The app streamlines daily visit planning, reduces logistical errors, and creates a more professional experience for both agents and clients.

---

## ✅ MVP Feature Scope (Prioritized)

### 1. House Visit Management
- Add/edit/delete house entries
- Fields: address, description, images, link, open hours
- Attach notes and tags per visit

### 2. Route Planning & Scheduling
- **Optimize visit order using Google Route Optimization API**
- Show real-time travel time/distance
- Use Google Maps for routing and map display
- **Advanced route optimization with time window constraints**

### 3. Responsive UI (Mobile-first)
- Clean, accessible layout for on-the-go use
- Google Maps integrated view
- Shareable itinerary preview (basic table view)

---

## 🧱 Core Architecture (MVP)

### 🧭 System Overview
```plaintext
[Frontend - React + Next.js]
        │
        ▼
[API Server - FastAPI (Python)]
        │
        ├──→ [Supabase Postgres (Data + Auth)]
        └──→ [Google Route Optimization API]
```

---

## 🧰 Tech Stack Summary

### ⚙️ Frontend (Web UI)
| Layer              | Tech                                |
|--------------------|--------------------------------------|
| Framework          | React + Next.js                     |
| Styling/UI         | TailwindCSS + shadcn/ui             |
| Map Integration    | Google Maps JS API                  |
| State Management   | React Context or Zustand            |
| Auth Client        | Supabase Auth JS                    |

---

### 🛠 Backend (API Layer)
| Layer              | Tech                                |
|--------------------|--------------------------------------|
| Web Framework      | FastAPI (Python)                    |
| Auth               | Supabase Auth (JWT)                 |
| API Contract       | REST + OpenAPI                      |
| **Route Optimization** | **Google Route Optimization API** |
| Google Maps Access | Google Maps Python Client           |
| ORM/DB Access      | SQLAlchemy or Supabase Client       |

---

### 🗄️ Database & Hosting
| Layer              | Tech                                |
|--------------------|--------------------------------------|
| Database           | PostgreSQL (via Supabase)           |
| Tables             | `users`, `properties`, `visit_plans`, `routes` |
| Auth & Storage     | Supabase (auth, image upload)       |
| Deployment (MVP)   | Docker Compose or Supabase-hosted   |

---

## 🔌 External APIs
| Use Case           | Provider                           |
|--------------------|------------------------------------|
| Map Rendering      | Google Maps JS API                 |
| **Route Optimization** | **Google Route Optimization API** |
| Address Geocoding  | Google Maps Places API             |

---

## 🔄 Extensibility Plan

| Area               | MVP Implementation               | Future Evolution                            |
|--------------------|----------------------------------|---------------------------------------------|
| **Route Optimization** | **Google Route Optimization API** | **Multi-vehicle routing, capacity constraints** |
| Auth               | Realtor login only               | Add client views, OAuth, roles              |
| Map API            | Google Maps                      | Swappable to Mapbox/OSM                     |
| Itinerary Sharing  | Static table export              | Google Docs/Calendar integration            |
| Deployment         | Local Docker dev                 | Add CI/CD, split into microservices         |

---
