export default function WelcomePage() {
  return (
    <main style={{ minHeight: "100vh", display: "grid", placeItems: "center", padding: 24, fontFamily: "Arial, sans-serif", color: "#17241f" }}>
      <section style={{ maxWidth: 480, textAlign: "center" }}>
        <div style={{ fontSize: 38, marginBottom: 12 }}>✳</div>
        <h1>You're signed in.</h1>
        <p>Your authentication flow completed. The next MVP step is the FuturePath career profile dashboard.</p>
        <a href="/" style={{ color: "#426d2d" }}>Return to sign in</a>
      </section>
    </main>
  );
}
