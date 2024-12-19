import os
from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes.route import router
import uvicorn
from app.utils.defaultDBInsert.master_user import automate_saving_master_user
from server import initialize_db
from app.middlewares.corsMiddleware import add_middlewares

load_dotenv()

app=FastAPI()

add_middlewares(app)

app.include_router(router)

def start_server():
    try:
        initialize_db()

        automate_saving_master_user()

        PORT = int(os.getenv("PORT", 8000))
        print("Server running on Port",PORT)
        uvicorn.run("main:app", host="0.0.0.0", port=PORT,reload=True )

    except Exception as e:
        print(f"Error establishing Server: {e}")

if __name__ == '__main__':
    start_server()