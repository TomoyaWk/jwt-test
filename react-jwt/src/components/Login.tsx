import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      const response = await fetch("http://localhost:5100/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Credentials": "true",
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.msg || "ログインに失敗しました");
      }

      // トークンをローカルストレージに保存
      localStorage.setItem("accessToken", data.access_token);
      localStorage.setItem("refreshToken", data.refresh_token);

      console.log("Login successful", data);

      // ログイン後のリダイレクト先
      // ここを実装する場合は、保護されたルートを作成する必要があります
      navigate("/top");
    } catch (error) {
      console.error("Login error:", error);
      setError(
        error instanceof Error ? error.message : "ログインに失敗しました"
      );
    }
  };

  return (
    <div className="flex flex-col items-center gap-4 mb-8 border border-gray-300 rounded-md p-4">
      <h2 className="text-3xl font-bold text-center">Login</h2>
      <form
        onSubmit={handleSubmit}
        className="flex flex-col items-center w-full"
      >
        <div className="flex flex-col gap-3 w-full max-w-xs">
          <input
            type="text"
            name="user_name"
            className="px-4 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter your username..."
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="password"
            name="password"
            className="px-4 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter your password..."
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        {error && <div className="text-red-500 mt-2">{error}</div>}
        <div>
          <button
            type="submit"
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md mb-4 mt-4 transition-colors"
          >
            Login
          </button>
        </div>
      </form>
    </div>
  );
}

export default Login;
