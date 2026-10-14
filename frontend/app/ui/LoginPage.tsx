'use client';

import { FormEvent, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export default function LoginPage() {
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function handleLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setBusy(true);
    try {
      const body = new URLSearchParams();
      body.set("username", identifier);
      body.set("password", password);
      const response = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body,
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(data.detail ?? "Unable to sign in. Please check your details.");
      // MVP: token storage is intentionally not persisted in localStorage.
      // Replace with an HttpOnly-cookie session before production.
      window.location.href = `/welcome?token=${encodeURIComponent(data.access_token)}`;
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong. Please try again.");
    } finally {
      setBusy(false);
    }
  }

  function handleGoogleSSO() {
    window.location.href = `${API_BASE}/auth/google/login`;
  }

  return (
    <main className="auth-shell">
      <section className="visual-panel" aria-label="FuturePath AI introduction">
        <div className="visual-top">
          <a className="brand" href="/" aria-label="FuturePath AI home">
            <span className="brand-mark"><span /></span>
            <span>futurepath<span className="brand-ai">.ai</span></span>
          </a>
          <span className="secure-label"><span className="secure-dot" /> YOUR NEXT CHAPTER</span>
        </div>

        <div className="hero-copy">
          <div className="eyebrow"><span className="eyebrow-line" /> CAREER CLARITY, REIMAGINED</div>
          <h1>Your future<br />isn’t a <em>guess.</em></h1>
          <p className="hero-description">
            Turn your experience into direction. Discover the skills, opportunities,
            and next steps that move your career forward.
          </p>
          <div className="insight-card">
            <div className="insight-heading">
              <span className="insight-icon">✳</span>
              <span>YOUR CAREER, IN FOCUS</span>
              <span className="live-pill">PERSONALIZED</span>
            </div>
            <div className="insight-main">
              <div>
                <span className="small-label">NEXT BEST STEP</span>
                <strong>Build your skill map</strong>
                <span className="insight-sub">A clearer path starts with you.</span>
              </div>
              <div className="progress-ring"><span>01</span></div>
            </div>
            <div className="skill-bars" aria-hidden="true">
              <span className="bar bar-one" /><span className="bar bar-two" /><span className="bar bar-three" />
              <span className="bar bar-four" /><span className="bar bar-five" /><span className="bar bar-six" />
              <span className="bar bar-seven" /><span className="bar bar-eight" /><span className="bar bar-nine" />
              <span className="bar bar-ten" /><span className="bar bar-eleven" /><span className="bar bar-twelve" />
            </div>
          </div>
        </div>
        <div className="visual-footer">
          <span>MAKE YOUR NEXT MOVE COUNT.</span>
          <span>01 — YOUR JOURNEY STARTS HERE</span>
        </div>
      </section>

      <section className="form-panel">
        <div className="mobile-brand">
          <span className="brand-mark"><span /></span>
          <span>futurepath<span className="brand-ai">.ai</span></span>
        </div>
        <div className="form-wrap">
          <div className="form-kicker">WELCOME BACK</div>
          <h2>Sign in to your<br /><span>next chapter.</span></h2>
          <p className="form-intro">Pick up where your ambition left off.</p>

          <button className="sso-button" type="button" onClick={handleGoogleSSO}>
            <svg viewBox="0 0 48 48" aria-hidden="true" className="google-icon">
              <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z" transform="translate(0 4)"/>
              <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.76 7.18l7.73 6C44.42 38.01 46.98 31.88 46.98 24.55z"/>
              <path fill="#FBBC05" d="M10.53 28.59A14.4 14.4 0 0 1 9.75 24c0-1.59.27-3.13.76-4.59l-7.98-6.19A23.9 23.9 0 0 0 0 24c0 3.87.93 7.52 2.56 10.78l7.97-6.19z" transform="translate(0 4)"/>
              <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.91-5.8l-7.73-6c-2.14 1.44-4.89 2.3-8.18 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 43.62 14.62 48 24 48z" transform="translate(0 -2)"/>
            </svg>
            <span>Continue with Google</span>
            <span className="button-arrow">↗</span>
          </button>
          <div className="sso-caption"><span className="tiny-shield">◇</span> FAST, SECURE SINGLE SIGN-ON</div>

          <div className="separator"><span /> <span className="separator-text">OR USE YOUR ACCOUNT</span> <span /></div>

          <form onSubmit={handleLogin} className="login-form">
            <label htmlFor="identifier">Username or email</label>
            <div className="input-wrap">
              <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z" /></svg>
              <input id="identifier" name="username" autoComplete="username" placeholder="Enter your username or email" value={identifier} onChange={e => setIdentifier(e.target.value)} required />
            </div>

            <div className="password-label-row">
              <label htmlFor="password">Password</label>
              <a href="mailto:support@futurepath.ai?subject=Password%20reset">Forgot password?</a>
            </div>
            <div className="input-wrap">
              <svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4" /></svg>
              <input id="password" name="password" autoComplete="current-password" placeholder="Enter your password" type={showPassword ? "text" : "password"} value={password} onChange={e => setPassword(e.target.value)} required />
              <button className="show-password" type="button" onClick={() => setShowPassword(v => !v)} aria-label={showPassword ? "Hide password" : "Show password"}>{showPassword ? "Hide" : "Show"}</button>
            </div>

            {error && <p className="error-message" role="alert">{error}</p>}
            <button className="submit-button" type="submit" disabled={busy}>
              <span>{busy ? "Signing in…" : "Sign in with password"}</span>
              {!busy && <span className="submit-arrow">→</span>}
            </button>
          </form>

          <p className="signup-prompt">New to FuturePath? <a href="mailto:support@futurepath.ai?subject=Create%20an%20account">Create an account <span>↗</span></a></p>
        </div>
        <footer className="form-footer">
          <span>© 2026 FUTUREPATH AI</span>
          <div><a href="#privacy">PRIVACY</a><span className="footer-dot">·</span><a href="#terms">TERMS</a></div>
        </footer>
      </section>
    </main>
  );
}
