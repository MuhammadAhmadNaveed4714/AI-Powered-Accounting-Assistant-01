import {
    BrowserRouter,
    Routes,
    Route,
    Navigate
} from "react-router-dom";

import Register from "./pages/Register";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Expenses from "./pages/Expenses";
import Income from "./pages/Income";
import ProtectedRoute from "./components/ProtectedRoute";
import AdminDashboard from "./pages/AdminDashboard";
function App() {
  return (
    <BrowserRouter>
     <Routes>
     

     <Route
    path="/"
    element={<Navigate to="/login" />}
/>



    {/* Register */}
    <Route
        path="/register"
        element={<Register />}
    />

    {/* Login */}
    <Route
        path="/login"
        element={<Login />}
    />

    <Route
    path="/dashboard"
    element={
        <ProtectedRoute>
            <Dashboard />
        </ProtectedRoute>
    }
/>

<Route
    path="/expenses"
    element={
        <ProtectedRoute>
            <Expenses />
        </ProtectedRoute>
    }
/>

<Route
    path="/income"
    element={
        <ProtectedRoute>
            <Income />
        </ProtectedRoute>
    }
/>


<Route
    path="/admin-dashboard"
    element={
        <ProtectedRoute>
            <AdminDashboard />
        </ProtectedRoute>
    }
/>


</Routes>
    </BrowserRouter>
  );
}

export default App;