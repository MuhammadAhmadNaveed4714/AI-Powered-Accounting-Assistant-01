import {
    BrowserRouter,
    Routes,
    Route,
    Navigate
} from "react-router-dom";

import Documents from "./pages/Documents";
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

                {/* =========================================
                    Home
                ========================================= */}

                <Route
                    path="/"
                    element={
                        <Navigate
                            to="/login"
                            replace
                        />
                    }
                />


                {/* =========================================
                    Register
                ========================================= */}

                <Route
                    path="/register"
                    element={<Register />}
                />


                {/* =========================================
                    Login
                ========================================= */}

                <Route
                    path="/login"
                    element={<Login />}
                />


                {/* =========================================
                    User Dashboard
                ========================================= */}

                <Route
                    path="/dashboard"
                    element={
                        <ProtectedRoute>
                            <Dashboard />
                        </ProtectedRoute>
                    }
                />


                {/* =========================================
                    Expenses
                ========================================= */}

                <Route
                    path="/expenses"
                    element={
                        <ProtectedRoute>
                            <Expenses />
                        </ProtectedRoute>
                    }
                />


                {/* =========================================
                    Documents
                ========================================= */}

                <Route
                    path="/documents"
                    element={
                        <ProtectedRoute>
                            <Documents />
                        </ProtectedRoute>
                    }
                />


                {/* =========================================
                    Income
                ========================================= */}

                <Route
                    path="/income"
                    element={
                        <ProtectedRoute>
                            <Income />
                        </ProtectedRoute>
                    }
                />


                {/* =========================================
                    Admin Dashboard
                ========================================= */}

                <Route
                    path="/admin-dashboard"
                    element={
                        <ProtectedRoute>
                            <AdminDashboard />
                        </ProtectedRoute>
                    }
                />


                {/* =========================================
                    Unknown Route
                ========================================= */}

                <Route
                    path="*"
                    element={
                        <Navigate
                            to="/login"
                            replace
                        />
                    }
                />

            </Routes>

        </BrowserRouter>

    );

}


export default App;
