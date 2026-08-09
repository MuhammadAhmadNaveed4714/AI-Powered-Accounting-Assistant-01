import { Navigate, useLocation } from "react-router-dom";

function ProtectedRoute({ children }) {

    const token = localStorage.getItem("token");

    const user = JSON.parse(
        localStorage.getItem("user")
    );

    const location = useLocation();


    // =========================================
    // User not logged in
    // =========================================

    if (!token || !user) {

        return <Navigate to="/login" replace />;

    }


    // =========================================
    // Prevent normal users from accessing Admin Dashboard
    // =========================================

    if (
        location.pathname === "/admin-dashboard" &&
        user.role !== "admin"
    ) {

        return <Navigate to="/dashboard" replace />;

    }


    // =========================================
    // Allow access
    // =========================================

    return children;

}

export default ProtectedRoute;
