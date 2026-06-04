import json

# Juegos Free to Play conocidos
free_to_play = [
    "Counter Strike 2", "Fortnite", "Apex Legends", "Valorant",
    "Dota 2", "Team Fortress 2", "Fall Guys", "Rocket League",
    "Overwatch 2"
]

# Exclusivos Nintendo con precio fijo
nintendo_exclusivos = [
    "Super Mario Bros Wonder", "The Legend of Zelda Breath of the Wild",
    "Mario Kart 8 Deluxe", "Splatoon 3", "Animal Crossing New Horizons",
    "Pokemon Scarlet", "Pokemon Violet", "Kirby Forgotten Land",
    "Metroid Dread", "Bayonetta 3", "Pikmin 4", "Fire Emblem Engage",
    "Fire Emblem Three Houses", "Xenoblade Chronicles 3", "Astral Chain",
    "Luigi Mansion 3", "Paper Mario Origami King", "Super Mario Odyssey",
    "Super Smash Bros Ultimate", "Donkey Kong Country Tropical Freeze",
    "Captain Toad Treasure Tracker", "Yoshi Crafted World",
    "New Super Mario Bros U Deluxe", "Mario Party Superstars",
    "WarioWare Get It Together"
]

# Exclusivos PlayStation con precio
playstation_precios = {
    "Uncharted 4": "$19.99",
    "Bloodborne": "$19.99",
    "Resident Evil 4 Remake": "$59.99",
    "Alan Wake 2": "$59.99",
    "Demon Souls Remake": "$39.99",
    "Astros Playroom": "Free",
    "Gran Turismo 7": "$59.99",
    "Resident Evil 3 Remake": "$39.99",
    "FIFA 23": "$59.99",
    "NBA 2K23": "$59.99",
    "Madden NFL 23": "$59.99",
    "MLB The Show 23": "$59.99",
}

# Juegos con precio en otras tiendas
otras_tiendas = {
    "Halo Infinite": ("Xbox Store", "$59.99", "https://www.xbox.com/games/halo-infinite"),
    "Rainbow Six Siege": ("Ubisoft Store", "$19.99", "https://www.ubisoft.com/rainbow-six-siege"),
    "Diablo III": ("Battle.net", "$19.99", "https://us.battle.net/shop/product/diablo-iii"),
    "Hazelight A Way Out": ("EA App", "$29.99", "https://www.ea.com/games/a-way-out"),
    "Ori and the Blind Forest": ("Xbox Store", "$19.99", "https://www.xbox.com/games/ori-and-the-blind-forest"),
}

with open("resultados_final.json", "r", encoding="utf-8") as f:
    juegos = json.load(f)

for juego in juegos:
    titulo = juego["title"]
    precio_actual = juego.get("precios", [{}])[0].get("precio_actual", "N/A")

    # Solo actualizar los que no tienen precio
    if precio_actual != "N/A":
        continue

    if titulo in free_to_play:
        juego["precios"] = [{
            "tienda": "Steam",
            "precio_actual": "Free to Play",
            "precio_original": "Free to Play",
            "descuento": 0,
            "en_oferta": False,
            "url": f"https://store.steampowered.com/search/?term={titulo.replace(' ', '+')}"
        }]
        print(f"✅ Free to Play: {titulo}")

    elif titulo in nintendo_exclusivos:
        juego["precios"] = [{
            "tienda": "Nintendo eShop",
            "precio_actual": "$59.99",
            "precio_original": "$59.99",
            "descuento": 0,
            "en_oferta": False,
            "url": f"https://www.nintendo.com/search/#q={titulo.replace(' ', '%20')}"
        }]
        print(f"✅ Nintendo: {titulo}")

    elif titulo in playstation_precios:
        precio = playstation_precios[titulo]
        juego["precios"] = [{
            "tienda": "PlayStation Store",
            "precio_actual": precio,
            "precio_original": precio,
            "descuento": 0,
            "en_oferta": False,
            "url": f"https://store.playstation.com/search/{titulo.replace(' ', '%20')}"
        }]
        print(f"✅ PlayStation: {titulo}")

    elif titulo in otras_tiendas:
        tienda, precio, url = otras_tiendas[titulo]
        juego["precios"] = [{
            "tienda": tienda,
            "precio_actual": precio,
            "precio_original": precio,
            "descuento": 0,
            "en_oferta": False,
            "url": url
        }]
        print(f"✅ Otra tienda: {titulo}")

with open("resultados_final.json", "w", encoding="utf-8") as f:
    json.dump(juegos, f, ensure_ascii=False, indent=2)

print("\n✅ Precios actualizados!")