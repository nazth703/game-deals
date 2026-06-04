import requests

def obtener_precio_steam(titulo):
    try:
        # Primero buscamos el ID del juego en Steam
        url = "https://store.steampowered.com/api/storesearch"
        params = {
            "term": titulo,
            "l": "english",
            "cc": "US"
        }
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data["total"] > 0:
                juego = data["items"][0]
                app_id = juego["id"]
                nombre = juego["name"]
                
                # Ahora obtenemos el precio con el ID
                url_precio = f"https://store.steampowered.com/api/appdetails"
                params_precio = {
                    "appids": app_id,
                    "cc": "US",
                    "filters": "price_overview"
                }
                response_precio = requests.get(url_precio, params=params_precio, headers=headers, timeout=10)
                
                if response_precio.status_code == 200:
                    data_precio = response_precio.json()
                    info = data_precio.get(str(app_id), {})
                    
                    if info.get("success"):
                        precio_data = info["data"].get("price_overview")
                        if precio_data:
                            return {
                                "tienda": "Steam",
                                "nombre": nombre,
                                "precio_actual": precio_data["final_formatted"],
                                "precio_original": precio_data["initial_formatted"],
                                "descuento": precio_data["discount_percent"],
                                "en_oferta": precio_data["discount_percent"] > 0,
                                "url": f"https://store.steampowered.com/app/{app_id}"
                            }
                        else:
                            return {
                                "tienda": "Steam",
                                "nombre": nombre,
                                "precio_actual": "Free to Play",
                                "precio_original": "Free to Play",
                                "descuento": 0,
                                "en_oferta": False,
                                "url": f"https://store.steampowered.com/app/{app_id}"
                            }
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Probar con algunos juegos
juegos_prueba = ["Elden Ring", "Hades", "Cyberpunk 2077", "Counter Strike 2"]

for juego in juegos_prueba:
    resultado = obtener_precio_steam(juego)
    if resultado:
        print(f"\n{resultado['nombre']}")
        print(f"  Precio actual:   {resultado['precio_actual']}")
        print(f"  Precio original: {resultado['precio_original']}")
        print(f"  Descuento:       {resultado['descuento']}%")
        print(f"  En oferta:       {resultado['en_oferta']}")
        print(f"  URL:             {resultado['url']}")
    else:
        print(f"\n{juego}: No encontrado en Steam")