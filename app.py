from flask import Flask, request, redirect
import json, os, uuid, datetime
app = Flask(__name__)
FILE = "pedidos.json"
PAYPAL = "https://www.paypal.me/Daniel1986Elian"
WHATSAPP = "https://wa.me/34643464401?text=Hola%20VendeMas%20Studio,%20quiero%20suscribirme"
EMAIL = "danielian.1218@gmail.com"
BIZUM = "624769152"

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
<title>VendeMas Studio</title><style>
body{margin:0;font-family:system-ui;background:#0f0f1a;color:#fff}
.phone{max-width:480px;margin:0 auto;min-height:100vh;background:#111126;padding-bottom:120px}
header{padding:20px;background:linear-gradient(135deg,#7c3aed,#f97316);border-radius:0 0 24px 24px;text-align:center}
.card{background:#1e1e38;margin:14px;padding:16px;border-radius:18px}
.plan{background:#2a2a4d;margin:10px 0;padding:14px;border-radius:14px}
.btn{display:block;text-align:center;background:linear-gradient(90deg,#7c3aed,#f97316);color:#fff;padding:14px;border-radius:14px;text-decoration:none;font-weight:700;border:0;width:100%;font-size:16px;margin-top:10px}
.btn2{display:block;text-align:center;background:#25D366;color:#fff;padding:14px;border-radius:14px;text-decoration:none;font-weight:700;margin-top:10px}
.btn3{display:block;text-align:center;background:#fff;color:#111;padding:14px;border-radius:14px;text-decoration:none;font-weight:700;margin-top:10px}
input,select,textarea{width:100%;padding:12px;border-radius:12px;border:1px solid #333;background:#0f0f1a;color:#fff;margin:8px 0;box-sizing:border-box}
nav{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:480px;background:#1a1a33;display:flex;justify-content:space-around;padding:12px 0}
nav a{color:#fff;text-decoration:none;font-size:13px}
small{color:#bbb}
</style></head><body><div class="phone">
<header><h1>VendeMas Studio</h1><p>Diseños 3D, desmontajes y videos cinematicos que hacen vender mas</p></header>
__CONTENIDO__
<div class="card"><h3>Contacto directo</h3><p>WhatsApp: 643464401<br>Gmail: danielian.1218@gmail.com<br>Bizum: 624769152<br>PayPal: paypal.me/Daniel1986Elian</p></div>
<nav><a href="/">Inicio</a><a href="/crear">Crear</a><a href="/pagar">Pagar</a><a href="/proyectos">Proyectos</a><a href="/admin">Admin</a></nav>
</div></body></html>
"""

def pagina(c):
    return BASE.replace("__CONTENIDO__", c)

@app.route("/")
def inicio():
    h = f"""
    <div class="card"><h2>Crea tu anuncio y vende mas</h2><p>1. Elige tu plan y paga<br>2. Pide tu diseño<br>3. Te lo entrego por WhatsApp o Gmail</p><a class="btn" href="/crear">Crear mi primer diseño</a><a class="btn2" href="{WHATSAPP}">Hablar por WhatsApp</a></div>
    <div class="card"><h2>Planes</h2>
    <div class="plan"><h3>Basico - 19 euros</h3><p>1 imagen 3D + 1 anuncio para Instagram / TikTok</p><a class="btn" href="{PAYPAL}/19">Pagar Basico con PayPal</a></div>
    <div class="plan"><h3>Pro - 49 euros</h3><p>3 diseños + desmontaje + 1 video logo</p><a class="btn" href="{PAYPAL}/49">Pagar Pro con PayPal</a></div>
    <div class="plan"><h3>Premium - 99 euros</h3><p>Todo ilimitado ese mes + video cinematografico + prioridad</p><a class="btn" href="{PAYPAL}/99">Pagar Premium con PayPal</a></div>
    <p><small>Si pagas con Bizum, haz Bizum al 624769152 y manda el comprobante por WhatsApp al 643464401.</small></p>
    </div>
    """
    return pagina(h)

@app.route("/pagar")
def pagar():
    h = f"""
    <div class="card"><h2>Pagar suscripcion</h2>
    <a class="btn" href="{PAYPAL}/19">PayPal Basico 19 euros</a>
    <a class="btn" href="{PAYPAL}/49">PayPal Pro 49 euros</a>
    <a class="btn" href="{PAYPAL}/99">PayPal Premium 99 euros</a>
    </div>
    <div class="card"><h3>Pagar con Bizum</h3><p>1. Abre tu banco y haz Bizum al numero:<br><b style="font-size:22px">624769152</b><br>2. Pon concepto: VendeMas + tu nombre<br>3. Manda la captura por WhatsApp al 643464401</p><a class="btn2" href="{WHATSAPP}">Enviar comprobante por WhatsApp</a></div>
    <div class="card"><h3>Dudas?</h3><p>Escribeme: {EMAIL}<br>WhatsApp: 643464401</p><a class="btn3" href="mailto:{EMAIL}">Enviar email</a></div>
    """
    return pagina(h)

@app.route("/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        datos = cargar()
        datos.append({"id": str(uuid.uuid4())[:8], "cliente": request.form.get("cliente",""), "idea": request.form.get("idea",""), "tipo": request.form.get("tipo",""), "estado": "Pendiente - Esperando pago", "fecha": datetime.datetime.now().strftime("%d/%m %H:%M")})
        guardar(datos)
        return redirect("/proyectos")
    return pagina('<div class="card"><h2>Crear pedido</h2><p>Primero paga tu plan en Pagar, luego crea tu pedido aqui.</p><form method="POST"><input name="cliente" placeholder="Tu empresa / tu nombre" required><textarea name="idea" placeholder="Quiero un anuncio lujoso para mi crema..." required></textarea><select name="tipo"><option>Imagen 3D</option><option>Desmontaje esquema</option><option>Video cinematografico logo</option><option>Anuncio Instagram TikTok</option><option>Banner web</option><option>Mockup</option></select><button class="btn" type="submit">Crear pedido</button></form></div>')

@app.route("/proyectos")
def proyectos():
    datos = cargar()
    h = '<div class="card"><h2>Mis Proyectos</h2></div>'
    for p in reversed(datos):
        h += f'<div class="card"><h3>{p["tipo"]}</h3><p>{p["idea"]}</p><p>{p["cliente"]} | {p["fecha"]} | {p["estado"]}</p></div>'
    return pagina(h if datos else h + '<div class="card"><p>Aun no tienes pedidos. Crea el primero.</p></div>')

@app.route("/admin")
def admin():
    datos = cargar()
    return pagina(f'<div class="card"><h2>Panel Admin - Daniel</h2><p>Pedidos: {len(datos)}<br>Ingresos si todos pagan 19 euros: {len(datos)*19} euros<br>WhatsApp: 643464401<br>Email: {EMAIL}<br>Bizum: {BIZUM}</p></div>')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
