from app.main import app

# Este arquivo serve como ponto de entrada para o servidor Uvicorn
# Importa o objeto app do módulo app.main

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
