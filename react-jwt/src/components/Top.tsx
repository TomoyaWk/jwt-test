import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

function Top() {
  const navigate = useNavigate();
  const [loginUser, setLoginUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [userList, setUserList] = useState<User[]>([]);

  type User = {
    id: number;
    username: string;
    password: string;
    created_at?: Date;
    updated_at?: Date;
  };

  useEffect(() => {
    const fetchLoginData = async () => {
      try {
        // アクセストークンを取得
        const accessToken = localStorage.getItem("accessToken");

        // ユーザー情報を取得するAPIリクエスト
        const response = await fetch("http://localhost:5100/users/me", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${accessToken}`,
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error("認証エラーまたはAPIエラー");
        }

        const userData = await response.json();
        setLoginUser(userData);
        setLoading(false);
      } catch (error) {
        console.error("認証エラー:", error);
        // エラー発生時はログインページへリダイレクト
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        navigate("/");
      }
    };

    fetchLoginData();

    const fetchUserData = async () => {
      try {
        // アクセストークンを取得
        const accessToken = localStorage.getItem("accessToken");
        // ユーザー一覧を取得
        const response = await fetch("http://localhost:5100/users/", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${accessToken}`,
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error("認証エラーまたはAPIエラー");
        }

        const userListData = await response.json();
        setUserList(userListData);
      } catch (error) {
        console.error("ユーザー取得エラー:", error);
      }
    };
    fetchUserData();
  }, [navigate]);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="flex flex-col items-center gap-4 mb-8 rounded-md p-4">
      <h2 className="text-3xl font-bold text-center">Top Page</h2>

      <div className="flex flex-row gap-4 items-center">
        {loginUser && (
          <div className="text-center">
            <p>ようこそ {loginUser.username}さん</p>
          </div>
        )}
        <button
          onClick={() => {
            localStorage.removeItem("accessToken");
            localStorage.removeItem("refreshToken");
            navigate("/");
          }}
          className="px-3 py-1 border border-red-300 text-red text-md rounded-md"
        >
          Logout
        </button>
      </div>
      <div className="flex flex-col gap-4 w-full max-w-md">
        {userList.map((user) => {
          return (
            <div
              key={user.id}
              className="flex flex-row justify-between items-center border border-gray-300 rounded-md p-2"
            >
              <div>{user.id}</div>
              <div>{user.username}</div>
              <div>
                {user.created_at
                  ? new Date(user.created_at).toLocaleString("ja-JP")
                  : ""}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default Top;
