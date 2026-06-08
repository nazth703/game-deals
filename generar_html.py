import json

with open("resultados_final.json", "r", encoding="utf-8") as f:
    juegos = json.load(f)

# Cargar tiempos
try:
    with open("tiempos.json", "r") as f:
        tiempos = json.load(f)
    tiempo_sec = tiempos["secuencial"]
    tiempo_par = tiempos["paralelo"]
    veces = tiempos["veces_mas_rapido"]
except:
    tiempo_sec = 1166.01
    tiempo_par = 292.59
    veces = 4.0

def generar_tarjetas(juegos):
    tarjetas = ""
    for juego in juegos:
        score = juego.get("metacritic_score", "N/A")
        imagen = juego.get("imagen", "")
        titulo = juego.get("title", "")
        plataforma = juego.get("platform", "")
        rating = juego.get("rating", "N/A")
        fecha = juego.get("fecha_lanzamiento", "N/A")
        hltb = juego.get("hltb", {})
        main_story = hltb.get("main_story", "N/A")
        main_extra = hltb.get("main_extra", "N/A")
        completionist = hltb.get("completionist", "N/A")
        precios = juego.get("precios", [])
        generos = juego.get("generos", "N/A")

        if score and score != "N/A" and score is not None:
            try:
                score_num = int(score)
                if score_num >= 80:
                    score_color = "#00ff88"
                    score_bg = "rgba(0,255,136,0.15)"
                elif score_num >= 60:
                    score_color = "#ffcc00"
                    score_bg = "rgba(255,204,0,0.15)"
                else:
                    score_color = "#ff3366"
                    score_bg = "rgba(255,51,102,0.15)"
            except:
                score_color = "#555"
                score_bg = "rgba(85,85,85,0.15)"
                score = "—"
        else:
            score = "—"
            score_color = "#555"
            score_bg = "rgba(85,85,85,0.15)"

        if not imagen or imagen == "N/A" or imagen == "None":
            steam_img = ""
            for p in precios:
                if p.get("url") and p["url"] != "N/A" and "/app/" in p["url"]:
                    app_id = p["url"].split("/app/")[-1]
                    steam_img = f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/header.jpg"
                    break
            imagen = steam_img if steam_img else "https://via.placeholder.com/300x200?text=No+Image"

        precio_principal = ""
        tienda_principal = ""
        en_oferta = False
        precio_original = ""
        descuento = 0
        for p in precios:
            if p.get("precio_actual") and p["precio_actual"] not in ["N/A", ""]:
                precio_principal = p["precio_actual"]
                tienda_principal = p.get("tienda", "")
                en_oferta = p.get("en_oferta", False)
                precio_original = p.get("precio_original", "")
                descuento = p.get("descuento", 0)
                break

        precio_html = ""
        if precio_principal:
            if en_oferta and precio_original:
                precio_html = f'<span class="precio-tachado">{precio_original}</span> <span class="precio-actual-card">{precio_principal}</span> <span class="descuento-card">-{descuento}%</span>'
            else:
                precio_html = f'<span class="precio-actual-card">{precio_principal}</span>'

        plataforma_icon = {
            "PS4": "🎮", "PS5": "🎮", "Switch": "🕹️",
            "Xbox": "🟢", "PC": "💻"
        }.get(plataforma, "🎮")

        tarjetas += f"""
        <div class="card"
             data-platform="{plataforma}"
             data-score="{score if score != '—' else 0}"
             data-title="{titulo}"
             data-imagen="{imagen}"
             data-fecha="{fecha}"
             data-rating="{rating}"
             data-main-story="{main_story}"
             data-main-extra="{main_extra}"
             data-completionist="{completionist}"
             data-generos="{generos}"
             onclick="openModal(this)">
            <div class="card-img-wrapper">
                <img src="{imagen}" alt="{titulo}" onerror="this.src='https://via.placeholder.com/300x200?text=No+Image'">
                <div class="card-platform-badge">{plataforma_icon} {plataforma}</div>
                {f'<div class="card-oferta-badge">OFERTA</div>' if en_oferta and precio_original else ''}
            </div>
            <div class="card-body">
                <h3 class="game-title">{titulo}</h3>
                <div class="card-scores">
                    <div class="score-item" style="color:{score_color}; background:{score_bg}">
                        <span class="score-num">{score}</span>
                        <span class="score-lbl">META</span>
                    </div>
                    <div class="score-item" style="color:#00aaff; background:rgba(0,170,255,0.1)">
                        <span class="score-num">{rating}</span>
                        <span class="score-lbl">RATING</span>
                    </div>
                    <div class="score-item" style="color:#aa66ff; background:rgba(170,102,255,0.1)">
                        <span class="score-num">{main_story}h</span>
                        <span class="score-lbl">HLTB</span>
                    </div>
                </div>
                <div class="card-precio">
                    <span class="tienda-lbl">{tienda_principal}</span>
                    <div class="precio-display">{precio_html}</div>
                </div>
            </div>
        </div>
        """
    return tarjetas

html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Game Deals - Proyecto Multicore</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #080808;
            --bg2: #111111;
            --bg3: #1a1a1a;
            --border: #222;
            --border2: #333;
            --red: #ff0033;
            --blue: #0088ff;
            --text: #e8e8e8;
            --text2: #888;
            --text3: #555;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }}

        header {{ background: var(--bg2); border-bottom: 1px solid var(--border); padding: 0 40px; height: 64px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 100; backdrop-filter: blur(10px); }}
        .header-logo {{ display: flex; align-items: center; gap: 12px; }}
        .logo-icon {{ width: 36px; height: 36px; background: linear-gradient(135deg, var(--red), var(--blue)); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 18px; }}
        .logo-text {{ font-size: 1.3rem; font-weight: 900; letter-spacing: -0.5px; }}
        .logo-text span:first-child {{ color: var(--text); }}
        .logo-text span:last-child {{ color: var(--red); }}
        .header-info {{ display: flex; align-items: center; gap: 20px; }}
        .header-stat {{ text-align: right; }}
        .header-stat .num {{ font-size: 1.1rem; font-weight: 700; color: var(--blue); }}
        .header-stat .lbl {{ font-size: 0.7rem; color: var(--text2); text-transform: uppercase; letter-spacing: 1px; }}

        .tiempos-section {{ background: var(--bg2); border-top: 1px solid var(--border); padding: 20px 40px; }}
        .tiempos-title {{ font-size: 0.75rem; font-weight: 700; color: var(--text2); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 14px; }}
        .tiempos-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; }}
        .tiempo-card {{ background: var(--bg3); border-radius: 10px; padding: 16px; border: 1px solid var(--border); }}
        .tiempo-card.secuencial {{ border-left: 3px solid var(--red); }}
        .tiempo-card.paralelo {{ border-left: 3px solid #00ff88; }}
        .tiempo-card.diferencia {{ border-left: 3px solid var(--blue); }}
        .tiempo-card .lbl {{ font-size: 0.7rem; color: var(--text2); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }}
        .tiempo-card .val {{ font-size: 1.4rem; font-weight: 800; }}
        .tiempo-card.secuencial .val {{ color: var(--red); }}
        .tiempo-card.paralelo .val {{ color: #00ff88; }}
        .tiempo-card.diferencia .val {{ color: var(--blue); }}
        .tiempo-card .sub {{ font-size: 0.75rem; color: var(--text3); margin-top: 4px; }}
        .barra-comparacion {{ margin-top: 14px; background: var(--bg3); border-radius: 10px; padding: 14px 16px; border: 1px solid var(--border); }}
        .barra-lbl {{ display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--text2); margin-bottom: 8px; }}
        .barra-wrapper {{ background: var(--border); border-radius: 4px; height: 8px; overflow: hidden; margin-bottom: 6px; }}
        .barra-secuencial {{ height: 100%; background: var(--red); border-radius: 4px; width: 100%; }}
        .barra-paralelo {{ height: 100%; background: #00ff88; border-radius: 4px; width: {round(tiempo_par/tiempo_sec*100)}%; }}

        .controls {{ background: var(--bg2); border-bottom: 1px solid var(--border); padding: 14px 40px; display: flex; gap: 12px; flex-wrap: wrap; align-items: center; }}
        .search-wrapper {{ position: relative; flex: 1; min-width: 200px; }}
        .search-wrapper input {{ width: 100%; background: var(--bg3); color: var(--text); border: 1px solid var(--border2); padding: 9px 14px 9px 36px; border-radius: 8px; font-size: 0.875rem; font-family: 'Inter', sans-serif; transition: border-color 0.2s; }}
        .search-wrapper input:focus {{ outline: none; border-color: var(--blue); }}
        .search-icon {{ position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: var(--text3); font-size: 14px; }}
        .controls select {{ background: var(--bg3); color: var(--text); border: 1px solid var(--border2); padding: 9px 14px; border-radius: 8px; font-size: 0.875rem; font-family: 'Inter', sans-serif; cursor: pointer; }}
        .controls select:focus {{ outline: none; border-color: var(--blue); }}
        .results-count {{ color: var(--text2); font-size: 0.8rem; margin-left: auto; }}
        .results-count span {{ color: var(--text); font-weight: 600; }}

        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 20px; padding: 24px 40px; }}
        .card {{ background: var(--bg2); border-radius: 12px; overflow: hidden; border: 1px solid var(--border); cursor: pointer; transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s; }}
        .card:hover {{ transform: translateY(-4px); border-color: var(--red); box-shadow: 0 8px 32px rgba(255,0,51,0.15); }}
        .card-img-wrapper {{ position: relative; height: 150px; overflow: hidden; }}
        .card-img-wrapper img {{ width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s; }}
        .card:hover .card-img-wrapper img {{ transform: scale(1.05); }}
        .card-platform-badge {{ position: absolute; top: 10px; left: 10px; background: rgba(0,0,0,0.75); backdrop-filter: blur(4px); color: var(--text); font-size: 0.7rem; font-weight: 600; padding: 4px 8px; border-radius: 6px; border: 1px solid var(--border2); }}
        .card-oferta-badge {{ position: absolute; top: 10px; right: 10px; background: var(--red); color: white; font-size: 0.65rem; font-weight: 700; padding: 4px 8px; border-radius: 6px; }}
        .card-body {{ padding: 14px; }}
        .game-title {{ font-size: 0.95rem; font-weight: 700; color: var(--text); margin-bottom: 12px; line-height: 1.3; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        .card-scores {{ display: flex; gap: 6px; margin-bottom: 12px; }}
        .score-item {{ flex: 1; display: flex; flex-direction: column; align-items: center; padding: 6px 4px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); }}
        .score-num {{ font-size: 0.9rem; font-weight: 700; line-height: 1; }}
        .score-lbl {{ font-size: 0.6rem; opacity: 0.7; margin-top: 2px; letter-spacing: 0.5px; }}
        .card-precio {{ display: flex; align-items: center; justify-content: space-between; background: var(--bg3); border-radius: 8px; padding: 8px 12px; border: 1px solid var(--border); }}
        .tienda-lbl {{ font-size: 0.72rem; color: var(--text2); }}
        .precio-display {{ display: flex; align-items: center; gap: 6px; }}
        .precio-tachado {{ font-size: 0.75rem; color: var(--text3); text-decoration: line-through; }}
        .precio-actual-card {{ font-size: 0.95rem; font-weight: 700; color: var(--blue); }}
        .descuento-card {{ font-size: 0.65rem; font-weight: 700; background: var(--red); color: white; padding: 2px 5px; border-radius: 4px; }}

        .modal-overlay {{ display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.85); backdrop-filter: blur(6px); z-index: 1000; align-items: center; justify-content: center; padding: 20px; }}
        .modal-overlay.active {{ display: flex; }}
        .modal {{ background: var(--bg2); border: 1px solid var(--border2); border-radius: 16px; width: 100%; max-width: 680px; max-height: 90vh; overflow-y: auto; position: relative; }}
        .modal-header {{ position: relative; height: 220px; overflow: hidden; border-radius: 16px 16px 0 0; }}
        .modal-header img {{ width: 100%; height: 100%; object-fit: cover; }}
        .modal-header-overlay {{ position: absolute; inset: 0; background: linear-gradient(to top, var(--bg2) 0%, transparent 60%); }}
        .modal-close {{ position: absolute; top: 14px; right: 14px; width: 32px; height: 32px; background: rgba(0,0,0,0.6); border: 1px solid var(--border2); border-radius: 50%; color: var(--text); font-size: 18px; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: background 0.2s; z-index: 10; }}
        .modal-close:hover {{ background: var(--red); border-color: var(--red); }}
        .modal-body {{ padding: 20px 24px 24px; }}
        .modal-title {{ font-size: 1.4rem; font-weight: 900; margin-bottom: 6px; }}
        .modal-platform {{ font-size: 0.8rem; color: var(--text2); margin-bottom: 16px; }}
        .modal-scores {{ display: flex; gap: 10px; margin-bottom: 20px; }}
        .modal-score-box {{ flex: 1; background: var(--bg3); border-radius: 10px; padding: 12px; border: 1px solid var(--border); text-align: center; }}
        .modal-score-box .val {{ font-size: 1.3rem; font-weight: 800; }}
        .modal-score-box .lbl {{ font-size: 0.65rem; color: var(--text2); text-transform: uppercase; letter-spacing: 1px; margin-top: 2px; }}
        .modal-section-title {{ font-size: 0.75rem; font-weight: 700; color: var(--text2); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }}
        .modal-hltb {{ display: flex; gap: 8px; margin-bottom: 20px; }}
        .hltb-item {{ flex: 1; background: var(--bg3); border-radius: 8px; padding: 10px; border: 1px solid var(--border); text-align: center; }}
        .hltb-item .val {{ font-size: 1rem; font-weight: 700; color: #aa66ff; }}
        .hltb-item .lbl {{ font-size: 0.65rem; color: var(--text2); margin-top: 2px; }}
        .modal-precios {{ display: flex; flex-direction: column; gap: 8px; }}
        .modal-precio-btn {{ display: flex; align-items: center; justify-content: space-between; background: var(--bg3); border: 1px solid var(--border); border-radius: 10px; padding: 12px 16px; text-decoration: none; color: var(--text); transition: border-color 0.2s; }}
        .modal-precio-btn:hover {{ border-color: var(--blue); }}
        .modal-precio-btn.oferta {{ border-color: var(--red); }}
        .modal-tienda {{ font-size: 0.85rem; font-weight: 600; }}
        .modal-precio-info {{ display: flex; align-items: center; gap: 8px; }}
        .modal-precio-original {{ font-size: 0.8rem; color: var(--text3); text-decoration: line-through; }}
        .modal-precio-actual {{ font-size: 1rem; font-weight: 700; color: var(--blue); }}
        .modal-precio-btn.oferta .modal-precio-actual {{ color: #00ff88; }}
        .modal-descuento {{ background: var(--red); color: white; font-size: 0.7rem; font-weight: 700; padding: 3px 7px; border-radius: 5px; }}
        .modal-info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 20px; }}
        .modal-info-item {{ background: var(--bg3); border-radius: 8px; padding: 10px 12px; border: 1px solid var(--border); }}
        .modal-info-item .lbl {{ font-size: 0.65rem; color: var(--text2); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }}
        .modal-info-item .val {{ font-size: 0.9rem; font-weight: 600; }}

        footer {{ border-top: 1px solid var(--border); padding: 20px 40px; display: flex; align-items: center; justify-content: space-between; }}
        .footer-left {{ font-size: 0.8rem; color: var(--text3); }}
        .footer-right {{ display: flex; gap: 16px; }}
        .footer-tag {{ font-size: 0.75rem; color: var(--text3); background: var(--bg3); padding: 4px 10px; border-radius: 20px; border: 1px solid var(--border); }}

        ::-webkit-scrollbar {{ width: 6px; }}
        ::-webkit-scrollbar-track {{ background: var(--bg); }}
        ::-webkit-scrollbar-thumb {{ background: var(--border2); border-radius: 3px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: var(--red); }}
    </style>
</head>
<body>

<header>
    <div class="header-logo">
        <div class="logo-icon">🎮</div>
        <div class="logo-text"><span>GAME</span><span>DEALS</span></div>
    </div>
    <div class="header-info">
        <div class="header-stat">
            <div class="num">{len(juegos)}</div>
            <div class="lbl">Juegos</div>
        </div>
        <div class="header-stat">
            <div class="num" style="color:var(--red)">LIVE</div>
            <div class="lbl">Precios</div>
        </div>
    </div>
</header>

<div class="controls">
    <div class="search-wrapper">
        <span class="search-icon">🔍</span>
        <input type="text" id="search" placeholder="Buscar juego...">
    </div>
    <select id="filterPlatform">
        <option value="">Todas las plataformas</option>
        <option value="Switch">Nintendo Switch</option>
        <option value="PS4">PlayStation 4</option>
        <option value="PS5">PlayStation 5</option>
        <option value="Xbox">Xbox</option>
        <option value="PC">PC</option>
    </select>
    <select id="sortBy">
        <option value="title">Ordenar: Nombre</option>
        <option value="score">Ordenar: Metacritic</option>
        <option value="rating">Ordenar: Rating</option>
    </select>
    <div class="results-count"><span id="resultsCount">{len(juegos)}</span> resultados</div>
</div>

<div class="grid" id="grid">
    {generar_tarjetas(juegos)}
</div>

<!-- SECCIÓN DE TIEMPOS AL FINAL -->
<div class="tiempos-section">
    <div class="tiempos-title">⚡ Comparación de Rendimiento — Multiprocesamiento</div>
    <div class="tiempos-grid">
        <div class="tiempo-card secuencial">
            <div class="lbl">Versión Secuencial</div>
            <div class="val">{tiempo_sec}s</div>
            <div class="sub">{round(tiempo_sec/60, 1)} minutos — 200 juegos uno por uno</div>
        </div>
        <div class="tiempo-card paralelo">
            <div class="lbl">Versión Paralela (4 hilos)</div>
            <div class="val">{tiempo_par}s</div>
            <div class="sub">{round(tiempo_par/60, 1)} minutos — 200 juegos en paralelo</div>
        </div>
        <div class="tiempo-card diferencia">
            <div class="lbl">Mejora de Rendimiento</div>
            <div class="val">{veces}x más rápido</div>
            <div class="sub">Ahorro de {round((tiempo_sec - tiempo_par)/60, 1)} minutos</div>
        </div>
    </div>
    <div class="barra-comparacion">
        <div class="barra-lbl">
            <span style="color:var(--red)">■ Secuencial: {tiempo_sec}s</span>
            <span style="color:#00ff88">■ Paralelo: {tiempo_par}s</span>
        </div>
        <div class="barra-wrapper">
            <div class="barra-secuencial"></div>
        </div>
        <div class="barra-wrapper">
            <div class="barra-paralelo"></div>
        </div>
    </div>
</div>

<footer>
    <div class="footer-left">Game Deals © 2025 — Proyecto Multiprocesamiento</div>
    <div class="footer-right">
        <span class="footer-tag">RAWG API</span>
        <span class="footer-tag">HowLongToBeat</span>
        <span class="footer-tag">Steam API</span>
    </div>
</footer>

<div class="modal-overlay" id="modalOverlay" onclick="closeModalOutside(event)">
    <div class="modal" id="modal">
        <div class="modal-header">
            <img id="modal-img" src="" alt="">
            <div class="modal-header-overlay"></div>
            <button class="modal-close" onclick="closeModal()">✕</button>
        </div>
        <div class="modal-body">
            <h2 class="modal-title" id="modal-title"></h2>
            <p class="modal-platform" id="modal-platform"></p>
            <div class="modal-scores" id="modal-scores"></div>
            <div class="modal-info-grid" id="modal-info"></div>
            <p class="modal-section-title">⏱ How Long to Beat</p>
            <div class="modal-hltb" id="modal-hltb"></div>
            <p class="modal-section-title">🏷 Precios</p>
            <div class="modal-precios" id="modal-precios"></div>
        </div>
    </div>
</div>

<script>
    const allCards = Array.from(document.querySelectorAll('.card'));

    function filterAndSort() {{
        const search = document.getElementById('search').value.toLowerCase();
        const platform = document.getElementById('filterPlatform').value;
        const sortBy = document.getElementById('sortBy').value;
        const grid = document.getElementById('grid');

        let visible = allCards.filter(card => {{
            const title = card.dataset.title.toLowerCase();
            const cardPlatform = card.dataset.platform;
            return title.includes(search) && (platform === '' || cardPlatform === platform);
        }});

        visible.sort((a, b) => {{
            if (sortBy === 'title') return a.dataset.title.localeCompare(b.dataset.title);
            if (sortBy === 'score') return b.dataset.score - a.dataset.score;
            if (sortBy === 'rating') return parseFloat(b.dataset.rating||0) - parseFloat(a.dataset.rating||0);
            return 0;
        }});

        allCards.forEach(c => c.style.display = 'none');
        visible.forEach(c => {{ c.style.display = 'block'; grid.appendChild(c); }});
        document.getElementById('resultsCount').textContent = visible.length;
    }}

    document.getElementById('search').addEventListener('input', filterAndSort);
    document.getElementById('filterPlatform').addEventListener('change', filterAndSort);
    document.getElementById('sortBy').addEventListener('change', filterAndSort);

    function openModal(card) {{
        const titulo = card.dataset.title;
        const imagen = card.dataset.imagen;
        const plataforma = card.dataset.platform;
        const fecha = card.dataset.fecha;
        const rating = card.dataset.rating;
        const score = card.dataset.score;
        const mainStory = card.dataset.mainStory;
        const mainExtra = card.dataset.mainExtra;
        const completionist = card.dataset.completionist;
        const generos = card.dataset.generos || 'N/A';

        document.getElementById('modal-img').src = imagen;
        document.getElementById('modal-title').textContent = titulo;
        document.getElementById('modal-platform').textContent = plataforma + ' • Lanzamiento: ' + fecha;

        const scoreColor = score >= 80 ? '#00ff88' : score >= 60 ? '#ffcc00' : score > 0 ? '#ff3366' : '#555';
        document.getElementById('modal-scores').innerHTML = `
            <div class="modal-score-box" style="border-color:${{scoreColor}}20">
                <div class="val" style="color:${{scoreColor}}">${{score || '—'}}</div>
                <div class="lbl">Metacritic</div>
            </div>
            <div class="modal-score-box" style="border-color:#00aaff20">
                <div class="val" style="color:#00aaff">${{rating || 'N/A'}}</div>
                <div class="lbl">Rating</div>
            </div>
        `;

        document.getElementById('modal-info').innerHTML = `
            <div class="modal-info-item">
                <div class="lbl">Plataforma</div>
                <div class="val">${{plataforma}}</div>
            </div>
            <div class="modal-info-item">
                <div class="lbl">Lanzamiento</div>
                <div class="val">${{fecha}}</div>
            </div>
            <div class="modal-info-item" style="grid-column: span 2">
                <div class="lbl">Géneros</div>
                <div class="val" style="color:#aa66ff">${{generos}}</div>
            </div>
        `;

        document.getElementById('modal-hltb').innerHTML = `
            <div class="hltb-item">
                <div class="val">${{mainStory}}h</div>
                <div class="lbl">Historia</div>
            </div>
            <div class="hltb-item">
                <div class="val">${{mainExtra}}h</div>
                <div class="lbl">Historia + Extra</div>
            </div>
            <div class="hltb-item">
                <div class="val">${{completionist}}h</div>
                <div class="lbl">Completista</div>
            </div>
        `;

        const tienda = card.querySelector('.tienda-lbl')?.textContent || '';
        const precioActual = card.querySelector('.precio-actual-card')?.textContent || '';
        const precioOriginal = card.querySelector('.precio-tachado')?.textContent || '';
        const descuento = card.querySelector('.descuento-card')?.textContent || '';

        if (precioActual) {{
            const esOferta = !!precioOriginal;
            document.getElementById('modal-precios').innerHTML = `
                <div class="modal-precio-btn ${{esOferta ? 'oferta' : ''}}">
                    <span class="modal-tienda">${{tienda}}</span>
                    <div class="modal-precio-info">
                        ${{precioOriginal ? `<span class="modal-precio-original">${{precioOriginal}}</span>` : ''}}
                        <span class="modal-precio-actual">${{precioActual}}</span>
                        ${{descuento ? `<span class="modal-descuento">${{descuento}}</span>` : ''}}
                    </div>
                </div>
            `;
        }} else {{
            document.getElementById('modal-precios').innerHTML = '<p style="color:var(--text3);font-size:0.85rem">No disponible</p>';
        }}

        document.getElementById('modalOverlay').classList.add('active');
        document.body.style.overflow = 'hidden';
    }}

    function closeModal() {{
        document.getElementById('modalOverlay').classList.remove('active');
        document.body.style.overflow = '';
    }}

    function closeModalOutside(e) {{
        if (e.target === document.getElementById('modalOverlay')) closeModal();
    }}

    document.addEventListener('keydown', e => {{ if (e.key === 'Escape') closeModal(); }});
</script>

</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Página HTML generada: index.html")