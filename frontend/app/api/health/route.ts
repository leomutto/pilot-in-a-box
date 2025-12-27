import { NextResponse } from "next/server";

const BACKEND_URL =
  process.env.BACKEND_URL || "http://pib-backend:8000";

export async function GET() {
  try {
    // Intentamos consultar el health del backend
    const res = await fetch(`${BACKEND_URL}/health`, {
      method: "GET",
    });

    if (!res.ok) {
      return NextResponse.json(
        {
          status: "degraded",
          frontend: "healthy",
          backend: "unhealthy",
        },
        { status: 500 }
      );
    }

    const backendHealth = await res.json();

    return NextResponse.json(
      {
        status: "ok",
        frontend: "healthy",
        backend: backendHealth,
      },
      { status: 200 }
    );
  } catch (error) {
    return NextResponse.json(
      {
        status: "down",
        frontend: "healthy",
        backend: "unreachable",
      },
      { status: 500 }
    );
  }
}