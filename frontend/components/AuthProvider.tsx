"use client";

import { ReactNode } from "react";

// TODO: Integrate Better Auth when backend is ready
// For now, just pass through children

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  // Placeholder for Better Auth integration
  // Will wrap with SessionProvider once backend auth is configured
  return <>{children}</>;
}
