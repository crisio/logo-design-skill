/*
 * <kot-avatar>: la mascota de peluche (Kot) de un agente, animada y sin dependencias.
 *
 * Toma el PNG transparente del Kot y lo anima con transformaciones CSS: flota, respira, se mece, parpadea,
 * voltea un poco hacia el cursor, se aplasta al pasar el mouse y da un saltito al tocarlo. Respeta
 * «reducir movimiento», se pausa cuando no se ve y funciona sin internet (archivo local, script clásico).
 *
 * Uso:
 *   <script src="kot-avatar.js" defer></script>
 *   <kot-avatar src="kot-512.png" kot='{"ojos":[…],"caja":[…]}' alt="Hilo" style="width:160px"></kot-avatar>
 *
 * Atributos:
 *   src        PNG transparente del Kot (cuadrado).
 *   kot        JSON con "ojos" ([{cx,cy,rx,ry,parpado,muestra}], normalizados 0–1) y "caja" ([x0,y0,x1,y1], 0–1).
 *              Lo genera scripts/kot_build.py en kot.json.
 *   alt        nombre para lectores de pantalla; sin alt, el Kot se trata como decorativo.
 *   sombra     dibuja una sombra suave bajo el Kot.
 *   circulo    recorta el Kot en un círculo con fondo (color en la variable CSS --kot-fondo).
 *   tiempo     pose fija en ese milisegundo del ciclo (para capturar cuadros); desactiva la animación en vivo.
 *   parpadeo   0–1, cierre de los párpados en la pose fija (por defecto, el parpadeo grabado del ciclo).
 *   quieto     sin animación (pose de reposo).
 * El Kot siempre se dibuja en un cuadrado centrado dentro de la caja del elemento, aunque la caja no sea cuadrada.
 * En filas flex con texto largo, ponle flex:none (o un ancho mínimo) para que no se encoja.
 */
(function () {
  "use strict";
  if (typeof customElements === "undefined" || customElements.get("kot-avatar")) return;

  var CICLO = 3000;          // ms: todo lo grabado se repite cada 3 s (loop perfecto)
  var TAU = Math.PI * 2;
  var CUADRO = 1000 / 24;    // duración de un cuadro de la animación grabada

  // Movimiento base del ciclo grabado; t en ms. x e y en fracción del lado; r en grados.
  function pose(t) {
    var f = (((t % CICLO) + CICLO) % CICLO) / CICLO;
    var flota = -0.022 * Math.sin(TAU * f);
    var respira = 0.012 * Math.sin(TAU * 2 * f + 0.6);
    var mece = 1.1 * Math.sin(TAU * f + Math.PI / 3);
    return { x: 0, y: flota, sx: 1 - respira * 0.6, sy: 1 + respira, r: mece };
  }

  // Curva de un parpadeo: cierra en 70 ms y abre en 100 ms.
  function curvaParpadeo(d) {
    if (d < 0 || d > 170) return 0;
    return d < 70 ? d / 70 : 1 - (d - 70) / 100;
  }

  // Parpadeo grabado: uno por ciclo. Empieza para que el cierre total caiga justo en un cuadro (el 50, a 2083 ms)
  // y la animación de 24 cuadros por segundo sí muestre el ojo convertido en línea.
  var INICIO_PARPADEO = 2 * CUADRO * 24 - 70 + 2 * CUADRO; // 2013.33 ms
  function parpadeoGrabado(t) {
    return curvaParpadeo((((t % CICLO) + CICLO) % CICLO) - INICIO_PARPADEO);
  }

  // Un solo oyente de pointermove para todos los Kots que están animando.
  var vivos = new Set();
  function alMoverGlobal(e) { vivos.forEach(function (k) { k._alMover(e); }); }
  function activar(k) {
    if (!vivos.size) window.addEventListener("pointermove", alMoverGlobal, { passive: true });
    vivos.add(k);
  }
  function desactivar(k) {
    if (vivos.delete(k) && !vivos.size) window.removeEventListener("pointermove", alMoverGlobal);
  }

  var CSS = [
    ":host{display:inline-block;position:relative;aspect-ratio:1/1;width:160px;container-type:size;contain:layout paint;-webkit-tap-highlight-color:transparent}",
    ".marco{position:absolute;inset:0;margin:auto;width:min(100cqw,100cqh);height:min(100cqw,100cqh)}",
    ":host([circulo]) .marco{border-radius:50%;overflow:hidden;background:var(--kot-fondo,transparent)}",
    ".cuerpo{position:absolute;inset:0;will-change:transform}",
    ".cuerpo>img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;display:block;user-select:none;-webkit-user-drag:none;pointer-events:none}",
    ".parpado{position:absolute;border-radius:50%;transform-origin:50% 0;transform:scaleY(0);pointer-events:none}",
    // Parpadeo con fieltro real: «tapa» cubre el ojo con un parche de fieltro tomado de al lado y «ojo» es una copia
    // del ojo que se aplasta hasta ser una línea. Las dos solo se ven mientras parpadea.
    ".tapa,.ojo{position:absolute;overflow:hidden;pointer-events:none;visibility:hidden}",
    ".tapa{-webkit-mask-image:radial-gradient(closest-side,#000 72%,transparent 100%);mask-image:radial-gradient(closest-side,#000 72%,transparent 100%)}",
    ".ojo{transform-origin:50% 58%;-webkit-mask-image:radial-gradient(closest-side,#000 80%,transparent 100%);mask-image:radial-gradient(closest-side,#000 80%,transparent 100%)}",
    ".tapa img,.ojo img{position:absolute;max-width:none;display:block}",
    ".sombra{position:absolute;border-radius:50%;background:radial-gradient(closest-side,rgba(0,0,0,.28),rgba(0,0,0,0));pointer-events:none;display:none}",
    ":host([sombra]) .sombra{display:block}"
  ].join("");

  function num(v, d) { var n = parseFloat(v); return isFinite(n) ? n : d; }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }

  class KotAvatar extends HTMLElement {
    static get observedAttributes() { return ["src", "kot", "tiempo", "parpadeo", "quieto", "sombra", "alt"]; }

    constructor() {
      super();
      this._raiz = this.attachShadow({ mode: "open" });
      this._raf = 0;
      this._listo = false;
      this._visible = true;
      this._mira = { x: 0, y: 0, tx: 0, ty: 0 };
      this._golpe = -1e9;
      this._salto = -1e9;
      this._alturaSalto = 0.06;
      this._parpadeo = { inicio: -1e9, doble: false, proximo: 0 };
      this._cuadro = this._cuadro.bind(this);
      this._alCambiarMovimiento = this._arrancar.bind(this);
      this._alCambiarVisibilidad = this._alCambiarVisibilidad.bind(this);
    }

    connectedCallback() {
      this._listo = true;
      this._accesibilidad();
      this._montar();
      this._observar();
      this._arrancar();
    }

    disconnectedCallback() {
      this._parar();
      this._listo = false;
      if (this._io) { this._io.disconnect(); this._io = null; }
      if (this._mq) {
        if (this._mq.removeEventListener) this._mq.removeEventListener("change", this._alCambiarMovimiento);
        this._mq = null;
      }
      document.removeEventListener("visibilitychange", this._alCambiarVisibilidad);
    }

    attributeChangedCallback(nombre) {
      // Durante la mejora del elemento llegan varios cambios seguidos: se ignoran hasta connectedCallback
      if (!this._listo) return;
      if (nombre === "alt") { this._accesibilidad(); return; }
      this._montar();
      this._arrancar();
    }

    _accesibilidad() {
      var alt = this.getAttribute("alt");
      if (alt) {
        this.setAttribute("role", "img");
        this.setAttribute("aria-label", alt);
        this.removeAttribute("aria-hidden");
        this._etiquetaPropia = true;
      } else {
        // Sin alt (o con alt vacío) el Kot es decorativo: se quita lo que el propio componente puso antes
        if (this._etiquetaPropia) {
          this.removeAttribute("role");
          this.removeAttribute("aria-label");
          this._etiquetaPropia = false;
        }
        if (!this.hasAttribute("aria-label")) this.setAttribute("aria-hidden", "true");
      }
    }

    _datos() {
      var d = {};
      try { d = JSON.parse(this.getAttribute("kot") || "{}") || {}; } catch (e) { d = {}; }
      if (!Array.isArray(d.ojos)) d.ojos = [];
      if (!Array.isArray(d.caja) || d.caja.length !== 4) d.caja = [0.1, 0.1, 0.9, 0.9];
      return d;
    }

    _montar() {
      var d = this._datos();
      var caja = d.caja;
      var piso = clamp(num(caja[3], 0.9), 0, 1);
      // El saltito no puede subir más que el margen libre arriba del personaje (si no, se corta)
      this._alturaSalto = clamp(num(caja[1], 0.1) - 0.022 - 0.02 - 0.01, 0, 0.06);
      var src = this.getAttribute("src") || "";
      var html = "<style>" + CSS + "</style><div class=\"marco\" part=\"marco\">" +
        "<div class=\"sombra\"></div><div class=\"cuerpo\"><img alt=\"\" draggable=\"false\">";
      for (var i = 0; i < d.ojos.length; i++) {
        html += Array.isArray(d.ojos[i].muestra)
          ? "<div class=\"tapa\"><img alt=\"\"></div><div class=\"ojo\"><img alt=\"\"></div>"
          : "<i class=\"parpado\"></i>";
      }
      html += "</div></div>";
      this._raiz.innerHTML = html;
      this._cuerpo = this._raiz.querySelector(".cuerpo");
      this._sombra = this._raiz.querySelector(".sombra");
      this._cuerpo.querySelector("img").src = src;
      this._cuerpo.style.transformOrigin = "50% " + (piso * 100).toFixed(2) + "%";
      this._parpados = [];
      var tapas = this._raiz.querySelectorAll(".tapa"), copias = this._raiz.querySelectorAll(".ojo");
      var planos = this._raiz.querySelectorAll(".parpado"), it = 0, ip = 0;
      // Caja centrada en (cx, cy) que muestra la imagen completa desplazada para enseñar el punto (fx, fy)
      function ventana(c, cx, cy, hx, hy, fx, fy) {
        c.style.left = ((cx - hx) * 100).toFixed(3) + "%";
        c.style.top = ((cy - hy) * 100).toFixed(3) + "%";
        c.style.width = (hx * 200).toFixed(3) + "%";
        c.style.height = (hy * 200).toFixed(3) + "%";
        var im = c.querySelector("img");
        im.src = src;
        im.style.width = (100 / (2 * hx)).toFixed(3) + "%";
        im.style.height = (100 / (2 * hy)).toFixed(3) + "%";
        im.style.left = (-(fx - hx) / (2 * hx) * 100).toFixed(3) + "%";
        im.style.top = (-(fy - hy) / (2 * hy) * 100).toFixed(3) + "%";
      }
      for (var k = 0; k < d.ojos.length; k++) {
        var o = d.ojos[k], cx = num(o.cx, 0), cy = num(o.cy, 0), rx = num(o.rx, 0), ry = num(o.ry, 0);
        if (rx <= 0 || ry <= 0) { if (!Array.isArray(o.muestra)) ip++; else it++; continue; }
        if (Array.isArray(o.muestra)) {
          var tapa = tapas[it], copia = copias[it]; it++;
          ventana(tapa, cx, cy, rx * 1.5, ry * 1.35, cx + num(o.muestra[0], 0), cy + num(o.muestra[1], 0));
          ventana(copia, cx, cy, rx * 1.25, ry * 1.18, cx, cy);
          this._parpados.push({ tipo: "fieltro", tapa: tapa, ojo: copia });
        } else {
          var p = planos[ip]; ip++;
          var px = rx * 1.18, py = ry * 1.12;
          p.style.left = ((cx - px) * 100).toFixed(3) + "%";
          p.style.top = ((cy - py) * 100).toFixed(3) + "%";
          p.style.width = (px * 200).toFixed(3) + "%";
          p.style.height = (py * 200).toFixed(3) + "%";
          p.style.background = "linear-gradient(rgba(255,255,255,.10),rgba(0,0,0,.12))," + (o.parpado || "#888");
          p.style.boxShadow = "inset 0 -1.5px 0 rgba(0,0,0,.32)";
          this._parpados.push({ tipo: "plano", el: p });
        }
      }
      var ancho = (num(caja[2], 0.9) - num(caja[0], 0.1)) * 0.78;
      this._sombra.style.left = (((num(caja[0], 0.1) + num(caja[2], 0.9)) / 2 - ancho / 2) * 100).toFixed(2) + "%";
      this._sombra.style.width = (ancho * 100).toFixed(2) + "%";
      this._sombra.style.top = ((piso - 0.012) * 100).toFixed(2) + "%";
      this._sombra.style.height = "5%";
      this._pintar(0, 0, true);
    }

    _observar() {
      var yo = this;
      if (!this._io && "IntersectionObserver" in window) {
        this._io = new IntersectionObserver(function (e) {
          var u = e[e.length - 1];          // la entrada más reciente
          yo._visible = u ? u.isIntersecting : true;
          yo._arrancar();
        });
        this._io.observe(this);
      }
      if (!this._mq && window.matchMedia) {
        this._mq = window.matchMedia("(prefers-reduced-motion: reduce)");
        if (this._mq.addEventListener) this._mq.addEventListener("change", this._alCambiarMovimiento);
      }
      document.addEventListener("visibilitychange", this._alCambiarVisibilidad);
      if (!this._toque) {
        this._toque = true;
        this.addEventListener("pointerenter", function () { yo._golpe = performance.now(); });
        this.addEventListener("pointerdown", function () { yo._salto = performance.now(); });
      }
    }

    _alCambiarVisibilidad() {
      if (!document.hidden) this._arrancar();
    }

    _enVivo() {
      if (this.hasAttribute("tiempo") || this.hasAttribute("quieto")) return false;
      if (this._mq && this._mq.matches) return false;
      return true;
    }

    _arrancar() {
      this._parar();
      if (this.hasAttribute("tiempo")) {
        var t = num(this.getAttribute("tiempo"), 0);
        var p = this.hasAttribute("parpadeo") ? clamp(num(this.getAttribute("parpadeo"), 0), 0, 1) : parpadeoGrabado(t);
        this._pintar(t, p, true);
        return;
      }
      if (!this._enVivo()) { this._pintar(0, 0, true); return; }
      if (this._visible && !document.hidden) {
        activar(this);
        this._raf = requestAnimationFrame(this._cuadro);
      }
    }

    _parar() {
      if (this._raf) cancelAnimationFrame(this._raf);
      this._raf = 0;
      desactivar(this);
    }

    _alMover(e) {
      var r = this.getBoundingClientRect();
      var mx = Math.max(window.innerWidth / 2, 1), my = Math.max(window.innerHeight / 2, 1);
      this._mira.tx = clamp((e.clientX - (r.left + r.width / 2)) / mx, -1, 1);
      this._mira.ty = clamp((e.clientY - (r.top + r.height / 2)) / my, -1, 1);
    }

    _cuadro(ahora) {
      this._raf = 0;
      if (!this._enVivo() || !this._visible || document.hidden) { this._arrancar(); return; }
      var m = this._mira;
      m.x += (m.tx - m.x) * 0.06;
      m.y += (m.ty - m.y) * 0.06;
      // Parpadeo en vivo: cada 2.5–6 s, a veces doble
      var pb = this._parpadeo;
      if (!pb.proximo) pb.proximo = ahora + 1200 + Math.random() * 2500;
      if (ahora >= pb.proximo) {
        pb.inicio = ahora;
        pb.doble = Math.random() < 0.2;
        pb.proximo = ahora + 2500 + Math.random() * 3500;
      }
      var d = ahora - pb.inicio;
      var p = curvaParpadeo(d);
      if (!p && pb.doble) p = curvaParpadeo(d - 260);
      this._pintar(ahora, p, false);
      this._raf = requestAnimationFrame(this._cuadro);
    }

    _pintar(t, parpadeo, fijo) {
      if (!this._cuerpo) return;
      var q = pose(t);
      if (!fijo) {
        q.r += this._mira.x * 3.5;
        q.x += this._mira.x * 0.012;
        q.y += this._mira.y * 0.006;
        var ahora = performance.now();
        var g = (ahora - this._golpe) / 380;          // aplastón al pasar el mouse
        if (g >= 0 && g < 1) {
          var a = Math.sin(g * Math.PI) * (1 - g) * 0.08;
          q.sy -= a; q.sx += a * 0.7;
        }
        var s = (ahora - this._salto) / 460;          // saltito al tocar
        if (s >= 0 && s < 1) {
          var h = Math.sin(s * Math.PI);
          q.y -= this._alturaSalto * h;
          q.sy += 0.03 * h; q.sx -= 0.02 * h;
        }
      }
      this._cuerpo.style.transform =
        "translate(" + (q.x * 100).toFixed(3) + "%," + (q.y * 100).toFixed(3) + "%) rotate(" + q.r.toFixed(3) +
        "deg) scale(" + q.sx.toFixed(4) + "," + q.sy.toFixed(4) + ")";
      var pp = clamp(parpadeo, 0, 1);
      for (var i = 0; i < this._parpados.length; i++) {
        var pa = this._parpados[i];
        if (pa.tipo === "plano") {
          pa.el.style.transform = "scaleY(" + pp.toFixed(3) + ")";
        } else {
          var ver = pp > 0.001 ? "visible" : "hidden";
          pa.tapa.style.visibility = ver;
          pa.ojo.style.visibility = ver;
          pa.ojo.style.transform = "scaleY(" + (1 - 0.9 * pp).toFixed(3) + ")";
        }
      }
      if (this._sombra) {
        var k = clamp(1 + q.y * 4, 0.6, 1.2);
        this._sombra.style.transform = "scale(" + k.toFixed(3) + ")";
        this._sombra.style.opacity = clamp(0.9 + q.y * 6, 0.35, 1).toFixed(3);
      }
    }
  }

  customElements.define("kot-avatar", KotAvatar);
  window.KotAvatar = { pose: pose, parpadeoGrabado: parpadeoGrabado, CICLO: CICLO };
})();
