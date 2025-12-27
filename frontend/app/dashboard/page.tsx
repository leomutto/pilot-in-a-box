"use client";

import { useAuth } from "../../hooks/useAuth";

export default function DashboardPage() {
  const { user, loading, error, logout } = useAuth();

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p>Cargando...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="flex flex-col gap-4">
          <p className="text-red-600">{error}</p>
          <button
            onClick={logout}
            className="bg-black text-white px-4 py-2 rounded"
          >
            Volver al login
          </button>
        </div>
      </div>
    );
  }

  if (!user) {
    // En teoría, el middleware + useAuth ya te mandan a login
    return null;
  }

  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <p className="text-lg">Sesión iniciada como: {user.email}</p>

      <button
        onClick={logout}
        className="bg-black text-white px-4 py-2 rounded hover:bg-gray-800"
      >
        Cerrar sesión
      </button>
    </div>
  );
}