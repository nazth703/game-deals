import json
import requests
from concurrent.futures import ThreadPoolExecutor
import time

RAWG_API_KEY = "154cb5c212454612addc70d536944b0d"

def cargar_juegos():
    with open("games.json", "r", encoding="utf-8") as f:
        return json.load(f)

# =============================================
# Función de reintento automático
# Si falla la conexión, reintenta hasta 3 veces
# =============================================
def con_reintento(func, *args, max_intentos=3, espera=2):
    for intento in range(1, max_intentos + 1):
        try:
            return func(*args)
        except Exception as e:
            if intento < max_intentos:
                print(f"  ⚠️ Intento {intento} fallido, reintentando en {espera}s... ({e})")
                time.sleep(espera)
            else:
                print(f"  ❌ Falló después de {max_intentos} intentos: {e}")
                return None

def _obtener_rawg(titulo):
    url = "https://api.rawg.io/api/games"
    params = {"key": RAWG_API_KEY, "search": titulo, "page_size": 1}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    if data["results"]:
        juego = data["results"][0]

        # 3er nivel de paralelismo: procesar campos del JSON en paralelo
        def obtener_metacritic():
            return juego.get("metacritic", "N/A")

        def obtener_imagen():
            return juego.get("background_image", "N/A")

        def obtener_fecha():
            return juego.get("released", "N/A")

        def obtener_rating():
            return juego.get("rating", "N/A")

        def obtener_generos():
            generos = juego.get("genres", [])
            return ", ".join([g["name"] for g in generos]) if generos else "N/A"

        with ThreadPoolExecutor(max_workers=5) as executor:
            f_meta = executor.submit(obtener_metacritic)
            f_img = executor.submit(obtener_imagen)
            f_fecha = executor.submit(obtener_fecha)
            f_rating = executor.submit(obtener_rating)
            f_generos = executor.submit(obtener_generos)

            metacritic = f_meta.result()
            imagen = f_img.result()
            fecha = f_fecha.result()
            rating = f_rating.result()
            generos = f_generos.result()

        return {
            "metacritic_score": metacritic,
            "imagen": imagen,
            "fecha_lanzamiento": fecha,
            "rating": rating,
            "generos": generos
        }

    return {"metacritic_score": "N/A", "imagen": "N/A", "fecha_lanzamiento": "N/A", "rating": "N/A", "generos": "N/A"}

def obtener_rawg(titulo):
    resultado = con_reintento(_obtener_rawg, titulo)
    if resultado is None:
        return {"metacritic_score": "N/A", "imagen": "N/A", "fecha_lanzamiento": "N/A", "rating": "N/A", "generos": "N/A"}
    return resultado

def _obtener_hltb(titulo):
    from howlongtobeatpy import HowLongToBeat
    resultados = HowLongToBeat().search(titulo)
    if resultados and len(resultados) > 0:
        juego = max(resultados, key=lambda x: x.similarity)
        return {
            "main_story": juego.main_story,
            "main_extra": juego.main_extra,
            "completionist": juego.completionist
        }
    return {"main_story": "N/A", "main_extra": "N/A", "completionist": "N/A"}

def obtener_hltb(titulo):
    resultado = con_reintento(_obtener_hltb, titulo)
    if resultado is None:
        return {"main_story": "N/A", "main_extra": "N/A", "completionist": "N/A"}
    return resultado

def procesar_juego(juego):
    titulo = juego["title"]
    print(f"Procesando: {titulo}")

    with ThreadPoolExecutor(max_workers=2) as executor:
        future_rawg = executor.submit(obtener_rawg, titulo)
        future_hltb = executor.submit(obtener_hltb, titulo)
        datos_rawg = future_rawg.result()
        datos_hltb = future_hltb.result()

    return {
        "id": juego["id"],
        "title": titulo,
        "platform": juego["platform"],
        "metacritic_score": datos_rawg["metacritic_score"],
        "imagen": datos_rawg["imagen"],
        "fecha_lanzamiento": datos_rawg["fecha_lanzamiento"],
        "rating": datos_rawg["rating"],
        "generos": datos_rawg.get("generos", "N/A"),
        "hltb": datos_hltb
    }

def scraping_secuencial(juegos):
    print("\n=== VERSIÓN SECUENCIAL ===")
    inicio = time.time()
    resultados = []
    for juego in juegos:
        resultado = procesar_juego(juego)
        resultados.append(resultado)
    tiempo = time.time() - inicio
    print(f"\nTiempo secuencial: {tiempo:.2f} segundos")
    return resultados, tiempo

def scraping_paralelo(juegos, num_hilos=4):
    print(f"\n=== VERSIÓN PARALELA ({num_hilos} hilos) ===")
    inicio = time.time()
    with ThreadPoolExecutor(max_workers=num_hilos) as executor:
        resultados = list(executor.map(procesar_juego, juegos))
    tiempo = time.time() - inicio
    print(f"\nTiempo paralelo: {tiempo:.2f} segundos")
    return resultados, tiempo

def guardar_resultados(resultados, archivo):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    print(f"Resultados guardados en {archivo}")

if __name__ == "__main__":
    juegos = cargar_juegos()

    # Versión secuencial
    resultados_sec, tiempo_sec = scraping_secuencial(juegos)
    guardar_resultados(resultados_sec, "resultados_secuencial.json")

    # Versión paralela
    resultados_par, tiempo_par = scraping_paralelo(juegos, num_hilos=4)
    guardar_resultados(resultados_par, "resultados_paralelo.json")

    # Guardar tiempos para mostrar en la página web
    tiempos = {
        "secuencial": round(tiempo_sec, 2),
        "paralelo": round(tiempo_par, 2),
        "veces_mas_rapido": round(tiempo_sec / tiempo_par, 1),
        "juegos": len(juegos)
    }
    with open("tiempos.json", "w") as f:
        json.dump(tiempos, f)

    print(f"\n=== COMPARACIÓN FINAL ===")
    print(f"Secuencial: {tiempo_sec:.2f} segundos")
    print(f"Paralelo:   {tiempo_par:.2f} segundos")
    print(f"El paralelo fue {tiempo_sec/tiempo_par:.1f}x más rápido")