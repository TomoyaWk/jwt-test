import "./App.css";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Login from "./components/Login";
import Register from "./components/Register";
import Top from "./components/Top";

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col items-center justify-center p-4">
        <div className="mb-4 flex gap-4">
          <Link to="/" className="text-blue-500 hover:text-blue-700">
            Login
          </Link>
          <Link to="/register" className="text-blue-500 hover:text-blue-700">
            Register
          </Link>
        </div>

        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/top" element={<Top />} />
          <Route
            path="*"
            element={
              <div className="text-center">
                <h1 className="text-2xl font-bold mb-4">
                  404 - Page Not Found
                </h1>
                <p className="mb-4">お探しのページは見つかりませんでした。</p>
                <Link to="/" className="text-blue-500 hover:text-blue-700">
                  ログインに戻る
                </Link>
              </div>
            }
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
