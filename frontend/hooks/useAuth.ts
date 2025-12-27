"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

type User = {
  id: number;
  email: string;
  // agregá más campos si tu UserOut tiene otros
};

export function useAuth() {
  const router = useRouter();

  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function fetchMe() {
    try {
      setLoading(true);
      setError(null);

      const res = await fetch("/api/me", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!res.ok) {
        // Si está no autorizado, mandamos a login
        if (res.status === 401) {
          setUser(null);
          router.push("/login");
          return;
        }

        const data = await res.json();
        setError(data.detail || "Error al obtener el usuario");
        setUser(null);
        return;
      }

      const data = await res.json();
      setUser(data);
    } catch (err) {
      setError("Error de red o servidor");
      setUser(null);
    } finally {
      setLoading(false);
    }
  }

  async function logout() {
    try {
      await fetch("/api/logout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });
    } catch (err) {
      // aunque falle, igual redirigimos
    } finally {
      setUser(null);
      router.push("/login");
    }
  }

  useEffect(() => {
    fetchMe();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return {
    user,
    loading,
    error,
    logout,
    refetch: fetchMe,
  };
}