// Qazi Car Hunt: one Worker that serves the car-search page. Public, no login.
import APP from "./app.html";
import SEARCHES from "./searches/index.js";

const HEADERS = { "Cache-Control": "no-store" };

export default {
  async fetch(request) {
    const url = new URL(request.url);

    if (url.pathname === "/" || url.pathname === "/index.html") {
      const html = APP.replace("/*__SEARCHES__*/[]", JSON.stringify(SEARCHES).replace(/</g, "\\u003c"));
      return new Response(html, { headers: { ...HEADERS, "Content-Type": "text/html; charset=utf-8" } });
    }
    if (url.pathname === "/searches.json") {
      return new Response(JSON.stringify(SEARCHES), { headers: { ...HEADERS, "Content-Type": "application/json" } });
    }
    // Old unlock links keep working: send them to the page.
    if (url.pathname.startsWith("/k/")) return Response.redirect(new URL("/", url), 302);
    return new Response("Not found", { status: 404, headers: HEADERS });
  },
};
