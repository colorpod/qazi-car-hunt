// Qazi Car Hunt: one Worker that serves the car-search page.
// Access: open /k/<ACCESS_KEY> once per device; it sets a long-lived cookie. Everything else 404s without it.
import APP from "./app.html";
import SEARCHES from "./searches/index.js";

const COOKIE = "qch";
const YEAR = 60 * 60 * 24 * 365;
const HEADERS = { "X-Robots-Tag": "noindex, nofollow", "Cache-Control": "no-store" };

function hasAccess(request, key) {
  const c = request.headers.get("Cookie") || "";
  return key && c.split(/;\s*/).some((p) => p === `${COOKIE}=${key}`);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const key = env.ACCESS_KEY;

    if (url.pathname.startsWith("/k/")) {
      if (!key || url.pathname.slice(3) !== key) return new Response("Not found", { status: 404, headers: HEADERS });
      return new Response(null, {
        status: 302,
        headers: { ...HEADERS, Location: "/", "Set-Cookie": `${COOKIE}=${key}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${YEAR}` },
      });
    }

    if (!hasAccess(request, key)) return new Response("Not found", { status: 404, headers: HEADERS });

    if (url.pathname === "/" || url.pathname === "/index.html") {
      const html = APP.replace("/*__SEARCHES__*/[]", JSON.stringify(SEARCHES).replace(/</g, "\\u003c"));
      return new Response(html, { headers: { ...HEADERS, "Content-Type": "text/html; charset=utf-8" } });
    }
    if (url.pathname === "/searches.json") {
      return new Response(JSON.stringify(SEARCHES), { headers: { ...HEADERS, "Content-Type": "application/json" } });
    }
    return new Response("Not found", { status: 404, headers: HEADERS });
  },
};
