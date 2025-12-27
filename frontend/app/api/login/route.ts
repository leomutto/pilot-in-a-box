import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL || "http://pib-backend:8000";

export function GET() {
  return NextResponse.json(
    { detail: "Method Not Allowed" },
    { status: 405 }
  );
}

export async function POST(req: NextRequest) {
  try {
    const { email, password } = await req.json();

    const res = await fetch(`${BACKEND_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json();

    if (!res.ok) {
      return NextResponse.json({ detail: data.detail }, { status: res.status });
    }

    const response = NextResponse.json({ ok: true });

    // -----------------------------------------------------
    // ACCESS TOKEN → cookie normal (JS puede leerla)
    // -----------------------------------------------------
    response.cookies.set("token", data.access_token, {
      httpOnly: false,
      secure: false,
      sameSite: "lax",
      path: "/",
    });

    // -----------------------------------------------------
    // REFRESH TOKEN → cookie httpOnly (JS NO puede leerla)
    // -----------------------------------------------------
    response.cookies.set("refresh_token", data.refresh_token, {
      httpOnly: true,
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