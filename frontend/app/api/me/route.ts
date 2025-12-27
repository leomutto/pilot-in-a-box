import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL || "http://pib-backend:8000";

export async function GET(req: NextRequest) {
  try {
    const accessToken =
      req.cookies.get("token")?.value || req.headers.get("authorization");

    const refreshToken = req.cookies.get("refresh_token")?.value;

    // -----------------------------------------------------
    // 1. Si no hay access token → no autorizado
    // -----------------------------------------------------
    if (!accessToken) {
      return NextResponse.json(
        { detail: "Token no enviado" },
        { status: 401 }
      );
    }

    // -----------------------------------------------------
    // 2. Intentar validar el access token llamando a /auth/me
    // -----------------------------------------------------
    let res = await fetch(`${BACKEND_URL}/auth/me`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${accessToken.replace("Bearer ", "")}`,
      },
    });

    // Si el access token es válido → devolver respuesta
    if (res.ok) {
      const data = await res.json();
      return NextResponse.json(data, { status: res.status });
    }

    // -----------------------------------------------------
    // 3. Si el access token expiró → intentar refresh
    // -----------------------------------------------------
    if (res.status === 401 && refreshToken) {
      const refreshRes = await fetch(`${BACKEND_URL}/auth/refresh`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh_token: refreshToken }),
      });

      const refreshData = await refreshRes.json();

      if (!refreshRes.ok) {
        return NextResponse.json(
          { detail: "Refresh token inválido o expirado" },
          { status: 401 }
        );
      }

      // -----------------------------------------------------
      // 4. Guardar el nuevo access token en cookies
      // -----------------------------------------------------
      const response = NextResponse.json(refreshData);

      response.cookies.set("token", refreshData.access_token, {
        httpOnly: false,
        secure: false,
        sameSite: "lax",
        path: "/",
      });

      // -----------------------------------------------------
      // 5. Reintentar /auth/me con el nuevo access token
      // -----------------------------------------------------
      res = await fetch(`${BACKEND_URL}/auth/me`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${refreshData.access_token}`,
        },
      });

      const finalData = await res.json();
      return NextResponse.json(finalData, { status: res.status });
    }

    // -----------------------------------------------------
    // 6. Si no hay refresh token o falló → no autorizado
    // -----------------------------------------------------
    return NextResponse.json(
      { detail: "Token inválido o expirado" },
      { status: 401 }
    );
  } catch (error) {
    return NextResponse.json(
      { detail: "Error interno en Next.js" },
      { status: 500 }
    );
  }
}