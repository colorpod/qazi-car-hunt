// Qazi Car Hunt: one Worker that serves the car-search page. Public, no login.
import APP from "./app.html";
import SEARCHES from "./searches/index.js";
import CMC_CARFAX from "./carfax/SBM11FAA6GW006265.pdf";
import MILLER_STICKER from "./sticker/SBM14FCAXLW004596.pdf";

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
    // CARFAX PDFs dealers emailed us, for cars with no free report link.
    if (url.pathname === "/carfax/SBM11FAA6GW006265.pdf") {
      return new Response(CMC_CARFAX, { headers: { ...HEADERS, "Content-Type": "application/pdf" } });
    }
    if (url.pathname === "/sticker/SBM14FCAXLW004596.pdf") {
      return new Response(MILLER_STICKER, { headers: { ...HEADERS, "Content-Type": "application/pdf" } });
    }
    // Old unlock links keep working: send them to the page.
    if (url.pathname.startsWith("/k/")) return Response.redirect(new URL("/", url), 302);
    return new Response("Not found", { status: 404, headers: HEADERS });
  },
};
