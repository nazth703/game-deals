import schedule
import time
import subprocess
import os

def actualizar():
    print("\n🔄 Iniciando actualización automática...")
    
    # Paso 1: Obtener precios de Steam
    print("📦 Actualizando precios de Steam...")
    subprocess.run(["python", "agregar_precios.py"])
    
    # Paso 2: Agregar precios de otras tiendas
    print("🏪 Actualizando otras tiendas...")
    subprocess.run(["python", "agregar_precios2.py"])
    
    # Paso 3: Regenerar el HTML
    print("🌐 Regenerando página web...")
    subprocess.run(["python", "generar_html.py"])
    
    # Paso 4: Subir a GitHub automáticamente
    print("📤 Subiendo a GitHub...")
    subprocess.run(["git", "add", "index.html", "resultados_final.json"])
    subprocess.run(["git", "commit", "-m", "Actualización automática de precios"])
    subprocess.run(["git", "push"])
    
    print("✅ Actualización completada!")

# Correr inmediatamente al iniciar
actualizar()

# Programar para cada 24 horas
schedule.every(24).hours.do(actualizar)

print("\n⏰ Actualizador iniciado - se ejecuta cada 24 horas")
print("Presiona Ctrl+C para detener\n")

while True:
    schedule.run_pending()
    time.sleep(60)