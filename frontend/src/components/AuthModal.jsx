import React, { useState } from "react";
import { X, Mail, Lock, User, Sparkles, ArrowRight, ShieldCheck, Check } from "lucide-react";
import SecondlyBrainLogo from "./SecondlyBrainLogo";

function AuthModal({ isOpen, onClose, onAuthSuccess, initialMode = "login" }) {
  const [mode, setMode] = useState(initialMode); // "login" | "register" | "forgot" | "reset"
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [resetToken, setResetToken] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [message, setMessage] = useState(null);

  if (!isOpen) return null;

  const API_URL = import.meta.env.VITE_API_URL || (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1" ? "http://localhost:8000" : "");

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setMessage(null);

    try {
      if (mode === "login") {
        const resp = await fetch(`${API_URL}/api/auth/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password })
        });
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.detail || "Login failed");
        localStorage.setItem("sb_token", data.token);
        onAuthSuccess(data.user);
        onClose();
      } else if (mode === "register") {
        if (password !== confirmPassword) {
          throw new Error("Passwords do not match.");
        }
        const resp = await fetch(`${API_URL}/api/auth/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name, email, password })
        });
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.detail || "Registration failed");
        localStorage.setItem("sb_token", data.token);
        onAuthSuccess(data.user);
        onClose();
      } else if (mode === "forgot") {
        const resp = await fetch(`${API_URL}/api/auth/forgot-password`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email })
        });
        const data = await resp.json();
        setMessage(data.message);
      } else if (mode === "reset") {
        const resp = await fetch(`${API_URL}/api/auth/reset-password`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ token: resetToken, new_password: newPassword })
        });
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.detail || "Reset failed");
        setMessage("Password updated successfully! Please log in.");
        setMode("login");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-modal-overlay" onClick={onClose}>
      <div className="auth-modal-card" onClick={(e) => e.stopPropagation()}>
        <button className="auth-close-btn" onClick={onClose}>
          <X size={16} />
        </button>

        <div className="auth-header-brand">
          <SecondlyBrainLogo variant="full" size="medium" />
          <p className="auth-subtitle">Your Intelligent Second Brain</p>
        </div>

        {error && <div className="auth-alert-error">{error}</div>}
        {message && <div className="auth-alert-success">{message}</div>}

        <form onSubmit={handleSubmit} className="auth-form-body">
          {mode === "register" && (
            <div className="input-field-group">
              <label>Full Name</label>
              <div className="input-with-icon">
                <User size={15} />
                <input
                  type="text"
                  placeholder="Rohith Kumar"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                />
              </div>
            </div>
          )}

          {(mode === "login" || mode === "register" || mode === "forgot") && (
            <div className="input-field-group">
              <label>Email Address</label>
              <div className="input-with-icon">
                <Mail size={15} />
                <input
                  type="email"
                  placeholder="user@secondlybrain.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
            </div>
          )}

          {(mode === "login" || mode === "register") && (
            <div className="input-field-group">
              <label>Password</label>
              <div className="input-with-icon">
                <Lock size={15} />
                <input
                  type="password"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
            </div>
          )}

          {mode === "register" && (
            <div className="input-field-group">
              <label>Confirm Password</label>
              <div className="input-with-icon">
                <Lock size={15} />
                <input
                  type="password"
                  placeholder="••••••••"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                />
              </div>
            </div>
          )}

          {mode === "reset" && (
            <>
              <div className="input-field-group">
                <label>Reset Token</label>
                <div className="input-with-icon">
                  <ShieldCheck size={15} />
                  <input
                    type="text"
                    placeholder="Enter reset token from email"
                    value={resetToken}
                    onChange={(e) => setResetToken(e.target.value)}
                    required
                  />
                </div>
              </div>
              <div className="input-field-group">
                <label>New Password</label>
                <div className="input-with-icon">
                  <Lock size={15} />
                  <input
                    type="password"
                    placeholder="New password (min 6 chars)"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    required
                  />
                </div>
              </div>
            </>
          )}

          {mode === "login" && (
            <div className="forgot-password-link">
              <button type="button" onClick={() => setMode("forgot")}>
                Forgot password?
              </button>
            </div>
          )}

          <button type="submit" className="auth-submit-btn" disabled={loading}>
            <span>
              {mode === "login"
                ? "Sign In"
                : mode === "register"
                ? "Create Account"
                : mode === "forgot"
                ? "Send Reset Link"
                : "Update Password"}
            </span>
            <ArrowRight size={15} />
          </button>
        </form>

        <div className="auth-footer-toggle">
          {mode === "login" ? (
            <p>
              Don't have an account?{" "}
              <button type="button" onClick={() => setMode("register")}>
                Create Account
              </button>
            </p>
          ) : (
            <p>
              Already have an account?{" "}
              <button type="button" onClick={() => setMode("login")}>
                Sign In
              </button>
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default AuthModal;
