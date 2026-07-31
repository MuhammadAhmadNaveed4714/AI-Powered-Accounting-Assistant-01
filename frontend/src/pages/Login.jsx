import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/api";
import { toast } from "react-toastify";
import "../styles/auth.css";
import { Link } from "react-router-dom";
function Login() {

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleLogin = async (e) => {

        e.preventDefault();

        try {

            const response = await API.post("/login", {
                email,
                password
            });


           // Save JWT Token
localStorage.setItem(
    "token",
    response.data.access_token
);

// Save Complete User
localStorage.setItem(
    "user",
    JSON.stringify(response.data.user)
);

            toast.success("Login successful!");

            if (response.data.user.role === "admin") {

                navigate("/admin-dashboard", {
                    replace: true
                });

            } else {

                navigate("/dashboard", {
                    replace: true
                });

            }


        } catch (error) {

            toast.error(
    error.response?.data?.message ||
    "Login failed."
);

        }

    };
    

    useEffect(() => {

    document.title = "Login | AI Accounting Assistant";

}, []);

   return (

<div className="auth-container">

<div className="auth-card">

<div className="logo">
💰
</div>

<h2>Welcome Back</h2>

<p className="subtitle">
AI-Powered Accounting Assistant
</p>

<form onSubmit={handleLogin}>

<input
className="auth-input"
type="email"
placeholder="📧 Email Address"
value={email}
onChange={(e)=>setEmail(e.target.value)}
/>

<input
className="auth-input"
type="password"
placeholder="🔒 Password"
value={password}
onChange={(e)=>setPassword(e.target.value)}
/>

<button
className="auth-btn"
type="submit"
>

Login

</button>

</form>

<div className="auth-link">

Don't have an account?

{" "}

<Link to="/register">

Register

</Link>

</div>

</div>

</div>

);
}


export default Login;