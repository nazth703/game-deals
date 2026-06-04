import json

with open("resultados_final.json", "r", encoding="utf-8") as f:
    juegos = json.load(f)

sin_precio = [j["title"] for j in juegos if not j.get("precios") or j["precios"][0]["precio_actual"] == "N/A"]

print(f"Total sin precio: {len(sin_precio)}")
for j in sin_precio:
    print(f"  - {j}")