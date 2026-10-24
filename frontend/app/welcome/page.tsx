'use client';

import { useEffect, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
type User = { id: string; username: string; email?: string | null; is_active: boolean; auth_provider: string };
type Profile = { headline?: string | null; professional_summary?: string | null; current_location?: string | null; preferred_locations?: string[] | null; preferred_work_modes?: string[] | null; target_roles?: string[] | null; years_experience?: number | null; is_open_to_opportunities: boolean };
type Resume = { id: string; original_filename: string; file_size_bytes?: number | null; created_at: string };
type Job = { id: string; resume_id: string; status: string; attempt_count: number; max_attempts: number; error_message?: string | null };

export default function WelcomePage() {
  const [user, setUser] = useState<User | null>(null);
  const [profile, setProfile] = useState<Profile>({ is_open_to_opportunities: false });
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [jobs, setJobs] = useState<Record<string, Job>>({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState("");

  async function loadData() {
    const [u, p, r] = await Promise.all([
      fetch(`${API_BASE}/auth/me`, { credentials: "include" }).then(async x => { if (!x.ok) throw new Error("unauthenticated"); return x.json(); }),
      fetch(`${API_BASE}/career-profile`, { credentials: "include" }).then(async x => { if (!x.ok) throw new Error("profile"); return x.json(); }),
      fetch(`${API_BASE}/resumes`, { credentials: "include" }).then(async x => { if (!x.ok) throw new Error("resumes"); return x.json(); }),
    ]);
    setUser(u); if (p) setProfile(p); setResumes(r);
    const entries = await Promise.all(r.map(async (resume: Resume) => {
      const response = await fetch(`${API_BASE}/resumes/${resume.id}/processing-job`, { credentials: "include" });
      return [resume.id, response.ok ? await response.json() : null] as const;
    }));
    setJobs(Object.fromEntries(entries.filter(([, job]) => job)));
  }

  useEffect(() => { loadData().catch(() => { window.location.href = "/"; }).finally(() => setLoading(false)); }, []);

  useEffect(() => {
    const active = Object.values(jobs).some(j => j.status === "queued" || j.status === "running");
    if (!active) return;
    const timer = setInterval(() => loadData().catch(() => undefined), 2500);
    return () => clearInterval(timer);
  }, [jobs]);

  async function saveProfile(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault(); setSaving(true); setSaved(false);
    const response = await fetch(`${API_BASE}/career-profile`, { method: "PUT", headers: { "Content-Type": "application/json" }, credentials: "include", body: JSON.stringify(profile) });
    setSaving(false); if (response.ok) { setProfile(await response.json()); setSaved(true); }
  }

  async function uploadResume(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0]; if (!file) return;
    setUploadError(""); setUploading(true);
    const form = new FormData(); form.append("file", file);
    const response = await fetch(`${API_BASE}/resumes`, { method: "POST", credentials: "include", body: form });
    if (!response.ok) { const body = await response.json().catch(() => ({})); setUploadError(body.detail ?? "Resume upload failed."); setUploading(false); return; }
    await loadData(); setUploading(false); event.target.value = "";
  }

  async function retry(jobId: string) {
    await fetch(`${API_BASE}/processing-jobs/${jobId}/retry`, { method: "POST", credentials: "include" });
    await loadData();
  }

  async function logout() { await fetch(`${API_BASE}/auth/logout`, { method: "POST", credentials: "include" }); window.location.href = "/"; }
  if (loading) return <main style={{ minHeight: "100vh", display: "grid", placeItems: "center" }}>Loading…</main>;
  if (!user) return null;

  return <main style={{ minHeight: "100vh", padding: "48px 24px", fontFamily: "Arial, sans-serif", color: "#17241f", background: "#f7f5ef" }}>
    <section style={{ maxWidth: 900, margin: "0 auto" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 36 }}>
        <div><div style={{ letterSpacing: 2, fontSize: 12 }}>FUTUREPATH AI</div><h1 style={{ margin: "8px 0" }}>Welcome, {user.username}.</h1><p style={{ margin: 0 }}>Signed in as {user.email ?? "your FuturePath account"} via {user.auth_provider}.</p></div>
        <button onClick={logout} style={{ padding: "10px 18px", cursor: "pointer" }}>Sign out</button>
      </div>

      <section style={cardStyle}>
        <p style={eyebrow}>RELEASE 1 · RESUME INGESTION</p>
        <h2 style={{ marginTop: 0 }}>Build your career profile from your resume</h2>
        <p>Upload a PDF resume. FuturePath stores it privately and processes it asynchronously into structured career data.</p>
        <label style={{ display: "inline-block", marginTop: 12, padding: "12px 22px", border: "1px solid #17241f", borderRadius: 8, cursor: uploading ? "wait" : "pointer" }}>
          {uploading ? "Uploading…" : "Choose PDF resume"}
          <input type="file" accept="application/pdf,.pdf" onChange={uploadResume} disabled={uploading} style={{ display: "none" }} />
        </label>
        <p style={{ fontSize: 13, marginBottom: 0 }}>Maximum size: 10 MB · PDF only</p>
        {uploadError && <p style={{ color: "#9b1c1c" }}>{uploadError}</p>}
        {resumes.length > 0 && <div style={{ marginTop: 24 }}><h3>Resume processing</h3>{resumes.map(resume => { const job = jobs[resume.id]; return <div key={resume.id} style={{ padding: 14, border: "1px solid #e0ded7", borderRadius: 10, marginTop: 10 }}><strong>{resume.original_filename}</strong><div style={{ fontSize: 13, marginTop: 5 }}>Status: <strong>{job?.status?.toUpperCase() ?? "QUEUED"}</strong> · attempts {job?.attempt_count ?? 0}/{job?.max_attempts ?? 3}</div>{job?.status === "failed" && <><p style={{ color: "#9b1c1c" }}>{job.error_message ?? "Processing failed."}</p><button onClick={() => retry(job.id)}>Retry processing</button></>}</div>; })}</div>}
      </section>

      <section style={cardStyle}>
        <p style={eyebrow}>CAREER PROFILE</p>
        <h2 style={{ marginTop: 0 }}>Review and correct your profile</h2>
        <p>This information is user-owned data. AI extraction is a starting point; you remain the source of truth.</p>
        <form onSubmit={saveProfile} style={{ display: "grid", gap: 16, marginTop: 24 }}>
          <label>Headline<input value={profile.headline ?? ""} onChange={e => setProfile({ ...profile, headline: e.target.value })} placeholder="e.g. Backend Engineer | Python & Cloud" style={inputStyle} /></label>
          <label>Professional summary<textarea value={profile.professional_summary ?? ""} onChange={e => setProfile({ ...profile, professional_summary: e.target.value })} rows={5} placeholder="Summarize your experience, strengths and direction." style={inputStyle} /></label>
          <label>Current location<input value={profile.current_location ?? ""} onChange={e => setProfile({ ...profile, current_location: e.target.value })} placeholder="e.g. Pune, India" style={inputStyle} /></label>
          <label>Target roles<input value={(profile.target_roles ?? []).join(", ")} onChange={e => setProfile({ ...profile, target_roles: e.target.value.split(",").map(v => v.trim()).filter(Boolean) })} placeholder="e.g. Backend Engineer, Platform Engineer" style={inputStyle} /></label>
          <label>Preferred work modes<input value={(profile.preferred_work_modes ?? []).join(", ")} onChange={e => setProfile({ ...profile, preferred_work_modes: e.target.value.split(",").map(v => v.trim()).filter(Boolean) })} placeholder="e.g. Remote, Hybrid" style={inputStyle} /></label>
          <label>Years of experience<input type="number" min="0" max="99.9" step="0.1" value={profile.years_experience ?? ""} onChange={e => setProfile({ ...profile, years_experience: e.target.value ? Number(e.target.value) : null })} style={inputStyle} /></label>
          <label style={{ display: "flex", gap: 10, alignItems: "center" }}><input type="checkbox" checked={profile.is_open_to_opportunities} onChange={e => setProfile({ ...profile, is_open_to_opportunities: e.target.checked })} /> Open to new opportunities</label>
          <div><button type="submit" disabled={saving} style={{ padding: "12px 22px", cursor: "pointer" }}>{saving ? "Saving…" : "Save career profile"}</button>{saved && <span style={{ marginLeft: 14 }}>Saved ✓</span>}</div>
        </form>
      </section>
    </section>
  </main>;
}

const cardStyle: React.CSSProperties = { background: "white", borderRadius: 16, padding: 32, boxShadow: "0 4px 24px rgba(0,0,0,.06)", marginBottom: 24 };
const eyebrow: React.CSSProperties = { letterSpacing: 1.5, fontSize: 12, marginBottom: 8 };
const inputStyle: React.CSSProperties = { display: "block", width: "100%", boxSizing: "border-box", marginTop: 7, padding: "12px 14px", border: "1px solid #d7d5ce", borderRadius: 8, font: "inherit" };
