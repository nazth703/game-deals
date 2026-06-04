import json

# Cargar el archivo con buenos datos (imágenes, scores, hltb)
with open("resultados_paralelo.json", "r", encoding="utf-8") as f:
    datos_buenos = json.load(f)

# Cargar el archivo con los precios de Steam
with open("resultados_final.json", "r", encoding="utf-8") as f:
    datos_precios = json.load(f)

# Crear un diccionario de precios por id
precios_por_id = {j["id"]: j.get("precios", []) for j in datos_precios}

# Combinar
for juego in datos_buenos:
    juego["precios"] = precios_por_id.get(juego["id"], [])

# Guardar resultado combinado
with open("resultados_final.json", "w", encoding="utf-8") as f:
    json.dump(datos_buenos, f, ensure_ascii=False, indent=2)

print("✅ Archivos combinados correctamente")