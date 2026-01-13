import { StrictMode, lazy, Suspense } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./common/index.css";
import App from "./App";
import { initGlobalErrorHandler } from "./common/logger";

// 懒加载 Admin 模块
const AdminApp = lazy(() => import("./AdminApp"));

// 初始化全局错误处理
initGlobalErrorHandler();

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route
          path="/admin/*"
          element={
            <Suspense
              fallback={
                <div className="flex items-center justify-center h-screen">
                  Loading...
                </div>
              }
            >
              <AdminApp />
            </Suspense>
          }
        />
        <Route path="/*" element={<App />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>
);
