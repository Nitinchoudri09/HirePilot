"use client";

import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { api, User, AuthResponse } from "./api";

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (data: { email: string; password: string; full_name: string; role?: string }) => Promise<void>;
  googleLogin: (idToken: string) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

function persistAuth(data: AuthResponse) {
  localStorage.setItem("refera_token", data.access_token);
  localStorage.setItem("refera_user", JSON.stringify(data.user));
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("refera_token");
    const saved = localStorage.getItem("refera_user");
    if (token && saved) {
      setUser(JSON.parse(saved));
      api.getMe().then(setUser).catch(() => {
        localStorage.removeItem("refera_token");
        localStorage.removeItem("refera_user");
        setUser(null);
      }).finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email: string, password: string) => {
    const data = await api.login({ email, password });
    persistAuth(data);
    setUser(data.user);
  };

  const register = async (data: { email: string; password: string; full_name: string; role?: string }) => {
    const res = await api.register(data);
    persistAuth(res);
    setUser(res.user);
  };

  const googleLogin = async (idToken: string) => {
    const data = await api.googleAuth(idToken);
    persistAuth(data);
    setUser(data.user);
  };

  const logout = () => {
    localStorage.removeItem("refera_token");
    localStorage.removeItem("refera_user");
    setUser(null);
  };

  const refreshUser = async () => {
    const me = await api.getMe();
    setUser(me);
    localStorage.setItem("refera_user", JSON.stringify(me));
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, googleLogin, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
