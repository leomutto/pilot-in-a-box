import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  try {
    const response = NextResponse.json({ ok: true });

    // Borrar access token
    response.cookies.set("token", "", {
      httpOnly: false,
      secure: false,
      sameSite: "lax",
      path: "/",
      maxAge: 0,
    });

    // Borrar refresh token
    response.cookies.set("refresh_token", "", {
      httpOnly: true,
      secure: false, // poner true en producción con HTTPS
      sameSite: "lax",
      path: "/",
      maxAge: 0,
    });

    return response;
  } catch (error) {
    return NextResponse.json(
      { detail: "Error interno en Next.js" },
      { status: 500 }
    );
  }
}