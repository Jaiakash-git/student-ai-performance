import { useEffect, useRef, useState } from "react";

import "./App.css";

interface Message {
  sender: "user" | "ai";
  text: string;
}

interface AgentContext {
  student_name?: string;
  last_intent?: string | null;
  last_subject?: string | null;
  requested_subject?: string | null;
  last_result?: Record<string, unknown> | null;
}

interface DashboardData {
  student_name: string;
  average: number;
  attendance: number;
  performance_status: string;
  risk_level: string;
  risk_probability: number;
  highest_subject: string;
  highest_mark: number;
  lowest_subject: string;
  lowest_mark: number;
  overall_trend: string;
  average_improvement: number;
  recommendation: string;
  priority_subject: string;
  priority_mark: number;
}

interface AuthResponse {
  message: string;
  access_token: string;
  token_type: string;
  student_id: number;
  username: string;
  student_name: string;
}

type AuthMode = "login" | "register" | "forgot" | "verify-email";
type ForgotStep = "request" | "verify" | "reset";

const API_URL = "http://127.0.0.1:8000";

function App() {
  // ========================================
  // AUTHENTICATION
  // ========================================

  const [authMode, setAuthMode] = useState<AuthMode>("login");
  const [forgotStep, setForgotStep] =
    useState<ForgotStep>("request");

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [studentId, setStudentId] = useState("");
  const [email, setEmail] = useState("");
  const [confirmRegisterPassword, setConfirmRegisterPassword] =
    useState("");

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmRegisterPassword, setShowConfirmRegisterPassword] =
    useState(false);

  const [showForgotPasswordLink, setShowForgotPasswordLink] =
    useState(false);

  const [authLoading, setAuthLoading] = useState(false);
  const [authError, setAuthError] = useState("");
  const [authSuccess, setAuthSuccess] = useState("");

  // ========================================
  // FORGOT PASSWORD
  // ========================================

  const [forgotUsername, setForgotUsername] = useState("");
  const [forgotEmail, setForgotEmail] = useState("");
  const [forgotCode, setForgotCode] = useState("");
  const [resetPassword, setResetPassword] = useState("");
  const [confirmResetPassword, setConfirmResetPassword] =
    useState("");

  const [showResetPassword, setShowResetPassword] = useState(false);
  const [showConfirmResetPassword, setShowConfirmResetPassword] =
    useState(false);

  // ========================================
  // EMAIL VERIFICATION
  // ========================================

  const [verificationUsername, setVerificationUsername] =
    useState("");
  const [verificationEmail, setVerificationEmail] = useState("");
  const [verificationCode, setVerificationCode] = useState("");

  // ========================================
  // AUTH TOKEN
  // ========================================

  const [token, setToken] = useState<string | null>(
    localStorage.getItem("student_ai_token")
  );

  // ========================================
  // STUDENT
  // ========================================

  const [studentName, setStudentName] = useState(
    localStorage.getItem("student_ai_name") || ""
  );

  const [savedStudentId, setSavedStudentId] = useState(
    localStorage.getItem("student_ai_id") || ""
  );

  const [savedUsername, setSavedUsername] = useState(
    localStorage.getItem("student_ai_username") || ""
  );

  // ========================================
  // DASHBOARD
  // ========================================

  const [dashboard, setDashboard] =
    useState<DashboardData | null>(null);

  const [dashboardLoading, setDashboardLoading] = useState(false);
  const [dashboardError, setDashboardError] = useState("");

  // ========================================
  // NAVIGATION
  // ========================================

  const [activeSection, setActiveSection] = useState("dashboard");

  const navigateToSection = (
    section: string,
    elementId: string
  ) => {
    setActiveSection(section);

    setTimeout(() => {
      document
        .getElementById(elementId)
        ?.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
    }, 50);
  };

  // ========================================
  // PROFILE
  // ========================================

  const [isProfileOpen, setIsProfileOpen] = useState(false);

  const [isChangePasswordOpen, setIsChangePasswordOpen] =
    useState(false);

  const [isChangeEmailOpen, setIsChangeEmailOpen] =
    useState(false);

  // ========================================
  // CHANGE PASSWORD
  // ========================================

  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [passwordVerificationCode, setPasswordVerificationCode] =
    useState("");

  const [passwordCodeSent, setPasswordCodeSent] = useState(false);

  const [showCurrentPassword, setShowCurrentPassword] =
    useState(false);

  const [showNewPassword, setShowNewPassword] = useState(false);

  const [showConfirmPassword, setShowConfirmPassword] =
    useState(false);

  const [passwordChangeLoading, setPasswordChangeLoading] =
    useState(false);

  const [passwordCodeSending, setPasswordCodeSending] =
    useState(false);

  const [passwordChangeError, setPasswordChangeError] =
    useState("");

  const [passwordChangeSuccess, setPasswordChangeSuccess] =
    useState("");

  // ========================================
  // CHANGE EMAIL
  // ========================================

  const [newEmail, setNewEmail] = useState("");

  const [emailVerificationCode, setEmailVerificationCode] =
    useState("");

  const [emailCodeSent, setEmailCodeSent] = useState(false);

  const [emailChangeLoading, setEmailChangeLoading] =
    useState(false);

  const [emailCodeSending, setEmailCodeSending] =
    useState(false);

  const [emailChangeError, setEmailChangeError] =
    useState("");

  const [emailChangeSuccess, setEmailChangeSuccess] =
    useState("");

  // ========================================
  // CHAT
  // ========================================

  const [isChatOpen, setIsChatOpen] = useState(false);
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const [context, setContext] =
    useState<AgentContext | null>(null);

  const chatEndRef = useRef<HTMLDivElement | null>(null);

  // ========================================
  // AUTH INPUT REFS
  // ========================================

  const usernameRef =
    useRef<HTMLInputElement | null>(null);

  const passwordRef =
    useRef<HTMLInputElement | null>(null);

  const studentIdRef =
    useRef<HTMLInputElement | null>(null);

  // ========================================
  // AUTO SCROLL CHAT
  // ========================================

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading, isChatOpen]);

  // ========================================
  // RESTORE SESSION AFTER PAGE REFRESH
  // ========================================

  useEffect(() => {
    const storedToken =
      localStorage.getItem("student_ai_token");

    const storedStudentName =
      localStorage.getItem("student_ai_name");

    if (storedToken && storedStudentName) {
      setToken(storedToken);
      setStudentName(storedStudentName);

      loadDashboard(
        storedStudentName,
        storedToken
      );
    }
  }, []);

  // ========================================
  // RESET AUTH FLOW
  // ========================================

  const resetAuthFlow = () => {
    setForgotStep("request");

    setForgotUsername("");
    setForgotEmail("");
    setForgotCode("");

    setResetPassword("");
    setConfirmResetPassword("");

    setVerificationUsername("");
    setVerificationEmail("");
    setVerificationCode("");

    setEmail("");
    setConfirmRegisterPassword("");

    setShowPassword(false);
    setShowConfirmRegisterPassword(false);

    setShowResetPassword(false);
    setShowConfirmResetPassword(false);

    setShowForgotPasswordLink(false);

    setAuthError("");
    setAuthSuccess("");
    setAuthLoading(false);
  };

  // ========================================
  // SWITCH AUTH MODE
  // ========================================

  const switchAuthMode = (mode: AuthMode) => {
    setAuthMode(mode);

    if (mode !== "forgot") {
      setForgotStep("request");
    }

    if (mode !== "login") {
      setShowForgotPasswordLink(false);
    }

    setAuthError("");
    setAuthSuccess("");

    setShowPassword(false);
    setShowConfirmRegisterPassword(false);
    setShowResetPassword(false);
    setShowConfirmResetPassword(false);
  };

  // ========================================
  // LOGOUT
  // ========================================

  const logout = () => {
    localStorage.removeItem("student_ai_token");
    localStorage.removeItem("student_ai_name");
    localStorage.removeItem("student_ai_id");
    localStorage.removeItem("student_ai_username");

    setToken(null);
    setStudentName("");
    setSavedStudentId("");
    setSavedUsername("");

    setDashboard(null);
    setDashboardError("");

    setMessages([]);
    setContext(null);
    setIsChatOpen(false);

    setUsername("");
    setPassword("");
    setStudentId("");
    setEmail("");
    setConfirmRegisterPassword("");

    resetAuthFlow();

    setAuthMode("login");

    setIsProfileOpen(false);
    setIsChangePasswordOpen(false);
    setIsChangeEmailOpen(false);

    resetPasswordForm();
    resetEmailChangeForm();

    setActiveSection("dashboard");
  };

  // ========================================
  // LOGIN
  // ========================================

  const handleLogin = async () => {
    if (!username.trim() || !password.trim()) {
      setAuthError(
        "Please enter your username and password."
      );
      return;
    }

    setAuthLoading(true);
    setAuthError("");
    setAuthSuccess("");

    try {
      const response = await fetch(
        `${API_URL}/auth/login`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: username.trim(),
            password,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setShowForgotPasswordLink(true);

        throw new Error(
          data.detail ||
            "Invalid username or password."
        );
      }

      const authData: AuthResponse = data;

      setShowForgotPasswordLink(false);

      localStorage.setItem(
        "student_ai_token",
        authData.access_token
      );

      localStorage.setItem(
        "student_ai_name",
        authData.student_name
      );

      localStorage.setItem(
        "student_ai_id",
        String(authData.student_id)
      );

      localStorage.setItem(
        "student_ai_username",
        authData.username
      );

      setToken(authData.access_token);
      setStudentName(authData.student_name);

      setSavedStudentId(
        String(authData.student_id)
      );

      setSavedUsername(authData.username);

      setPassword("");
      setShowPassword(false);

      setActiveSection("dashboard");

      setMessages([
        {
          sender: "ai",
          text: `Hello ${authData.student_name}! 👋 How can I help you today?`,
        },
      ]);

      await loadDashboard(
        authData.student_name,
        authData.access_token
      );
    } catch (error) {
      console.error(error);

      setAuthError(
        error instanceof Error
          ? error.message
          : "Unable to connect to the AI server."
      );
    } finally {
      setAuthLoading(false);
    }
  };

  // ========================================
  // REGISTER
  // ========================================

  const handleRegister = async () => {
    if (
      !studentId.trim() ||
      !username.trim() ||
      !email.trim() ||
      !password.trim() ||
      !confirmRegisterPassword.trim()
    ) {
      setAuthError("Please fill in all fields.");
      return;
    }

    const numericStudentId = Number(studentId);

    if (
      !Number.isInteger(numericStudentId) ||
      numericStudentId <= 0
    ) {
      setAuthError(
        "Student ID must be a valid number."
      );
      return;
    }

    const normalizedEmail =
      email.trim().toLowerCase();

    if (
      !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(
        normalizedEmail
      )
    ) {
      setAuthError(
        "Please enter a valid email address."
      );
      return;
    }

    if (password.length < 6) {
      setAuthError(
        "Password must be at least 6 characters."
      );
      return;
    }

    if (
      password !== confirmRegisterPassword
    ) {
      setAuthError(
        "Password and confirmation do not match."
      );
      return;
    }

    setAuthLoading(true);
    setAuthError("");
    setAuthSuccess("");

    try {
      const response = await fetch(
        `${API_URL}/auth/register`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            student_id: numericStudentId,
            username: username.trim(),
            email: normalizedEmail,
            password,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Registration failed."
        );
      }

      setAuthSuccess(
        "Registration successful! You can now login."
      );

      setAuthMode("login");

      setStudentId("");
      setEmail("");
      setPassword("");
      setConfirmRegisterPassword("");

      setShowPassword(false);
      setShowConfirmRegisterPassword(false);

      setShowForgotPasswordLink(false);
    } catch (error) {
      console.error(error);

      setAuthError(
        error instanceof Error
          ? error.message
          : "Unable to register."
      );
    } finally {
      setAuthLoading(false);
    }
  };

  // ========================================
  // SEND EMAIL VERIFICATION
  // ========================================

  const handleSendEmailVerification =
    async () => {
      if (
        !verificationUsername.trim() ||
        !verificationEmail.trim()
      ) {
        setAuthError(
          "Please enter your username and email."
        );
        return;
      }

      setAuthLoading(true);
      setAuthError("");
      setAuthSuccess("");

      try {
        const response = await fetch(
          `${API_URL}/auth/send-email-verification`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              username:
                verificationUsername.trim(),

              email:
                verificationEmail.trim(),
            }),
          }
        );

        const data = await response.json();

        if (!response.ok) {
          throw new Error(
            data.detail ||
              "Unable to send verification code."
          );
        }

        setAuthSuccess(
          "If the account details are valid, a verification code has been sent to your email."
        );

        setVerificationCode("");
      } catch (error) {
        console.error(error);

        setAuthError(
          error instanceof Error
            ? error.message
            : "Unable to send verification code."
        );
      } finally {
        setAuthLoading(false);
      }
    };

  // ========================================
  // VERIFY EMAIL
  // ========================================

  const handleVerifyEmail = async () => {
    if (
      !verificationUsername.trim() ||
      !verificationCode.trim()
    ) {
      setAuthError(
        "Please enter your username and verification code."
      );
      return;
    }

    if (
      !/^\d{6}$/.test(
        verificationCode.trim()
      )
    ) {
      setAuthError(
        "Verification code must be 6 digits."
      );
      return;
    }

    setAuthLoading(true);
    setAuthError("");
    setAuthSuccess("");

    try {
      const response = await fetch(
        `${API_URL}/auth/verify-email`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username:
              verificationUsername.trim(),

            verification_code:
              verificationCode.trim(),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Invalid or expired verification code."
        );
      }

      setAuthMode("login");

      setUsername(
        verificationUsername.trim()
      );

      setVerificationUsername("");
      setVerificationEmail("");
      setVerificationCode("");

      setAuthSuccess(
        "Email verified successfully! You can now login and use password recovery."
      );
    } catch (error) {
      console.error(error);

      setAuthError(
        error instanceof Error
          ? error.message
          : "Unable to verify email."
      );
    } finally {
      setAuthLoading(false);
    }
  };

  // ========================================
  // FORGOT PASSWORD - REQUEST CODE
  // ========================================

  const handleForgotPassword = async () => {
    if (
      !forgotUsername.trim() ||
      !forgotEmail.trim()
    ) {
      setAuthError(
        "Please enter your username and registered email."
      );
      return;
    }

    setAuthLoading(true);
    setAuthError("");
    setAuthSuccess("");

    try {
      const response = await fetch(
        `${API_URL}/auth/forgot-password`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username:
              forgotUsername.trim(),

            email:
              forgotEmail.trim(),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Unable to process password recovery."
        );
      }

      setForgotStep("verify");

      setAuthSuccess(
        "If the account details are valid, a verification code has been sent to your email."
      );
    } catch (error) {
      console.error(error);

      setAuthError(
        error instanceof Error
          ? error.message
          : "Unable to process password recovery."
      );
    } finally {
      setAuthLoading(false);
    }
  };

  // ========================================
  // VERIFY RESET CODE
  // ========================================

  const handleVerifyResetCode = async () => {
    if (
      !forgotUsername.trim() ||
      !forgotCode.trim()
    ) {
      setAuthError(
        "Please enter your username and verification code."
      );
      return;
    }

    if (
      !/^\d{6}$/.test(
        forgotCode.trim()
      )
    ) {
      setAuthError(
        "Verification code must be 6 digits."
      );
      return;
    }

    setAuthLoading(true);
    setAuthError("");
    setAuthSuccess("");

    try {
      const response = await fetch(
        `${API_URL}/auth/verify-reset-code`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username:
              forgotUsername.trim(),

            verification_code:
              forgotCode.trim(),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Invalid or expired verification code."
        );
      }

      setForgotStep("reset");

      setAuthSuccess(
        "Code verified. You can now create a new password."
      );
    } catch (error) {
      console.error(error);

      setAuthError(
        error instanceof Error
          ? error.message
          : "Unable to verify reset code."
      );
    } finally {
      setAuthLoading(false);
    }
  };

  // ========================================
  // RESET PASSWORD
  // ========================================

  const handleResetPassword = async () => {
    setAuthError("");
    setAuthSuccess("");

    if (
      !forgotUsername.trim() ||
      !forgotCode.trim() ||
      !resetPassword ||
      !confirmResetPassword
    ) {
      setAuthError(
        "Please fill in all fields."
      );
      return;
    }

    if (resetPassword.length < 6) {
      setAuthError(
        "New password must be at least 6 characters."
      );
      return;
    }

    if (
      resetPassword !==
      confirmResetPassword
    ) {
      setAuthError(
        "New password and confirmation do not match."
      );
      return;
    }

    setAuthLoading(true);

    try {
      const response = await fetch(
        `${API_URL}/auth/reset-password`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username:
              forgotUsername.trim(),

            verification_code:
              forgotCode.trim(),

            new_password:
              resetPassword,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Unable to reset password."
        );
      }

      setAuthMode("login");
      setForgotStep("request");

      setUsername(
        forgotUsername.trim()
      );

      setPassword("");

      setForgotUsername("");
      setForgotEmail("");
      setForgotCode("");

      setResetPassword("");
      setConfirmResetPassword("");

      setShowResetPassword(false);
      setShowConfirmResetPassword(false);

      setShowForgotPasswordLink(false);

      setAuthSuccess(
        "Password reset successfully! You can now login with your new password."
      );
    } catch (error) {
      console.error(error);

      setAuthError(
        error instanceof Error
          ? error.message
          : "Unable to reset password."
      );
    } finally {
      setAuthLoading(false);
    }
  };

  // ========================================
  // LOAD DASHBOARD
  // ========================================

  const loadDashboard = async (
    name: string,
    authToken: string
  ) => {
    setDashboardLoading(true);
    setDashboardError("");

    try {
      const response = await fetch(
        `${API_URL}/student/${encodeURIComponent(
          name
        )}/dashboard`,
        {
          headers: {
            Authorization:
              `Bearer ${authToken}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Unable to load student data."
        );
      }

      setDashboard(data);
    } catch (error) {
      console.error(error);

      const errorMessage =
        error instanceof Error
          ? error.message.toLowerCase()
          : "";

      if (
        errorMessage.includes("token") ||
        errorMessage.includes("authenticated") ||
        errorMessage.includes("not authorized") ||
        errorMessage.includes("unauthorized")
      ) {
        logout();
        return;
      }

      setDashboardError(
        error instanceof Error
          ? error.message
          : "Unable to connect to the AI server."
      );
    } finally {
      setDashboardLoading(false);
    }
  };

  // ========================================
  // CHANGE PASSWORD
  // ========================================

  const resetPasswordForm = () => {
    setCurrentPassword("");
    setNewPassword("");
    setConfirmPassword("");

    setPasswordVerificationCode("");
    setPasswordCodeSent(false);

    setShowCurrentPassword(false);
    setShowNewPassword(false);
    setShowConfirmPassword(false);

    setPasswordChangeError("");
    setPasswordChangeSuccess("");

    setPasswordChangeLoading(false);
    setPasswordCodeSending(false);
  };

  const openChangePassword = () => {
    resetPasswordForm();

    setIsProfileOpen(false);
    setIsChangeEmailOpen(false);

    setIsChangePasswordOpen(true);
  };

  const closeChangePassword = () => {
    resetPasswordForm();
    setIsChangePasswordOpen(false);
  };

  // ========================================
  // SEND PASSWORD CHANGE CODE
  // ========================================

  const handleSendPasswordChangeCode =
    async () => {
      setPasswordChangeError("");
      setPasswordChangeSuccess("");

      if (!currentPassword) {
        setPasswordChangeError(
          "Please enter your current password."
        );
        return;
      }

      if (!token) {
        setPasswordChangeError(
          "Your session has expired. Please login again."
        );
        return;
      }

      setPasswordCodeSending(true);

      try {
        const response = await fetch(
          `${API_URL}/auth/change-password/request`,
          {
            method: "POST",
            headers: {
              "Content-Type":
                "application/json",

              Authorization:
                `Bearer ${token}`,
            },
            body: JSON.stringify({
              current_password:
                currentPassword,
            }),
          }
        );

        const data = await response.json();

        if (!response.ok) {
          throw new Error(
            data.detail ||
              "Unable to send verification code."
          );
        }

        setPasswordCodeSent(true);
        setPasswordVerificationCode("");

        setPasswordChangeSuccess(
          "A verification code has been sent to your registered email."
        );
      } catch (error) {
        console.error(error);

        const errorMessage =
          error instanceof Error
            ? error.message
            : "Unable to send verification code.";

        if (
          errorMessage
            .toLowerCase()
            .includes("authenticated") ||
          errorMessage
            .toLowerCase()
            .includes("token") ||
          errorMessage
            .toLowerCase()
            .includes("unauthorized")
        ) {
          logout();
          return;
        }

        setPasswordChangeError(
          errorMessage
        );
      } finally {
        setPasswordCodeSending(false);
      }
    };

  // ========================================
  // VERIFY + CHANGE PASSWORD
  // ========================================

  const handleChangePassword = async () => {
    setPasswordChangeError("");
    setPasswordChangeSuccess("");

    if (
      !currentPassword ||
      !newPassword ||
      !confirmPassword
    ) {
      setPasswordChangeError(
        "Please fill in all password fields."
      );
      return;
    }

    if (!passwordCodeSent) {
      setPasswordChangeError(
        "Please send and verify the email code before changing your password."
      );
      return;
    }

    if (!passwordVerificationCode.trim()) {
      setPasswordChangeError(
        "Please enter the verification code sent to your email."
      );
      return;
    }

    if (
      !/^\d{6}$/.test(
        passwordVerificationCode.trim()
      )
    ) {
      setPasswordChangeError(
        "Verification code must be 6 digits."
      );
      return;
    }

    if (newPassword.length < 6) {
      setPasswordChangeError(
        "New password must be at least 6 characters."
      );
      return;
    }

    if (
      newPassword !==
      confirmPassword
    ) {
      setPasswordChangeError(
        "New password and confirmation do not match."
      );
      return;
    }

    if (
      currentPassword ===
      newPassword
    ) {
      setPasswordChangeError(
        "New password must be different from your current password."
      );
      return;
    }

    if (!token) {
      setPasswordChangeError(
        "Your session has expired. Please login again."
      );
      return;
    }

    setPasswordChangeLoading(true);

    try {
      const response = await fetch(
        `${API_URL}/auth/change-password`,
        {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json",

            Authorization:
              `Bearer ${token}`,
          },

          body: JSON.stringify({
            current_password:
              currentPassword,

            new_password:
              newPassword,

            verification_code:
              passwordVerificationCode.trim(),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Unable to change password."
        );
      }

      setPasswordChangeSuccess(
        data.message ||
          "Password changed successfully."
      );

      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
      setPasswordVerificationCode("");

      setPasswordCodeSent(false);

      setShowCurrentPassword(false);
      setShowNewPassword(false);
      setShowConfirmPassword(false);
    } catch (error) {
      console.error(error);

      const errorMessage =
        error instanceof Error
          ? error.message
          : "Unable to change password.";

      if (
        errorMessage
          .toLowerCase()
          .includes("authenticated") ||
        errorMessage
          .toLowerCase()
          .includes("token") ||
        errorMessage
          .toLowerCase()
          .includes("unauthorized")
      ) {
        logout();
        return;
      }

      setPasswordChangeError(
        errorMessage
      );
    } finally {
      setPasswordChangeLoading(false);
    }
  };

  // ========================================
  // CHANGE EMAIL
  // ========================================

  const resetEmailChangeForm = () => {
    setNewEmail("");
    setEmailVerificationCode("");

    setEmailCodeSent(false);

    setEmailChangeLoading(false);
    setEmailCodeSending(false);

    setEmailChangeError("");
    setEmailChangeSuccess("");
  };

  const openChangeEmail = () => {
    resetEmailChangeForm();

    setIsProfileOpen(false);
    setIsChangePasswordOpen(false);

    setIsChangeEmailOpen(true);
  };

  const closeChangeEmail = () => {
    resetEmailChangeForm();
    setIsChangeEmailOpen(false);
  };

  // ========================================
  // SEND EMAIL CHANGE CODE
  // ========================================

  const handleRequestEmailChange =
    async () => {
      setEmailChangeError("");
      setEmailChangeSuccess("");

      if (!newEmail.trim()) {
        setEmailChangeError(
          "Please enter your new email address."
        );
        return;
      }

      const normalizedEmail =
        newEmail.trim().toLowerCase();

      if (
        !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(
          normalizedEmail
        )
      ) {
        setEmailChangeError(
          "Please enter a valid email address."
        );
        return;
      }

      if (!token) {
        setEmailChangeError(
          "Your session has expired. Please login again."
        );
        return;
      }

      setEmailCodeSending(true);

      try {
        const response = await fetch(
          `${API_URL}/auth/change-email/request`,
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json",

              Authorization:
                `Bearer ${token}`,
            },

            body: JSON.stringify({
              new_email:
                normalizedEmail,
            }),
          }
        );

        const data = await response.json();

        if (!response.ok) {
          throw new Error(
            data.detail ||
              "Unable to send email verification code."
          );
        }

        setNewEmail(normalizedEmail);
        setEmailVerificationCode("");
        setEmailCodeSent(true);

        setEmailChangeSuccess(
          "A verification code has been sent to your new email address."
        );
      } catch (error) {
        console.error(error);

        const errorMessage =
          error instanceof Error
            ? error.message
            : "Unable to send email verification code.";

        if (
          errorMessage
            .toLowerCase()
            .includes("authenticated") ||
          errorMessage
            .toLowerCase()
            .includes("token") ||
          errorMessage
            .toLowerCase()
            .includes("unauthorized")
        ) {
          logout();
          return;
        }

        setEmailChangeError(
          errorMessage
        );
      } finally {
        setEmailCodeSending(false);
      }
    };

  // ========================================
  // VERIFY EMAIL CHANGE
  // ========================================

  const handleVerifyEmailChange =
    async () => {
      setEmailChangeError("");
      setEmailChangeSuccess("");

      if (!emailCodeSent) {
        setEmailChangeError(
          "Please request a verification code first."
        );
        return;
      }

      if (!emailVerificationCode.trim()) {
        setEmailChangeError(
          "Please enter the verification code."
        );
        return;
      }

      if (
        !/^\d{6}$/.test(
          emailVerificationCode.trim()
        )
      ) {
        setEmailChangeError(
          "Verification code must be 6 digits."
        );
        return;
      }

      if (!token) {
        setEmailChangeError(
          "Your session has expired. Please login again."
        );
        return;
      }

      setEmailChangeLoading(true);

      try {
        const response = await fetch(
          `${API_URL}/auth/change-email/verify`,
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json",

              Authorization:
                `Bearer ${token}`,
            },

            body: JSON.stringify({
              verification_code:
                emailVerificationCode.trim(),
            }),
          }
        );

        const data = await response.json();

        if (!response.ok) {
          throw new Error(
            data.detail ||
              "Unable to verify email change."
          );
        }

        setEmailChangeSuccess(
          data.message ||
            "Email address changed successfully."
        );

        setNewEmail("");
        setEmailVerificationCode("");
        setEmailCodeSent(false);
      } catch (error) {
        console.error(error);

        const errorMessage =
          error instanceof Error
            ? error.message
            : "Unable to verify email change.";

        if (
          errorMessage
            .toLowerCase()
            .includes("authenticated") ||
          errorMessage
            .toLowerCase()
            .includes("token") ||
          errorMessage
            .toLowerCase()
            .includes("unauthorized")
        ) {
          logout();
          return;
        }

        setEmailChangeError(
          errorMessage
        );
      } finally {
        setEmailChangeLoading(false);
      }
    };

  // ========================================
  // SEND CHAT MESSAGE
  // ========================================

  const sendMessage = async () => {
    if (
      !message.trim() ||
      loading ||
      !token
    ) {
      return;
    }

    const userMessage =
      message.trim();

    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: userMessage,
      },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const response = await fetch(
        `${API_URL}/chat`,
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",

            Authorization:
              `Bearer ${token}`,
          },

          body: JSON.stringify({
            student_name:
              studentName,

            message:
              userMessage,

            context:
              context,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Unable to process your message."
        );
      }

      setContext(data.context);

      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text: data.response,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text:
            "Sorry, I couldn't connect to the AI server.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // ========================================
  // CHAT ENTER KEY
  // ========================================

  const handleChatKeyDown = (
    event: React.KeyboardEvent<HTMLInputElement>
  ) => {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();
      sendMessage();
    }
  };

  // ========================================
  // AUTH ENTER KEY
  // ========================================

  const handleUsernameKeyDown = (
    event: React.KeyboardEvent<HTMLInputElement>
  ) => {
    if (event.key === "Enter") {
      event.preventDefault();
      passwordRef.current?.focus();
    }
  };

  const handlePasswordKeyDown = (
    event: React.KeyboardEvent<HTMLInputElement>
  ) => {
    if (event.key === "Enter") {
      event.preventDefault();

      if (authMode === "login") {
        handleLogin();
      } else if (
        authMode === "register"
      ) {
        handleRegister();
      }
    }
  };

  const handleStudentIdKeyDown = (
    event: React.KeyboardEvent<HTMLInputElement>
  ) => {
    if (event.key === "Enter") {
      event.preventDefault();
      usernameRef.current?.focus();
    }
  };

  // ========================================
  // AUTH SCREEN
  // ========================================

  if (!token || !studentName) {
    return (
      <div className="auth-container">
        <div className="auth-background-shape shape-one" />
        <div className="auth-background-shape shape-two" />

        <div className="auth-card">
          <div className="auth-brand">
            <div className="auth-logo">
              🤖
            </div>

            <div>
              <h1>Student AI</h1>
              <span>
                Academic Assistant
              </span>
            </div>
          </div>

          {(authMode === "login" ||
            authMode === "register") && (
            <>
              <div className="auth-heading">
                <h2>
                  {authMode === "login"
                    ? "Welcome back"
                    : "Create your account"}
                </h2>

                <p>
                  {authMode === "login"
                    ? "Sign in to access your academic dashboard."
                    : "Create your account to get started with Student AI."}
                </p>
              </div>

              <div className="auth-tabs">
                <button
                  type="button"
                  className={
                    authMode === "login"
                      ? "auth-tab active"
                      : "auth-tab"
                  }
                  onClick={() =>
                    switchAuthMode("login")
                  }
                >
                  Login
                </button>

                <button
                  type="button"
                  className={
                    authMode === "register"
                      ? "auth-tab active"
                      : "auth-tab"
                  }
                  onClick={() =>
                    switchAuthMode("register")
                  }
                >
                  Register
                </button>
              </div>
            </>
          )}

          {authMode === "forgot" && (
            <div className="auth-heading">
              <h2>
                {forgotStep === "request"
                  ? "Forgot your password?"
                  : forgotStep === "verify"
                  ? "Verify your code"
                  : "Create a new password"}
              </h2>

              <p>
                {forgotStep === "request"
                  ? "Enter your username and registered email to recover your account."
                  : forgotStep === "verify"
                  ? "Enter the 6-digit verification code sent to your email."
                  : "Choose a new password for your Student AI account."}
              </p>
            </div>
          )}

          {authMode === "verify-email" && (
            <div className="auth-heading">
              <h2>
                Verify your email
              </h2>

              <p>
                Verify your email address to enable secure password recovery.
              </p>
            </div>
          )}

          {authError && (
            <div className="auth-message error">
              <span>⚠️</span>
              <span>{authError}</span>
            </div>
          )}

          {authSuccess && (
            <div className="auth-message success">
              <span>✓</span>
              <span>{authSuccess}</span>
            </div>
          )}

          {/* LOGIN */}

          {authMode === "login" && (
            <>
              <div className="form-group">
                <label htmlFor="username">
                  Username
                </label>

                <div className="input-wrapper">
                  <span>👤</span>

                  <input
                    id="username"
                    ref={usernameRef}
                    type="text"
                    placeholder="Enter your username"
                    value={username}
                    onChange={(event) =>
                      setUsername(
                        event.target.value
                      )
                    }
                    onKeyDown={
                      handleUsernameKeyDown
                    }
                    autoComplete="username"
                    disabled={authLoading}
                  />
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="password">
                  Password
                </label>

                <div className="input-wrapper password-wrapper">
                  <span>🔒</span>

                  <input
                    id="password"
                    ref={passwordRef}
                    type={
                      showPassword
                        ? "text"
                        : "password"
                    }
                    placeholder="Enter your password"
                    value={password}
                    onChange={(event) =>
                      setPassword(
                        event.target.value
                      )
                    }
                    onKeyDown={
                      handlePasswordKeyDown
                    }
                    autoComplete="current-password"
                    disabled={authLoading}
                  />

                  <button
                    type="button"
                    className="password-toggle"
                    onClick={() =>
                      setShowPassword(
                        (prev) => !prev
                      )
                    }
                    aria-label={
                      showPassword
                        ? "Hide password"
                        : "Show password"
                    }
                    disabled={authLoading}
                  >
                    {showPassword
                      ? "🙈"
                      : "👁️"}
                  </button>
                </div>
              </div>

              {showForgotPasswordLink && (
                <div className="auth-forgot-row">
                  <button
                    type="button"
                    className="auth-link-button"
                    onClick={() => {
                      setAuthMode("forgot");
                      setForgotStep(
                        "request"
                      );

                      setForgotUsername(
                        username.trim()
                      );

                      setAuthError("");
                      setAuthSuccess("");
                    }}
                    disabled={authLoading}
                  >
                    Forgot Password?
                  </button>
                </div>
              )}

              <button
                type="button"
                className="auth-submit"
                onClick={handleLogin}
                disabled={authLoading}
              >
                {authLoading ? (
                  <>
                    <span className="button-spinner" />
                    Signing in...
                  </>
                ) : (
                  <>Sign In →</>
                )}
              </button>

              <div className="auth-secondary-action">
                <span>
                  Need to verify your email?
                </span>

                <button
                  type="button"
                  onClick={() => {
                    setAuthMode(
                      "verify-email"
                    );

                    setShowForgotPasswordLink(
                      false
                    );

                    setAuthError("");
                    setAuthSuccess("");
                  }}
                >
                  Verify Email
                </button>
              </div>

              <div className="auth-footer">
                Don't have an account?

                <button
                  type="button"
                  onClick={() => {
                    setAuthMode(
                      "register"
                    );

                    setShowForgotPasswordLink(
                      false
                    );

                    setAuthError("");
                    setAuthSuccess("");
                  }}
                >
                  Create one
                </button>
              </div>
            </>
          )}

          {/* REGISTER */}

          {authMode === "register" && (
            <>
              <div className="form-group">
                <label htmlFor="student-id">
                  Student ID
                </label>

                <div className="input-wrapper">
                  <span>🎓</span>

                  <input
                    id="student-id"
                    ref={studentIdRef}
                    type="number"
                    placeholder="Enter your student ID"
                    value={studentId}
                    onChange={(event) =>
                      setStudentId(
                        event.target.value
                      )
                    }
                    onKeyDown={
                      handleStudentIdKeyDown
                    }
                    disabled={authLoading}
                  />
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="register-username">
                  Username
                </label>

                <div className="input-wrapper">
                  <span>👤</span>

                  <input
                    id="register-username"
                    ref={usernameRef}
                    type="text"
                    placeholder="Choose a username"
                    value={username}
                    onChange={(event) =>
                      setUsername(
                        event.target.value
                      )
                    }
                    onKeyDown={
                      handleUsernameKeyDown
                    }
                    autoComplete="username"
                    disabled={authLoading}
                  />
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="register-email">
                  Email Address
                </label>

                <div className="input-wrapper">
                  <span>✉️</span>

                  <input
                    id="register-email"
                    type="email"
                    placeholder="Enter your email address"
                    value={email}
                    onChange={(event) =>
                      setEmail(
                        event.target.value
                      )
                    }
                    autoComplete="email"
                    disabled={authLoading}
                  />
                </div>

                <small className="field-hint">
                  Use an email you can access for verification and password recovery.
                </small>
              </div>

              <div className="form-group">
                <label htmlFor="register-password">
                  Password
                </label>

                <div className="input-wrapper password-wrapper">
                  <span>🔒</span>

                  <input
                    id="register-password"
                    ref={passwordRef}
                    type={
                      showPassword
                        ? "text"
                        : "password"
                    }
                    placeholder="Create a password"
                    value={password}
                    onChange={(event) =>
                      setPassword(
                        event.target.value
                      )
                    }
                    onKeyDown={
                      handlePasswordKeyDown
                    }
                    autoComplete="new-password"
                    disabled={authLoading}
                  />

                  <button
                    type="button"
                    className="password-toggle"
                    onClick={() =>
                      setShowPassword(
                        (prev) => !prev
                      )
                    }
                    disabled={authLoading}
                    aria-label={
                      showPassword
                        ? "Hide password"
                        : "Show password"
                    }
                  >
                    {showPassword
                      ? "🙈"
                      : "👁️"}
                  </button>
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="confirm-register-password">
                  Confirm Password
                </label>

                <div className="input-wrapper password-wrapper">
                  <span>🔐</span>

                  <input
                    id="confirm-register-password"
                    type={
                      showConfirmRegisterPassword
                        ? "text"
                        : "password"
                    }
                    placeholder="Confirm your password"
                    value={
                      confirmRegisterPassword
                    }
                    onChange={(event) =>
                      setConfirmRegisterPassword(
                        event.target.value
                      )
                    }
                    onKeyDown={
                      handlePasswordKeyDown
                    }
                    autoComplete="new-password"
                    disabled={authLoading}
                  />

                  <button
                    type="button"
                    className="password-toggle"
                    onClick={() =>
                      setShowConfirmRegisterPassword(
                        (prev) => !prev
                      )
                    }
                    disabled={authLoading}
                    aria-label={
                      showConfirmRegisterPassword
                        ? "Hide password"
                        : "Show password"
                    }
                  >
                    {showConfirmRegisterPassword
                      ? "🙈"
                      : "👁️"}
                  </button>
                </div>

                <small className="field-hint">
                  Password must be at least 6 characters.
                </small>
              </div>

              <button
                type="button"
                className="auth-submit"
                onClick={handleRegister}
                disabled={authLoading}
              >
                {authLoading ? (
                  <>
                    <span className="button-spinner" />
                    Creating account...
                  </>
                ) : (
                  <>Create Account →</>
                )}
              </button>

              <div className="auth-footer">
                Already have an account?

                <button
                  type="button"
                  onClick={() => {
                    setAuthMode("login");

                    setShowForgotPasswordLink(
                      false
                    );

                    setAuthError("");
                    setAuthSuccess("");
                  }}
                >
                  Sign in
                </button>
              </div>
            </>
          )}

          {/* FORGOT PASSWORD - REQUEST */}

          {authMode === "forgot" &&
            forgotStep === "request" && (
              <>
                <div className="form-group">
                  <label htmlFor="forgot-username">
                    Username
                  </label>

                  <div className="input-wrapper">
                    <span>👤</span>

                    <input
                      id="forgot-username"
                      type="text"
                      placeholder="Enter your username"
                      value={
                        forgotUsername
                      }
                      onChange={(event) =>
                        setForgotUsername(
                          event.target.value
                        )
                      }
                      autoComplete="username"
                      disabled={authLoading}
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label htmlFor="forgot-email">
                    Registered Email
                  </label>

                  <div className="input-wrapper">
                    <span>✉️</span>

                    <input
                      id="forgot-email"
                      type="email"
                      placeholder="Enter your registered email"
                      value={
                        forgotEmail
                      }
                      onChange={(event) =>
                        setForgotEmail(
                          event.target.value
                        )
                      }
                      autoComplete="email"
                      disabled={authLoading}
                    />
                  </div>
                </div>

                <button
                  type="button"
                  className="auth-submit"
                  onClick={
                    handleForgotPassword
                  }
                  disabled={authLoading}
                >
                  {authLoading ? (
                    <>
                      <span className="button-spinner" />
                      Sending code...
                    </>
                  ) : (
                    <>
                      Send Verification Code →
                    </>
                  )}
                </button>

                <button
                  type="button"
                  className="auth-back-button"
                  onClick={() => {
                    setAuthMode("login");

                    setShowForgotPasswordLink(
                      false
                    );

                    setAuthError("");
                    setAuthSuccess("");
                  }}
                  disabled={authLoading}
                >
                  ← Back to Login
                </button>
              </>
            )}

          {/* FORGOT PASSWORD - VERIFY */}

          {authMode === "forgot" &&
            forgotStep === "verify" && (
              <>
                <div className="verification-email-info">
                  <div className="verification-icon">
                    ✉️
                  </div>

                  <div>
                    <strong>
                      Check your email
                    </strong>

                    <span>
                      Enter the 6-digit code sent to your registered email address.
                    </span>
                  </div>
                </div>

                <div className="form-group">
                  <label htmlFor="forgot-code">
                    Verification Code
                  </label>

                  <div className="input-wrapper code-input-wrapper">
                    <span>🔢</span>

                    <input
                      id="forgot-code"
                      type="text"
                      inputMode="numeric"
                      maxLength={6}
                      placeholder="Enter 6-digit code"
                      value={forgotCode}
                      onChange={(event) =>
                        setForgotCode(
                          event.target.value.replace(
                            /\D/g,
                            ""
                          )
                        )
                      }
                      disabled={authLoading}
                    />
                  </div>
                </div>

                <button
                  type="button"
                  className="auth-submit"
                  onClick={
                    handleVerifyResetCode
                  }
                  disabled={authLoading}
                >
                  {authLoading ? (
                    <>
                      <span className="button-spinner" />
                      Verifying...
                    </>
                  ) : (
                    <>Verify Code →</>
                  )}
                </button>

                <div className="verification-actions">
                  <button
                    type="button"
                    className="auth-back-button"
                    onClick={() => {
                      setForgotStep(
                        "request"
                      );

                      setForgotCode("");

                      setAuthError("");
                      setAuthSuccess("");
                    }}
                    disabled={authLoading}
                  >
                    ← Change Details
                  </button>

                  <button
                    type="button"
                    className="auth-link-button"
                    onClick={
                      handleForgotPassword
                    }
                    disabled={authLoading}
                  >
                    Resend Code
                  </button>
                </div>
              </>
            )}

          {/* FORGOT PASSWORD - RESET */}

          {authMode === "forgot" &&
            forgotStep === "reset" && (
              <>
                <div className="verified-code-badge">
                  <span>✓</span>
                  Code verified
                </div>

                <div className="form-group">
                  <label htmlFor="reset-password">
                    New Password
                  </label>

                  <div className="input-wrapper password-wrapper">
                    <span>🔑</span>

                    <input
                      id="reset-password"
                      type={
                        showResetPassword
                          ? "text"
                          : "password"
                      }
                      placeholder="Enter new password"
                      value={
                        resetPassword
                      }
                      onChange={(event) =>
                        setResetPassword(
                          event.target.value
                        )
                      }
                      autoComplete="new-password"
                      disabled={authLoading}
                    />

                    <button
                      type="button"
                      className="password-toggle"
                      onClick={() =>
                        setShowResetPassword(
                          (prev) => !prev
                        )
                      }
                      disabled={authLoading}
                    >
                      {showResetPassword
                        ? "🙈"
                        : "👁️"}
                    </button>
                  </div>
                </div>

                <div className="form-group">
                  <label htmlFor="confirm-reset-password">
                    Confirm New Password
                  </label>

                  <div className="input-wrapper password-wrapper">
                    <span>🔐</span>

                    <input
                      id="confirm-reset-password"
                      type={
                        showConfirmResetPassword
                          ? "text"
                          : "password"
                      }
                      placeholder="Confirm new password"
                      value={
                        confirmResetPassword
                      }
                      onChange={(event) =>
                        setConfirmResetPassword(
                          event.target.value
                        )
                      }
                      autoComplete="new-password"
                      disabled={authLoading}
                    />

                    <button
                      type="button"
                      className="password-toggle"
                      onClick={() =>
                        setShowConfirmResetPassword(
                          (prev) => !prev
                        )
                      }
                      disabled={authLoading}
                    >
                      {showConfirmResetPassword
                        ? "🙈"
                        : "👁️"}
                    </button>
                  </div>
                </div>

                <small className="field-hint">
                  Password must be at least 6 characters.
                </small>

                <button
                  type="button"
                  className="auth-submit"
                  onClick={
                    handleResetPassword
                  }
                  disabled={authLoading}
                >
                  {authLoading ? (
                    <>
                      <span className="button-spinner" />
                      Resetting password...
                    </>
                  ) : (
                    <>Reset Password →</>
                  )}
                </button>
              </>
            )}

          {/* EMAIL VERIFICATION */}

          {authMode === "verify-email" && (
            <>
              <div className="form-group">
                <label htmlFor="verification-username">
                  Username
                </label>

                <div className="input-wrapper">
                  <span>👤</span>

                  <input
                    id="verification-username"
                    type="text"
                    placeholder="Enter your username"
                    value={
                      verificationUsername
                    }
                    onChange={(event) =>
                      setVerificationUsername(
                        event.target.value
                      )
                    }
                    autoComplete="username"
                    disabled={authLoading}
                  />
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="verification-email">
                  Email Address
                </label>

                <div className="input-wrapper">
                  <span>✉️</span>

                  <input
                    id="verification-email"
                    type="email"
                    placeholder="Enter your email address"
                    value={
                      verificationEmail
                    }
                    onChange={(event) =>
                      setVerificationEmail(
                        event.target.value
                      )
                    }
                    autoComplete="email"
                    disabled={authLoading}
                  />
                </div>
              </div>

              <button
                type="button"
                className="auth-submit"
                onClick={
                  handleSendEmailVerification
                }
                disabled={authLoading}
              >
                {authLoading ? (
                  <>
                    <span className="button-spinner" />
                    Sending code...
                  </>
                ) : (
                  <>
                    Send Verification Code →
                  </>
                )}
              </button>

              <div className="form-divider">
                <span>
                  Already received a code?
                </span>
              </div>

              <div className="form-group">
                <label htmlFor="verification-code">
                  Verification Code
                </label>

                <div className="input-wrapper code-input-wrapper">
                  <span>🔢</span>

                  <input
                    id="verification-code"
                    type="text"
                    inputMode="numeric"
                    maxLength={6}
                    placeholder="Enter 6-digit code"
                    value={
                      verificationCode
                    }
                    onChange={(event) =>
                      setVerificationCode(
                        event.target.value.replace(
                          /\D/g,
                          ""
                        )
                      )
                    }
                    disabled={authLoading}
                  />
                </div>
              </div>

              <button
                type="button"
                className="auth-submit"
                onClick={
                  handleVerifyEmail
                }
                disabled={authLoading}
              >
                {authLoading ? (
                  <>
                    <span className="button-spinner" />
                    Verifying...
                  </>
                ) : (
                  <>Verify Email ✓</>
                )}
              </button>

              <button
                type="button"
                className="auth-back-button"
                onClick={() => {
                  setAuthMode("login");

                  setShowForgotPasswordLink(
                    false
                  );

                  setAuthError("");
                  setAuthSuccess("");
                }}
                disabled={authLoading}
              >
                ← Back to Login
              </button>
            </>
          )}
        </div>
      </div>
    );
  }

  // ========================================
  // DASHBOARD LOADING
  // ========================================

  if (
    dashboardLoading &&
    !dashboard
  ) {
    return (
      <div className="loading-screen">
        <div className="loading-card">
          <div className="loading-icon">
            🤖
          </div>

          <h2>
            Preparing your dashboard...
          </h2>

          <p>
            Loading your academic information
          </p>

          <div className="loading-spinner" />
        </div>
      </div>
    );
  }

  // ========================================
  // DASHBOARD ERROR
  // ========================================

  if (
    dashboardError &&
    !dashboard
  ) {
    return (
      <div className="error-screen">
        <div className="error-card">
          <div className="error-icon">
            ⚠️
          </div>

          <h2>
            Unable to load dashboard
          </h2>

          <p>
            {dashboardError}
          </p>

          <button
            onClick={() => {
              if (token) {
                loadDashboard(
                  studentName,
                  token
                );
              }
            }}
          >
            Try Again
          </button>

          <button
            className="secondary-error-button"
            onClick={logout}
          >
            Sign Out
          </button>
        </div>
      </div>
    );
  }

  // ========================================
  // MAIN DASHBOARD
  // ========================================

  return (
    <div className="app-container">

      {/* SIDEBAR */}

      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">
            🤖
          </div>

          <div>
            <h2>Student AI</h2>

            <span>
              Academic Assistant
            </span>
          </div>
        </div>

        <nav className="sidebar-nav">
          <button
            type="button"
            className={
              activeSection === "dashboard"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() =>
              navigateToSection(
                "dashboard",
                "dashboard-section"
              )
            }
          >
            <span>📊</span>
            Dashboard
          </button>

          <button
            type="button"
            className={
              activeSection === "performance"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() =>
              navigateToSection(
                "performance",
                "performance-section"
              )
            }
          >
            <span>📈</span>
            Performance
          </button>

          <button
            type="button"
            className={
              activeSection === "analytics"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() =>
              navigateToSection(
                "analytics",
                "analytics-section"
              )
            }
          >
            <span>🎯</span>
            Analytics
          </button>

          <button
            type="button"
            className={
              activeSection === "insights"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() =>
              navigateToSection(
                "insights",
                "insights-section"
              )
            }
          >
            <span>💡</span>
            Insights
          </button>
        </nav>

        <div className="sidebar-bottom">
          <button
            type="button"
            className="student-mini student-mini-button"
            onClick={() =>
              setIsProfileOpen(true)
            }
          >
            <div className="student-avatar">
              {studentName
                .charAt(0)
                .toUpperCase()}
            </div>

            <div>
              <strong>
                {studentName}
              </strong>

              <span>
                Student
              </span>
            </div>
          </button>

          <button
            className="change-student"
            onClick={logout}
          >
            ↩ Sign Out
          </button>
        </div>
      </aside>

      {/* MAIN */}

      <main className="dashboard">
        <section
          id="dashboard-section"
          className="dashboard-section dashboard-main-section"
        >
          <header className="dashboard-header">
            <div>
              <p className="header-label">
                STUDENT DASHBOARD
              </p>

              <h1>
                Welcome back, {studentName} 👋
              </h1>

              <p className="header-subtitle">
                Here's your current academic overview.
              </p>
            </div>

            <button
              type="button"
              className="header-profile"
              onClick={() =>
                setIsProfileOpen(true)
              }
            >
              <div className="profile-avatar">
                {studentName
                  .charAt(0)
                  .toUpperCase()}
              </div>

              <div>
                <strong>
                  {studentName}
                </strong>

                <span>
                  Academic Profile
                </span>
              </div>
            </button>
          </header>

          {dashboard && (
            <section className="summary-panel">
              <div>
                <span className="summary-label">
                  YOUR ACADEMIC SUMMARY
                </span>

                <h2>
                  {dashboard.overall_trend ===
                  "Improving"
                    ? "You're making good progress! 🚀"
                    : "Keep working on your academic goals! 💪"}
                </h2>

                <p>
                  Your average is{" "}
                  <strong>
                    {dashboard.average.toFixed(2)}
                  </strong>{" "}
                  with{" "}
                  <strong>
                    {dashboard.attendance.toFixed(2)}%
                  </strong>{" "}
                  attendance. Your current academic risk
                  level is{" "}
                  <strong>
                    {dashboard.risk_level}
                  </strong>
                  .
                </p>
              </div>

              <button
                className="summary-chat-button"
                onClick={() =>
                  setIsChatOpen(true)
                }
              >
                Chat with AI →
              </button>
            </section>
          )}
        </section>

        {dashboard && (
          <>
            {/* PERFORMANCE */}

            <section
              id="performance-section"
              className="dashboard-section"
            >
              <div className="section-title">
                <span>
                  PERFORMANCE
                </span>

                <h2>
                  Academic Performance
                </h2>

                <p>
                  Understand how you are performing across subjects.
                </p>
              </div>

              <div className="panel performance-panel">
                <div className="panel-header">
                  <div>
                    <h2>
                      Academic Overview
                    </h2>

                    <p>
                      Your current subject performance
                    </p>
                  </div>

                  <span className="panel-badge">
                    {dashboard.overall_trend}
                  </span>
                </div>

                <div className="subject-comparison">
                  <div className="subject-card highest">
                    <div className="subject-icon">
                      🏆
                    </div>

                    <div>
                      <span>
                        Highest Scoring
                      </span>

                      <h3>
                        {dashboard.highest_subject}
                      </h3>

                      <strong>
                        {dashboard.highest_mark.toFixed(2)}
                      </strong>
                    </div>
                  </div>

                  <div className="subject-card lowest">
                    <div className="subject-icon">
                      📚
                    </div>

                    <div>
                      <span>
                        Priority Subject
                      </span>

                      <h3>
                        {dashboard.lowest_subject}
                      </h3>

                      <strong>
                        {dashboard.lowest_mark.toFixed(2)}
                      </strong>
                    </div>
                  </div>
                </div>

                <div className="trend-section">
                  <div className="trend-header">
                    <div>
                      <span>
                        Overall Performance Trend
                      </span>

                      <h3>
                        {dashboard.overall_trend}
                      </h3>
                    </div>

                    <div className="trend-number">
                      {dashboard.average_improvement >= 0
                        ? "+"
                        : ""}
                      {dashboard.average_improvement.toFixed(2)}
                    </div>
                  </div>

                  <div className="trend-bar">
                    <div
                      className={
                        dashboard.average_improvement >= 0
                          ? "trend-progress improving"
                          : "trend-progress declining"
                      }
                      style={{
                        width: `${Math.min(
                          Math.max(
                            Math.abs(
                              dashboard.average_improvement
                            ) * 10,
                            5
                          ),
                          100
                        )}%`,
                      }}
                    />
                  </div>

                  <p>
                    Average improvement across subjects
                  </p>
                </div>
              </div>
            </section>

            {/* ANALYTICS */}

            <section
              id="analytics-section"
              className="dashboard-section"
            >
              <div className="section-title">
                <span>
                  ANALYTICS
                </span>

                <h2>
                  Academic Analytics
                </h2>

                <p>
                  A quick view of your important academic metrics.
                </p>
              </div>

              <div className="stats-grid">
                <div className="stat-card">
                  <div className="stat-top">
                    <span>
                      Average Mark
                    </span>

                    <div className="stat-icon purple">
                      📊
                    </div>
                  </div>

                  <div className="stat-value">
                    {dashboard.average.toFixed(2)}
                  </div>

                  <div className="stat-description">
                    Overall academic average
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-top">
                    <span>
                      Attendance
                    </span>

                    <div className="stat-icon blue">
                      📅
                    </div>
                  </div>

                  <div className="stat-value">
                    {dashboard.attendance.toFixed(2)}%
                  </div>

                  <div className="stat-description">
                    Overall attendance
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-top">
                    <span>
                      Academic Risk
                    </span>

                    <div className="stat-icon green">
                      🛡️
                    </div>
                  </div>

                  <div
                    className={
                      dashboard.risk_level
                        .toLowerCase()
                        .includes("high")
                        ? "stat-value risk-high"
                        : "stat-value risk-low"
                    }
                  >
                    {dashboard.risk_level}
                  </div>

                  <div className="stat-description">
                    Risk probability:{" "}
                    {dashboard.risk_probability.toFixed(2)}%
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-top">
                    <span>
                      Performance
                    </span>

                    <div className="stat-icon orange">
                      ⭐
                    </div>
                  </div>

                  <div className="stat-value performance-value">
                    {dashboard.performance_status}
                  </div>

                  <div className="stat-description">
                    Current performance status
                  </div>
                </div>
              </div>
            </section>

            {/* INSIGHTS */}

            <section
              id="insights-section"
              className="dashboard-section"
            >
              <div className="section-title">
                <span>
                  INSIGHTS
                </span>

                <h2>
                  AI-Powered Insights
                </h2>

                <p>
                  Personalized guidance based on your academic data.
                </p>
              </div>

              <div className="panel insight-panel">
                <div className="panel-header">
                  <div>
                    <h2>
                      AI Insight
                    </h2>

                    <p>
                      Personalized recommendation
                    </p>
                  </div>

                  <div className="ai-small-icon">
                    🤖
                  </div>
                </div>

                <div className="recommendation-box">
                  <div className="recommendation-icon">
                    💡
                  </div>

                  <p>
                    {dashboard.recommendation}
                  </p>
                </div>

                <div className="priority-box">
                  <span>
                    Priority Subject
                  </span>

                  <div>
                    <strong>
                      {dashboard.priority_subject}
                    </strong>

                    <span>
                      {dashboard.priority_mark.toFixed(2)} marks
                    </span>
                  </div>
                </div>

                <button
                  className="ask-ai-button"
                  onClick={() =>
                    setIsChatOpen(true)
                  }
                >
                  🤖 Ask AI Assistant
                </button>
              </div>
            </section>
          </>
        )}
      </main>

      {/* PROFILE MODAL */}

      {isProfileOpen && (
        <div
          className="modal-overlay"
          onClick={() =>
            setIsProfileOpen(false)
          }
        >
          <div
            className="profile-modal"
            onClick={(event) =>
              event.stopPropagation()
            }
          >
            <div className="modal-header">
              <div>
                <h2>
                  Academic Profile
                </h2>

                <p>
                  Your account information
                </p>
              </div>

              <button
                type="button"
                className="modal-close"
                onClick={() =>
                  setIsProfileOpen(false)
                }
              >
                ✕
              </button>
            </div>

            <div className="profile-main">
              <div className="profile-large-avatar">
                {studentName
                  .charAt(0)
                  .toUpperCase()}
              </div>

              <div>
                <h3>
                  {studentName}
                </h3>

                <span>
                  Student Account
                </span>
              </div>
            </div>

            <div className="profile-details">
              <div className="profile-detail-item">
                <span>
                  🎓 Student ID
                </span>

                <strong>
                  {savedStudentId ||
                    "Not available"}
                </strong>
              </div>

              <div className="profile-detail-item">
                <span>
                  👤 Username
                </span>

                <strong>
                  {savedUsername ||
                    "Not available"}
                </strong>
              </div>

              <div className="profile-detail-item">
                <span>
                  🧑‍🎓 Account Type
                </span>

                <strong>
                  Student
                </strong>
              </div>
            </div>

            <div className="profile-actions">
              <button
                type="button"
                className="change-password-button"
                onClick={
                  openChangePassword
                }
              >
                🔒 Change Password
              </button>

              <button
                type="button"
                className="change-password-button"
                onClick={
                  openChangeEmail
                }
              >
                ✉️ Change Email
              </button>

              <button
                type="button"
                className="profile-close-button"
                onClick={() =>
                  setIsProfileOpen(false)
                }
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* CHANGE PASSWORD MODAL */}

      {isChangePasswordOpen && (
        <div
          className="modal-overlay"
          onClick={
            closeChangePassword
          }
        >
          <div
            className="password-modal"
            onClick={(event) =>
              event.stopPropagation()
            }
          >
            <div className="modal-header">
              <div>
                <h2>
                  Change Password
                </h2>

                <p>
                  Keep your Student AI account secure.
                </p>
              </div>

              <button
                type="button"
                className="modal-close"
                onClick={
                  closeChangePassword
                }
              >
                ✕
              </button>
            </div>

            {passwordChangeError && (
              <div className="password-message error">
                <span>⚠️</span>
                {passwordChangeError}
              </div>
            )}

            {passwordChangeSuccess && (
              <div className="password-message success">
                <span>✓</span>
                {passwordChangeSuccess}
              </div>
            )}

            <div className="password-form">

              {/* CURRENT PASSWORD */}

              <div className="form-group">
                <label>
                  Current Password
                </label>

                <div className="input-wrapper password-wrapper">
                  <span>🔒</span>

                  <input
                    type={
                      showCurrentPassword
                        ? "text"
                        : "password"
                    }
                    placeholder="Enter current password"
                    value={
                      currentPassword
                    }
                    onChange={(event) =>
                      setCurrentPassword(
                        event.target.value
                      )
                    }
                    disabled={
                      passwordChangeLoading ||
                      passwordCodeSending
                    }
                  />

                  <button
                    type="button"
                    className="password-toggle"
                    onClick={() =>
                      setShowCurrentPassword(
                        (prev) => !prev
                      )
                    }
                    disabled={
                      passwordChangeLoading ||
                      passwordCodeSending
                    }
                  >
                    {showCurrentPassword
                      ? "🙈"
                      : "👁️"}
                  </button>
                </div>
              </div>

              {/* SEND CODE */}

              {!passwordCodeSent && (
                <button
                  type="button"
                  className="change-password-button"
                  onClick={
                    handleSendPasswordChangeCode
                  }
                  disabled={
                    passwordCodeSending ||
                    passwordChangeLoading
                  }
                >
                  {passwordCodeSending ? (
                    <>
                      <span className="button-spinner" />
                      Sending Code...
                    </>
                  ) : (
                    <>
                      ✉️ Send Verification Code
                    </>
                  )}
                </button>
              )}

              {/* CODE */}

              {passwordCodeSent && (
                <>
                  <div className="verification-email-info">
                    <div className="verification-icon">
                      ✉️
                    </div>

                    <div>
                      <strong>
                        Check your email
                      </strong>

                      <span>
                        Enter the 6-digit verification code sent to your registered email.
                      </span>
                    </div>
                  </div>

                  <div className="form-group">
                    <label>
                      Verification Code
                    </label>

                    <div className="input-wrapper code-input-wrapper">
                      <span>🔢</span>

                      <input
                        type="text"
                        inputMode="numeric"
                        maxLength={6}
                        placeholder="Enter 6-digit code"
                        value={
                          passwordVerificationCode
                        }
                        onChange={(event) =>
                          setPasswordVerificationCode(
                            event.target.value.replace(
                              /\D/g,
                              ""
                            )
                          )
                        }
                        disabled={
                          passwordChangeLoading
                        }
                      />
                    </div>
                  </div>

                  {/* NEW PASSWORD */}

                  <div className="form-group">
                    <label>
                      New Password
                    </label>

                    <div className="input-wrapper password-wrapper">
                      <span>🔑</span>

                      <input
                        type={
                          showNewPassword
                            ? "text"
                            : "password"
                        }
                        placeholder="Enter new password"
                        value={
                          newPassword
                        }
                        onChange={(event) =>
                          setNewPassword(
                            event.target.value
                          )
                        }
                        disabled={
                          passwordChangeLoading
                        }
                      />

                      <button
                        type="button"
                        className="password-toggle"
                        onClick={() =>
                          setShowNewPassword(
                            (prev) => !prev
                          )
                        }
                        disabled={
                          passwordChangeLoading
                        }
                      >
                        {showNewPassword
                          ? "🙈"
                          : "👁️"}
                      </button>
                    </div>
                  </div>

                  {/* CONFIRM PASSWORD */}

                  <div className="form-group">
                    <label>
                      Confirm New Password
                    </label>

                    <div className="input-wrapper password-wrapper">
                      <span>🔐</span>

                      <input
                        type={
                          showConfirmPassword
                            ? "text"
                            : "password"
                        }
                        placeholder="Confirm new password"
                        value={
                          confirmPassword
                        }
                        onChange={(event) =>
                          setConfirmPassword(
                            event.target.value
                          )
                        }
                        disabled={
                          passwordChangeLoading
                        }
                      />

                      <button
                        type="button"
                        className="password-toggle"
                        onClick={() =>
                          setShowConfirmPassword(
                            (prev) => !prev
                          )
                        }
                        disabled={
                          passwordChangeLoading
                        }
                      >
                        {showConfirmPassword
                          ? "🙈"
                          : "👁️"}
                      </button>
                    </div>
                  </div>

                  <small className="field-hint">
                    Password must be at least 6 characters.
                  </small>
                </>
              )}
            </div>

            <div className="password-modal-actions">
              <button
                type="button"
                className="profile-close-button"
                onClick={
                  closeChangePassword
                }
                disabled={
                  passwordChangeLoading ||
                  passwordCodeSending
                }
              >
                Cancel
              </button>

              {passwordCodeSent && (
                <button
                  type="button"
                  className="change-password-button"
                  onClick={
                    handleChangePassword
                  }
                  disabled={
                    passwordChangeLoading
                  }
                >
                  {passwordChangeLoading ? (
                    <>
                      <span className="button-spinner" />
                      Updating...
                    </>
                  ) : (
                    "🔒 Update Password"
                  )}
                </button>
              )}
            </div>
          </div>
        </div>
      )}

      {/* CHANGE EMAIL MODAL */}

      {isChangeEmailOpen && (
        <div
          className="modal-overlay"
          onClick={
            closeChangeEmail
          }
        >
          <div
            className="password-modal"
            onClick={(event) =>
              event.stopPropagation()
            }
          >
            <div className="modal-header">
              <div>
                <h2>
                  Change Email
                </h2>

                <p>
                  Update the email linked to your Student AI account.
                </p>
              </div>

              <button
                type="button"
                className="modal-close"
                onClick={
                  closeChangeEmail
                }
              >
                ✕
              </button>
            </div>

            {emailChangeError && (
              <div className="password-message error">
                <span>⚠️</span>
                {emailChangeError}
              </div>
            )}

            {emailChangeSuccess && (
              <div className="password-message success">
                <span>✓</span>
                {emailChangeSuccess}
              </div>
            )}

            <div className="password-form">

              {/* NEW EMAIL */}

              <div className="form-group">
                <label htmlFor="new-email">
                  New Email Address
                </label>

                <div className="input-wrapper">
                  <span>✉️</span>

                  <input
                    id="new-email"
                    type="email"
                    placeholder="Enter your new email address"
                    value={newEmail}
                    onChange={(event) =>
                      setNewEmail(
                        event.target.value
                      )
                    }
                    autoComplete="email"
                    disabled={
                      emailCodeSending ||
                      emailChangeLoading ||
                      emailCodeSent
                    }
                  />
                </div>

                <small className="field-hint">
                  A verification code will be sent to this new email address.
                </small>
              </div>

              {/* SEND EMAIL CODE */}

              {!emailCodeSent && (
                <button
                  type="button"
                  className="change-password-button"
                  onClick={
                    handleRequestEmailChange
                  }
                  disabled={
                    emailCodeSending ||
                    emailChangeLoading
                  }
                >
                  {emailCodeSending ? (
                    <>
                      <span className="button-spinner" />
                      Sending Code...
                    </>
                  ) : (
                    <>
                      ✉️ Send Verification Code
                    </>
                  )}
                </button>
              )}

              {/* VERIFY EMAIL CODE */}

              {emailCodeSent && (
                <>
                  <div className="verification-email-info">
                    <div className="verification-icon">
                      ✉️
                    </div>

                    <div>
                      <strong>
                        Check your new email
                      </strong>

                      <span>
                        Enter the 6-digit verification code sent to your new email address.
                      </span>
                    </div>
                  </div>

                  <div className="form-group">
                    <label htmlFor="email-change-code">
                      Verification Code
                    </label>

                    <div className="input-wrapper code-input-wrapper">
                      <span>🔢</span>

                      <input
                        id="email-change-code"
                        type="text"
                        inputMode="numeric"
                        maxLength={6}
                        placeholder="Enter 6-digit code"
                        value={
                          emailVerificationCode
                        }
                        onChange={(event) =>
                          setEmailVerificationCode(
                            event.target.value.replace(
                              /\D/g,
                              ""
                            )
                          )
                        }
                        disabled={
                          emailChangeLoading
                        }
                      />
                    </div>
                  </div>
                </>
              )}
            </div>

            <div className="password-modal-actions">
              <button
                type="button"
                className="profile-close-button"
                onClick={
                  closeChangeEmail
                }
                disabled={
                  emailCodeSending ||
                  emailChangeLoading
                }
              >
                Cancel
              </button>

              {emailCodeSent && (
                <button
                  type="button"
                  className="change-password-button"
                  onClick={
                    handleVerifyEmailChange
                  }
                  disabled={
                    emailChangeLoading
                  }
                >
                  {emailChangeLoading ? (
                    <>
                      <span className="button-spinner" />
                      Verifying...
                    </>
                  ) : (
                    "✓ Verify & Update Email"
                  )}
                </button>
              )}
            </div>
          </div>
        </div>
      )}

      {/* FLOATING AI */}

      {!isChatOpen && (
        <button
          className="floating-ai-button"
          onClick={() =>
            setIsChatOpen(true)
          }
        >
          <span className="floating-ai-icon">
            🤖
          </span>

          <span>
            Ask AI
          </span>
        </button>
      )}

      {/* CHAT */}

      {isChatOpen && (
        <>
          <div
            className="chat-overlay"
            onClick={() =>
              setIsChatOpen(false)
            }
          />

          <aside className="chat-panel">
            <div className="chat-panel-header">
              <div className="chat-title">
                <div className="chat-avatar">
                  🤖
                </div>

                <div>
                  <h2>
                    Student AI
                  </h2>

                  <span>
                    Your academic assistant
                  </span>
                </div>
              </div>

              <button
                className="chat-close"
                onClick={() =>
                  setIsChatOpen(false)
                }
              >
                ✕
              </button>
            </div>

            <div className="chat-messages">
              {messages.map(
                (msg, index) => (
                  <div
                    key={index}
                    className={`message-row ${msg.sender}`}
                  >
                    <div className="message-bubble">
                      {msg.text}
                    </div>
                  </div>
                )
              )}

              {loading && (
                <div className="message-row ai">
                  <div className="message-bubble typing">
                    <span />
                    <span />
                    <span />
                  </div>
                </div>
              )}

              <div ref={chatEndRef} />
            </div>

            <div className="chat-input-area">
              <input
                type="text"
                placeholder="Ask about your academics..."
                value={message}
                onChange={(event) =>
                  setMessage(
                    event.target.value
                  )
                }
                onKeyDown={
                  handleChatKeyDown
                }
                disabled={loading}
              />

              <button
                onClick={sendMessage}
                disabled={
                  loading ||
                  !message.trim()
                }
              >
                ➤
              </button>
            </div>
          </aside>
        </>
      )}
    </div>
  );
}

export default App;