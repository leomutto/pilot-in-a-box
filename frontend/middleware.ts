import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(req: NextRequest) {
  const accessToken = req.cookies.get("token")?.value;
  const refreshToken = req.cookies.get("refresh_token")?.value;

  // Rutas protegidas
  const protectedRoutes = ["/dashboard"];

  const isProtected = protectedRoutes.some((route) =>
    req.nextUrl.pathname.startsWith(route)
  );

  // -----------------------------------------------------
  // 1. Si la ruta es protegida y NO hay access token
  //    → intentar refresh automático
  // -----------------------------------------------------
  if (isProtected && !accessToken) {
    if (refreshToken) {
      // Dejar pasar: /api/me se encargará de renovar el token
      return NextResponse.next();
    }

    // Sin access token y sin refresh token → login
    return NextResponse.redirect(new URL("/login", req.url));
  }

  // -----------------------------------------------------
  // 2. Si hay access token → permitir acceso
  // -----------------------------------------------------
  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/dashboard"],
};