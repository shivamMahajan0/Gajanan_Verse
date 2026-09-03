for BAckend blash the following request
## use python version 3.10
0.In cmd blash cd dir
1.On Windows: venv\Scripts\activate
2.pip install -r requirements.txt
3.In .env paste your OpenRouter api key
4.python -m backend.ingest
5.uvicorn backend.main:app --reload ## download uvicorn or use python backend.main:app 

for frontend 
1.in cmd blash cd dir of frontend-react
2.npm run dev