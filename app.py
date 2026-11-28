from flask import Flask, request, redirect, jsonify
import json, os, uuid, datetime, time
import urllib.request, urllib.error

app = Flask(__name__)
FILE = "pedidos.json"
PAYPAL = "https://www.paypal.me/Daniel1986Elian"
WHATSAPP = "https://wa.me/34643464401?text=Hola%20VendeMas%20Studio,%20quiero%20informacion%20sobre%20un%20diseno"
EMAIL = "danielian.1218@gmail.com"
BIZUM = "624769152"

MUESTRAS = [
    {
        "titulo": "Anuncio Perfume Gold Edition",
        "categoria": "3D",
        "descripcion": "Ejemplo ilustrativo de estilo: iluminación de estudio y acabado publicitario para redes.",
        "img": "/static/01-perfume-gold.png"
    },
    {
        "titulo": "Despiece Técnico Smartwatch",
        "categoria": "Despiece",
        "descripcion": "Ejemplo ilustrativo de estilo: esquema por capas para explicar componentes y calidad.",
        "img": "/static/02-despiece-smartwatch.png"
    },
    {
        "titulo": "Intro Cinemática de Logo",
        "categoria": "Vídeo",
        "descripcion": "Ejemplo ilustrativo de estilo: intro animada para Reels, TikTok o lanzamientos.",
        "img": "",
        "video": "/static/03-intro-logo.mp4"
    }
]

def media(m):
    if m.get("video"):
        return f'<video class="muestra-img" src="{m["video"]}" controls playsinline preload="metadata"></video>'
    return f'<img class="muestra-img" src="{m["img"]}" alt="{m["titulo"]}" loading="lazy">'

def cargar():
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def guardar(d):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)

BASE = """
<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>VendeMas Studio | Diseño 3D y Anuncios</title><style>
body{margin:0;font-family:system-ui,-apple-system,sans-serif;background:#0a0a14;color:#f3f4f6}
.phone{max-width:480px;margin:0 auto;min-height:100vh;background:#111126;padding-bottom:120px;box-shadow:0 0 40px rgba(0,0,0,0.8)}
header{padding:26px 20px;background:linear-gradient(135deg,#7c3aed,#f97316);border-radius:0 0 24px 24px;text-align:center}
header h1{margin:0 0 6px 0;font-size:26px}
header p{margin:0;font-size:14px;opacity:0.95}
.card{background:#1a1a32;margin:14px;padding:18px;border-radius:18px;border:1px solid #2a2a48}
.plan{background:#232342;margin:12px 0;padding:16px;border-radius:14px;border:1px solid #34345c}
.plan h3{margin:0 0 6px 0;font-size:18px;color:#fb923c}
.badge{display:inline-block;padding:4px 10px;border-radius:999px;font-size:11px;font-weight:700;background:#7c3aed;color:#fff;margin-bottom:8px}
.btn{display:block;text-align:center;background:linear-gradient(90deg,#7c3aed,#f97316);color:#fff;padding:13px;border-radius:12px;text-decoration:none;font-weight:700;border:0;width:100%;font-size:15px;margin-top:10px;box-sizing:border-box}
.btn2{display:block;text-align:center;background:#25D366;color:#fff;padding:13px;border-radius:12px;text-decoration:none;font-weight:700;margin-top:10px;box-sizing:border-box}
.btn3{display:block;text-align:center;background:#2a2a4a;color:#fff;padding:12px;border-radius:12px;text-decoration:none;font-weight:600;margin-top:10px;border:1px solid #44446a}
.sample{background:#15152a;padding:12px;border-radius:12px;margin:10px 0;border-left:4px solid #f97316}
.muestra-img{width:100%;height:175px;object-fit:cover;border-radius:12px;margin-bottom:10px;background:#0f0f1a}
.filtros{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
.filtro-btn{background:#2a2a4a;color:#fff;border:0;padding:8px 12px;border-radius:10px;font-size:13px;font-weight:600}
.filtro-btn.activa{background:#7c3aed}
input,select,textarea{width:100%;padding:12px;border-radius:12px;border:1px solid #333355;background:#0d0d1a;color:#fff;margin:8px 0;box-sizing:border-box;font-family:inherit}
nav{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:480px;background:#15152a;display:flex;justify-content:space-around;padding:14px 0;border-top:1px solid #2a2a48;z-index:99}
nav a{color:#bbb;text-decoration:none;font-size:13px;font-weight:600}
nav a:hover,nav a:active{color:#fb923c}
small{color:#9ca3af;font-size:12px;line-height:1.45;display:block}
details{background:#15152a;border:1px solid #2a2a48;border-radius:12px;padding:10px 12px;margin-top:8px}
summary{cursor:pointer;font-size:13px;font-weight:700;color:#fb923c}
.legal{font-size:11.5px;color:#9ca3af;line-height:1.5;margin-top:14px;border-top:1px solid #2a2a44;padding-top:12px}
</style></head><body><div class="phone">
<header><h1>VendeMas Studio</h1><p>Diseños 3D, desmontajes y vídeos cinemáticos que multiplican tus ventas</p></header>
__CONTENIDO__
<div class="card">
<h3>Contacto y Atención</h3>
<p style="margin:6px 0 12px 0;font-size:14px;line-height:1.6">
WhatsApp: <b>+34 643 46 44 01</b><br>
Email: <b>danielian.1218@gmail.com</b><br>
Bizum: <b>624769152</b><br>
PayPal: <b>paypal.me/Daniel1986Elian</b>
</p>
<a class="btn2" href="https://wa.me/34643464401?text=Hola,%20tengo%20una%20consulta%20sobre%20VendeMas%20Studio">Hablar con Daniel por WhatsApp</a>
<div class="legal">
<p><b>IVA y facturación (España):</b> Salvo indicación expresa en contrario, los importes mostrados pueden no incluir el IVA español aplicable (21 % general o el régimen que corresponda según tu situación fiscal y la del cliente). Solicita factura indicando tus datos fiscales al realizar el pago.</p>
<details>
<summary>Aviso Legal y Condiciones de Servicio</summary>
<p style="margin:8px 0 0 0;font-size:12px;color:#cbd5e1;line-height:1.5">
Titular del servicio: Daniel [Completa apellidos y NIF/NIE/CIF antes de publicar] · Contacto: danielian.1218@gmail.com.<br>
Entregas digitales en 24–72 h según plan y complejidad, por WhatsApp o correo electrónico. Incluye ajustes razonables acordados tras la primera entrega. Al tratarse de contenido digital personalizado bajo encargo, revisa los detalles antes de iniciar la producción.
</p>
</details>
<details>
<summary>Política de Privacidad (RGPD)</summary>
<p style="margin:8px 0 0 0;font-size:12px;color:#cbd5e1;line-height:1.5">
Los datos introducidos en el formulario o enviados por WhatsApp/email se utilizan únicamente para gestionar tu encargo, comunicarnos contigo y atender consultas o facturación. Puedes solicitar acceso, rectificación o supresión escribiendo a danielian.1218@gmail.com.
</p>
</details>
</div>
</div>
<style>
#ia-btn{position:fixed;bottom:76px;right:14px;z-index:100;background:linear-gradient(90deg,#7c3aed,#f97316);color:#fff;border:0;border-radius:999px;padding:12px 16px;font-weight:700;font-size:14px;box-shadow:0 4px 14px rgba(0,0,0,.5)}
#ia-box{display:none;position:fixed;bottom:130px;right:12px;left:12px;max-width:380px;margin-left:auto;z-index:100;background:#1a1a32;border:1px solid #34345c;border-radius:16px;overflow:hidden}
#ia-msgs{height:260px;overflow-y:auto;padding:12px;font-size:14px;line-height:1.45}
.ia-b,.ia-u{padding:8px 11px;border-radius:12px;margin:6px 0;max-width:88%;white-space:pre-wrap}
.ia-b{background:#232342}
.ia-u{background:#7c3aed;margin-left:auto}
#ia-in{display:flex;gap:6px;padding:8px;border-top:1px solid #2a2a48}
#ia-in input{margin:0;flex:1}
#ia-in button{background:#f97316;color:#fff;border:0;border-radius:10px;padding:0 14px;font-weight:700}
</style>
<button id="ia-btn" type="button" onclick="iaToggle()">💬 Asistente</button>
<div id="ia-box">
<div id="ia-msgs"><div class="ia-b">Hola, soy el asistente de VendeMas Studio. Cuéntame qué producto quieres promocionar y te recomiendo un plan.</div></div>
<div id="ia-in"><input id="ia-txt" placeholder="Escribe aquí..." maxlength="500"><button type="button" onclick="iaSend()">Enviar</button></div>
</div>
<script>
var iaH=[];
function iaToggle(){var b=document.getElementById("ia-box");b.style.display=(b.style.display==="block")?"none":"block";}
function iaAdd(t,c){var d=document.createElement("div");d.className=c;d.textContent=t;var m=document.getElementById("ia-msgs");m.appendChild(d);m.scrollTop=m.scrollHeight;}
async function iaSend(){
  var i=document.getElementById("ia-txt");var t=i.value.trim();if(!t)return;
  i.value="";iaAdd(t,"ia-u");iaH.push({role:"user",content:t});
  try{
    var r=await fetch("/asistente",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({messages:iaH})});
    var j=await r.json();var a=j.respuesta||j.error||"Error";
    iaAdd(a,"ia-b");
    if(j.respuesta){iaH.push({role:"assistant",content:a});}else{iaH.pop();}
  }catch(e){iaAdd("No he podido conectar. Escríbenos por WhatsApp.","ia-b");iaH.pop();}
}
</script>
<nav><a href="/">Inicio</a><a href="/crear">Crear</a><a href="/pagar">Pagar</a><a href="/proyectos">Proyectos</a><a href="/admin">Admin</a></nav>
</div></body></html>
"""

def pagina(c):
    return BASE.replace("__CONTENIDO__", c)

@app.route("/")
def inicio():
    h = f"""
    <div class="card">
    <h2>Multiplica el impacto de tu producto</h2>
    <p style="font-size:14px;line-height:1.5;color:#ddd">1. Elige tu plan y realiza el pago.<br>2. Rellena los detalles de tu producto.<br>3. Recibe tus creatividades en alta resolución por WhatsApp o Gmail.</p>
    <a class="btn" href="/crear">Crear mi primer diseño</a>
    <a class="btn2" href="{WHATSAPP}">Consultar dudas por WhatsApp</a>
    </div>

    <div class="card">
    <h2>Muestras de Trabajos</h2>
    <div class="sample"><b>Anuncio Perfume Gold Edition</b><p style="margin:4px 0;font-size:13px;color:#aaa">Ejemplo ilustrativo de estilo con iluminación de estudio para campañas en redes.</p></div>
    <div class="sample"><b>Despiece Técnico Smartwatch</b><p style="margin:4px 0;font-size:13px;color:#aaa">Esquema visual por capas para mostrar componentes y calidad del producto.</p></div>
    <div class="sample"><b>Intro Cinemática Logo</b><p style="margin:4px 0;font-size:13px;color:#aaa">Pieza visual animada para portadas, lanzamientos y anuncios.</p></div>
    <a class="btn3" href="/proyectos">Ver galería visual y proyectos</a>
    </div>

    <div class="card">
    <h2>Planes de Diseño</h2>
    <div class="plan">
    <span class="badge">POPULAR</span>
    <h3>Básico - 19 €</h3>
    <p style="font-size:14px;margin:4px 0 10px 0">1 imagen 3D + 1 formato adaptado para Instagram / TikTok.</p>
    <a class="btn" href="{PAYPAL}/19">Pagar Básico (19 €) con PayPal</a>
    </div>
    <div class="plan">
    <h3>Pro - 49 €</h3>
    <p style="font-size:14px;margin:4px 0 10px 0">3 diseños + desmontaje esquemático + 1 vídeo logo.</p>
    <a class="btn" href="{PAYPAL}/49">Pagar Pro (49 €) con PayPal</a>
    </div>
    <div class="plan">
    <span class="badge" style="background:#f97316">AGENCIA</span>
    <h3>Premium - 99 €</h3>
    <p style="font-size:14px;margin:4px 0 10px 0">Creatividades ilimitadas ese mes + vídeo cinemático + prioridad.</p>
    <a class="btn" href="{PAYPAL}/99">Pagar Premium (99 €) con PayPal</a>
    </div>
    <small>Precios sujetos al régimen de IVA aplicable en España. Para Bizum, envía al 624769152 con tu nombre y manda el comprobante por WhatsApp al +34 643 46 44 01.</small>
    </div>
    """
    return pagina(h)

@app.route("/pagar")
def pagar():
    h = f"""
    <div class="card">
    <h2>Métodos de Pago</h2>
    <p style="font-size:14px;color:#ccc">Selecciona tu plan mediante PayPal:</p>
    <a class="btn" href="{PAYPAL}/19">PayPal Básico (19 €)</a>
    <a class="btn" href="{PAYPAL}/49">PayPal Pro (49 €)</a>
    <a class="btn" href="{PAYPAL}/99">PayPal Premium (99 €)</a>
    <small style="margin-top:10px">Indica si necesitas factura con tus datos fiscales (nombre/razón social, NIF/CIF y dirección) al enviar tu pedido o comprobante.</small>
    </div>
    <div class="card">
    <h3>Pago por Bizum</h3>
    <p style="font-size:14px;line-height:1.6">
    1. Abre la app de tu banco y haz Bizum al número:<br>
    <b style="font-size:24px;color:#fb923c">624769152</b><br>
    2. Concepto: <b>VendeMas + Tu Nombre</b><br>
    3. Envía la captura por WhatsApp al <b>+34 643 46 44 01</b>.
    </p>
    <a class="btn2" href="{WHATSAPP}">Enviar comprobante por WhatsApp</a>
    </div>
    """
    return pagina(h)

@app.route("/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        datos = cargar()
        datos.append({
            "id": str(uuid.uuid4())[:8],
            "cliente": request.form.get("cliente","").strip(),
            "idea": request.form.get("idea","").strip(),
            "tipo": request.form.get("tipo",""),
            "estado": "En cola - Pendiente confirmación",
            "fecha": datetime.datetime.now().strftime("%d/%m %H:%M")
        })
        guardar(datos)
        return redirect("/proyectos")
    return pagina("""
    <div class="card">
    <h2>Encargar Diseño</h2>
    <p style="font-size:14px;color:#ccc">Explícanos tu producto y cómo quieres que lo presentemos:</p>
    <form method="POST">
    <input name="cliente" placeholder="Nombre de tu marca o empresa" required>
    <textarea rows="4" name="idea" placeholder="Describe tu producto, colores, formato, texto y estilo deseado..." required></textarea>
    <select name="tipo">
      <option>Imagen 3D fotorrealista</option>
      <option>Desmontaje esquemático de producto</option>
      <option>Vídeo cinemático con logo animado</option>
      <option>Anuncio vertical para Instagram y TikTok</option>
      <option>Banner publicitario para tienda online</option>
      <option>Mockup digital de packaging</option>
    </select>
    <button class="btn" type="submit">Enviar encargo a producción</button>
    </form>
    </div>
    """)

@app.route("/proyectos")
def proyectos():
    datos = cargar()
    h = """
    <div class="card">
      <h2>Galería Visual de Muestras</h2>
      <small>Filtra por categoría para ver ejemplos de lo que podemos preparar para tu marca.</small>
      <div class="filtros">
        <button class="filtro-btn activa" type="button" onclick="filtrar('Todos', this)">Todos</button>
        <button class="filtro-btn" type="button" onclick="filtrar('3D', this)">3D</button>
        <button class="filtro-btn" type="button" onclick="filtrar('Despiece', this)">Despiece</button>
        <button class="filtro-btn" type="button" onclick="filtrar('Vídeo', this)">Vídeo</button>
      </div>
    </div>
    """
    for m in MUESTRAS:
        h += f"""
        <div class="card muestra-item" data-cat="{m['categoria']}">
          <span class="badge">{m['categoria']}</span>
          {media(m)}
          <h3 style="margin:0 0 6px 0">{m['titulo']}</h3>
          <small>{m['descripcion']}</small>
        </div>
        """
    h += """
    <script>
    function filtrar(cat, btn) {
      document.querySelectorAll('.filtro-btn').forEach(b => b.classList.remove('activa'));
      btn.classList.add('activa');
      document.querySelectorAll('.muestra-item').forEach(el => {
        el.style.display = (cat === 'Todos' || el.dataset.cat === cat) ? 'block' : 'none';
      });
    }
    </script>
    """
    h += '<div class="card"><h2>Tus Encargos Activos</h2></div>'
    if datos:
        for p in reversed(datos):
            h += f"""
            <div class="card" style="border-left:4px solid #7c3aed">
            <span class="badge">{p['tipo']}</span>
            <p style="margin:6px 0;font-size:14px">{p['idea']}</p>
            <small>Cliente: <b>{p['cliente']}</b> | {p['fecha']} | <span style="color:#fb923c">{p['estado']}</span></small>
            </div>
            """
    else:
        h += '<div class="card"><p style="font-size:14px;color:#aaa">No hay pedidos pendientes en este dispositivo. <a href="/crear" style="color:#fb923c">Crea el primero aquí</a>.</p></div>'
    return pagina(h)

@app.route("/admin")
def admin():
    datos = cargar()
    estimado = len(datos) * 19
    h = f"""
    <div class="card">
    <h2>Panel de Control - Daniel</h2>
    <p style="font-size:15px;line-height:1.8">
    Total encargos registrados: <b>{len(datos)}</b><br>
    Estimación base facturación: <b>{estimado} €</b><br>
    Canal WhatsApp: <b>+34 643 46 44 01</b><br>
    Email oficial: <b>{EMAIL}</b>
    </p>
    </div>
    """
    for p in reversed(datos):
        h += f"""
        <div class="card" style="font-size:13px">
        <b>ID #{p['id']} - {p['cliente']}</b> ({p['tipo']})<br>
        <i>{p['idea']}</i><br>
        <small>{p['fecha']} - Estado: {p['estado']}</small>
        </div>
        """
    return pagina(h)


IA_USO = {}
IA_DIA = {"d": "", "n": 0}
SYSTEM_IA = """Eres el asistente de VendeMas Studio, un servicio de diseño de imágenes 3D, despieces técnicos y vídeos cortos para vendedores online, atendido por Daniel desde España.
Planes: Básico 19 € (1 imagen 3D + 1 formato para Instagram/TikTok); Pro 49 € (3 diseños + despiece esquemático + 1 vídeo de logo); Premium 99 € (creatividades ilimitadas ese mes + vídeo + prioridad; el volumen exacto se confirma por WhatsApp). Precios sujetos al IVA aplicable. Entrega en 24-72 h por WhatsApp o email. Pago por PayPal o Bizum; factura bajo petición. WhatsApp: +34 643 46 44 01.
Reglas: responde en el idioma del cliente, de forma breve (máximo 4 frases) y amable. Recomienda el plan que mejor encaje según su producto. Las muestras de la galería son ejemplos ilustrativos de estilo, no trabajos hechos para clientes. No prometas resultados de ventas ni plazos distintos. No inventes servicios, precios ni condiciones que no estén aquí: si no lo sabes, dile que escriba por WhatsApp. Para encargar, indícale la página /crear. No pidas datos bancarios ni contraseñas."""

def llamar_ia(msgs):
    clave = os.environ.get("ANTHROPIC_API_KEY")
    if not clave:
        return None, "El asistente aún no está activo. Escríbenos por WhatsApp al +34 643 46 44 01."
    body = json.dumps({
        "model": os.environ.get("MODELO_IA", "claude-haiku-5-5"),
        "max_tokens": 400,
        "system": SYSTEM_IA,
        "messages": msgs
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages", data=body,
        headers={"x-api-key": clave, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read().decode("utf-8"))
        txt = "".join(b.get("text", "") for b in d.get("content", []) if b.get("type") == "text")
        return txt.strip(), None
    except urllib.error.HTTPError as e:
        print("IA HTTP error:", e.code, e.read().decode("utf-8", "ignore")[:300])
    except Exception as e:
        print("IA error:", repr(e))
    return None, "Ahora mismo no puedo responder. Escríbenos por WhatsApp al +34 643 46 44 01."

@app.route("/asistente", methods=["POST"])
def asistente():
    ip = (request.headers.get("X-Forwarded-For") or request.remote_addr or "x").split(",")[0].strip()
    ahora = time.time()
    hoy = datetime.date.today().isoformat()
    if IA_DIA["d"] != hoy:
        IA_DIA["d"] = hoy
        IA_DIA["n"] = 0
    if IA_DIA["n"] >= 300:
        return jsonify(error="El asistente ha llegado al límite de hoy. Escríbenos por WhatsApp al +34 643 46 44 01."), 429
    usos = [t for t in IA_USO.get(ip, []) if ahora - t < 3600]
    if len(usos) >= 15:
        return jsonify(error="Has hecho muchas preguntas seguidas. Prueba más tarde o escríbenos por WhatsApp."), 429
    data = request.get_json(silent=True) or {}
    msgs = []
    for m in (data.get("messages") or [])[-10:]:
        if isinstance(m, dict) and m.get("role") in ("user", "assistant") and isinstance(m.get("content"), str):
            msgs.append({"role": m["role"], "content": m["content"][:500]})
    while msgs and msgs[0]["role"] != "user":
        msgs.pop(0)
    if not msgs or msgs[-1]["role"] != "user":
        return jsonify(error="Escribe tu pregunta."), 400
    usos.append(ahora)
    IA_USO[ip] = usos
    IA_DIA["n"] += 1
    txt, err = llamar_ia(msgs)
    if err:
        return jsonify(error=err), 503
    return jsonify(respuesta=txt)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
