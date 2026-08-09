import { Link, useNavigate } from "react-router-dom";
import "../styles/navbar.css";
function Navbar() {

    const navigate = useNavigate();
    
    const user = JSON.parse(localStorage.getItem("user"));



   const logout = () => {

    if (!window.confirm("Are you sure you want to logout?")) {

        return;

    }

    localStorage.removeItem("token");
    localStorage.removeItem("user");

    navigate("/login", { replace: true });

};

    return (

    <div className="navbar">

        <h2 className="navbar-logo">
            AI Accounting Assistant
        </h2>

        <div className="navbar-links">

    {user?.role === "admin" && (

        <Link to="/admin-dashboard">
    Admin Panel
</Link>

    )}

    <Link to="/dashboard">
        Dashboard
    </Link>

    <Link to="/expenses">
        Expenses
    </Link>

    <Link to="/income">
        Income
    </Link>


    <Link to="/documents">
    Documents
    </Link>

</div>

        <button
            className="logout-btn"
            onClick={logout}
        >
            Logout
        </button>

    </div>

);

}

export default Navbar;