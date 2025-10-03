
# 🐾 Spy Cat – Django REST API

---

## Run locally

### 1. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate   
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run migrations
```bash
python manage.py migrate
```


### 4. Start development server
```bash
python manage.py runserver
```

By default the app runs at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## API Endpoints

### Cats
- `POST /api/cats/` – create spy cat  
- `GET /api/cats/` – list all cats  
- `GET /api/cats/{id}/` – get one cat  
- `PATCH /api/cats/{id}/` – update salary only  
- `DELETE /api/cats/{id}/` – remove cat  

### Missions
- `POST /api/missions/` – create mission with 1–3 targets  
- `GET /api/missions/` – list all missions  
- `GET /api/missions/{id}/` – get one mission (with targets)  
- `DELETE /api/missions/{id}/` – delete mission (only if not assigned to cat)  
- `POST /api/missions/{id}/assign-cat/` – assign a cat to mission  

### Targets
- `GET /api/targets/` – list all targets  
- `GET /api/targets/{id}/` – get one target  
- `PATCH /api/targets/{id}/` – update notes / mark complete  


### Postman Collection
A Postman collection with example requests is available in the Spy Cat API.postman_collection.json file.

