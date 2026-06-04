import json
import requests
from concurrent.futures import ThreadPoolExecutor
import time

# =============================================
# Obtener precio de Steam
# =============================================
def obtener_precio_steam(titulo):
    try:
        url = "https://store.steampowered.com/api/storesearch"
        params = {"term": titulo, "l": "english", "cc": "US"}
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data["total"] > 0:
                juego = data["items"][0]
                app_id = juego["id"]

                url_precio = "https://store.steampowered.com/api/appdetails"
                params_precio = {"appids": app_id, "cc": "US", "filters": "price_overview"}
                response_precio = requests.get(url_precio, params=params_precio, headers=headers, timeout=10)

                if response_precio.status_code == 200:
                    data_precio = response_precio.json()
                    info = data_precio.get(str(app_id), {})

                    if info.get("success"):
                        precio_data = info["data"].get("price_overview")
                        if precio_data:
                            return {
                                "tienda": "Steam",
                                "precio_actual": precio_data["final_formatted"],
                                "precio_original": precio_data["initial_formatted"],
                                "descuento": precio_data["discount_percent"],
                                "en_oferta": precio_data["discount_percent"] > 0,
                                "url": f"https://store.steampowered.com/app/{app_id}"
                            }
                        else:
                            return {
                                "tienda": "Steam",
                                "precio_actual": "Free to Play",
                                "precio_original": "Free to Play",
                                "descuento": 0,
                                "en_oferta": False,
                                "url": f"https://store.steampowered.com/app/{app_id}"
                            }
        return {"tienda": "Steam", "precio_actual": "N/A", "precio_original": "N/A", "descuento": 0, "en_oferta": False, "url": "N/A"}
    except Exception as e:
        return {"tienda": "Steam", "precio_actual": "N/A", "precio_original": "N/A", "descuento": 0, "en_oferta": False, "url": "N/A"}

# =============================================
# Agregar precio a un juego
# =============================================
def agregar_precio(juego):
    titulo = juego["title"]
    print(f"Obteniendo precio: {titulo}")
    precio = obtener_precio_steam(titulo)
    juego["precios"] = [precio]
    return juego

# =============================================
# MAIN
# =============================================
if __name__ == "__main__":
    # Cargar los resultados que ya teníamos
    with open("resultados_paralelo.json", "r", encoding="utf-8") as f:

        juegos = json.load(f)

    print(f"Agregando precios a {len(juegos)} juegos en paralelo...\n")
    inicio = time.time()

    # Paralelo: varios juegos al mismo tiempo
    with ThreadPoolExecutor(max_workers=6) as executor:
        juegos_con_precios = list(executor.map(agregar_precio, juegos))

    tiempo = time.time() - inicio
    print(f"\nTiempo total: {tiempo:.2f} segundos")

    # Guardar resultado final
    with open("resultados_final.json", "w", encoding="utf-8") as f:
        json.dump(juegos_con_precios, f, ensure_ascii=False, indent=2)

    print("✅ Guardado en resultados_final.json")