"use client";

import { GoogleLogin } from "@react-oauth/google";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";

export default function GoogleLoginButton() {
  const { googleLogin } = useAuth();
  const router = useRouter();
  const clientId = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID;

  if (!clientId) {
    return (
      <button
        type="button"
        disabled
        className="btn-secondary w-full opacity-50 cursor-not-allowed"
        title="Set NEXT_PUBLIC_GOOGLE_CLIENT_ID to enable"
      >
        Google Sign-In (configure OAuth)
      </button>
    );
  }

  return (
    <div className="flex justify-center">
      <GoogleLogin
        onSuccess={async (res) => {
          if (res.credential) {
            await googleLogin(res.credential);
            router.push("/dashboard");
          }
        }}
        onError={() => console.error("Google login failed")}
        theme="filled_black"
        size="large"
        text="continue_with"
        shape="rectangular"
      />
    </div>
  );
}
