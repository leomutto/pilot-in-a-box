import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL || "http://pib-backend:8000";

export async function POST(req: NextRequest) {
  try {
    const refreshToken = req.cookies.get("refresh_token")?.value;

    if (!refreshToken) {
      return NextResponse.json(
        { detail: "Refresh token no enviado" },
        { status: 401 }
      );
    }

    // Llamar al backend para renovar el access token
    const res = await fetch(`${BACKEND_URL}/auth/refresh`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });

    const data = await res.json();

    if (!res.ok) {
      return NextResponse.json(
        { detail: "Refresh token inválido o expirado" },
        { status: 401 }
      );
    }

    // Crear respuesta
    const response = NextResponse.json({ ok: true });

    // Guardar nuevo access token
    response.cookies.set("token", data.access_token, {
      httpOnly: false,
      secure: false, // poner true en producción con HTTPS
      sameSite: "lax",
      path: "/",
    });

    return response;
  } catch (error) {
    return NextResponse.json(
      { detail: "Error interno en Next.js" },
      { status: 500 }
    );
  }
}