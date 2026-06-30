/**
 * ─────────────────────────────────────────────────────────────────────────────
 * firebase-config.js  —  HirePilot Firebase Web SDK Configuration
 *
 * HOW TO GET YOUR WEB API KEY:
 * 1. Go to https://console.firebase.google.com/project/hirepilot-c0125/overview
 * 2. Click the gear icon ⚙️ → "Project settings"
 * 3. Scroll down to "Your apps" → click "</> Add app" (Web)
 * 4. Register app name "HirePilot Web"
 * 5. Copy the firebaseConfig object and paste the values below
 *
 * SECURITY: Do NOT commit real keys to Git. Use environment variables
 * injected via Django template context or a build step.
 * ─────────────────────────────────────────────────────────────────────────────
 */

// ── Firebase Web App Config ───────────────────────────────────────────────────
// Replace these placeholder values with the config from Firebase Console
// (Project Settings → Your apps → Web app → SDK setup and configuration)
const firebaseConfig = {
  apiKey:            "AIzaSyDGuhXrMq8iOib6GmjHk22h0AtbxRVfzaI",
  authDomain:        "hirepilot-c0125.firebaseapp.com",
  projectId:         "hirepilot-c0125",
  storageBucket:     "hirepilot-c0125.firebasestorage.app",
  messagingSenderId: "156770586473",
  appId:             "1:156770586473:web:8f2354fdf42c83201037f8",
  measurementId:     "G-F35XX2EJVN",
};

// ── Initialize Firebase ───────────────────────────────────────────────────────
import { initializeApp }                    from "https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js";
import { getAuth, sendPasswordResetEmail }  from "https://www.gstatic.com/firebasejs/10.12.0/firebase-auth.js";

const app  = initializeApp(firebaseConfig);
const auth = getAuth(app);

// ── sendPasswordResetEmail helper ─────────────────────────────────────────────
/**
 * Sends a Firebase password reset email to the given address.
 * Returns { success: true } or { success: false, error: { code, message } }
 *
 * Error codes handled:
 *   auth/invalid-email      — not a valid email format
 *   auth/user-not-found     — no account with this email (Firebase < v9 only)
 *   auth/too-many-requests  — rate-limited, try later
 *   auth/network-request-failed — no internet / timeout
 */
async function firebaseSendPasswordReset(email) {
  const actionCodeSettings = {
    // URL the user is redirected to AFTER resetting their password
    url: `${window.location.origin}/login/`,
    handleCodeInApp: false,
  };

  try {
    await sendPasswordResetEmail(auth, email.trim(), actionCodeSettings);
    return { success: true };
  } catch (err) {
    const friendlyMessages = {
      "auth/invalid-email":           "That doesn't look like a valid email address.",
      "auth/user-not-found":          "No account found with this email address.",
      "auth/too-many-requests":       "Too many requests. Please wait a moment and try again.",
      "auth/network-request-failed":  "Network error. Please check your connection and retry.",
      "auth/missing-email":           "Please enter your email address.",
    };
    return {
      success: false,
      error: {
        code:    err.code,
        message: friendlyMessages[err.code] || "An unexpected error occurred. Please try again.",
      },
    };
  }
}

export { auth, firebaseSendPasswordReset };
