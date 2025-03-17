import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const navigate = useNavigate();

  //登録ボタン押下
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setMsg("確認用とパスワードが一致しません");
      return;
    }
    console.log("Registration attempt with:", { username, password });
    // 登録処理
    registerRequest(username, password);
  };

  //ユーザー登録
  const registerRequest = async (username: string, password: string) => {
    try {
      const response = await fetch("http://localhost:5100/auth/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok) {
        console.log("Registration success", data);
        setMsg("");
        // 登録成功後にログインページへリダイレクト
        navigate("/");
      } else {
        console.error("Registration failed:", data.msg || response.statusText);
        setMsg(data.msg || "登録に失敗しました");
      }
    } catch (error) {
      console.error("Registration failed:", error);
      setMsg("登録に失敗しました");
    }
  };

  return (
    <div className="flex flex-col items-center gap-4 mb-8 border border-gray-300 rounded-md p-4">
      <h2 className="text-3xl font-bold text-center">Register</h2>
      <form
        onSubmit={handleSubmit}
        className="flex flex-col items-center w-full"
      >
        <div className="flex flex-col gap-3 w-full max-w-xs">
          <input
            type="text"
            name="user_name"
            className="px-4 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="ユーザー名"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="password"
            name="password"
            className="px-4 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="パスワード"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <input
            type="password"
            name="confirm_password"
            className="px-4 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="パスワードの確認"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
        </div>
        <div>
          {msg && (
            <div
              className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mt-4 w-full max-w-xs"
              role="alert"
            >
              <span className="block sm:inline">{msg}</span>
            </div>
          )}
        </div>
        <div>
          <button
            type="submit"
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md mb-4 mt-4 transition-colors"
          >
            登録
          </button>
        </div>
      </form>
    </div>
  );
}

export default Register;
