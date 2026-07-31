import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/api";
import { toast } from "react-toastify";
import "../styles/auth.css";
import { Link } from "react-router-dom";
function Register() {

    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();
    const handleRegister = async (e) => {

        e.preventDefault();

        try {

            const response = await API.post("/register", {
                username,
                email,
                password
            });

            toast.success("Registration successful!");
            setUsername("");
            setEmail("");
            setPassword("");


            setTimeout(() => {

            navigate("/login", {
            replace: true
            });

           }, 1500); 

        } catch (error) {

            toast.error(
    error.response?.data?.message ||
    "Registration failed."
);

        }

    };
    


    useEffect(() => {

    document.title = "Register | AI Accounting Assistant";

}, []);


   return (

<div className="auth-container">

<div className="auth-card">

<div className="logo">
📝
</div>

<h2>Create Account</h2>

<p className="subtitle">
Start Managing Your Finances
</p>

<form onSubmit={handleRegister}>

<input
className="auth-input"
type="text"
placeholder="👤 Username"
value={username}
onChange={(e)=>setUsername(e.target.value)}
/>

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

Create Account

</button>

</form>

<div className="auth-link">

Already have an account?

{" "}

<Link to="/login">

Login

</Link>

</div>

</div>

</div>

);
}

export default Register;