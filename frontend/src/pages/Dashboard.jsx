import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/api";
import Navbar from "../components/Navbar";
import "../styles/dashboard.css";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import Footer from "../components/Footer";
import { toast } from "react-toastify";
import axios from "axios";
import AIChatWidget from "../components/AIChatWidget";
import {
    FaMoneyBillWave,
    FaWallet,
    FaChartLine
} from "react-icons/fa";
import {
    PieChart,
    Pie,
    Cell,
    Tooltip,
    Legend,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    LineChart,
    Line,
    ResponsiveContainer
} from "recharts";

function Dashboard() {
    
    const navigate = useNavigate();
    const [darkMode, setDarkMode] = useState(false);
    const [summary, setSummary] = useState({
        total_income: 0,
        total_expenses: 0,
        balance: 0,
        insight: "",
        recommendation: "",
        categories: [],
        monthly_summary: []
    });

    const [categoryData, setCategoryData] = useState([]);
    const [monthlyData, setMonthlyData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [dateFilter, setDateFilter] = useState("all"); 
    const fetchSummary = async () => {

    try {

        setLoading(true);

        const token = localStorage.getItem("token");


        const response = await API.get(
            "/dashboard",
            {
                params: {
                    filter: dateFilter
                },

                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );


        setSummary(response.data);

        setCategoryData(
            response.data.categories || []
        );

        setMonthlyData(
            response.data.monthly_summary || []
        );


    } 
    catch (error) {


        console.log(error);


        if(error.response?.status === 401){


            toast.error(
                "Session expired. Please login again."
            );


            localStorage.removeItem("token");
            localStorage.removeItem("user");
            localStorage.removeItem("role");


            navigate("/login");


        }
        else {


            toast.error(
                "Failed to load dashboard data."
            );


        }


    }
    finally {


        setLoading(false);


    }

};

    useEffect(() => {

    const savedTheme = localStorage.getItem("darkMode");

    setDarkMode(savedTheme === "true");

    document.title = "Dashboard | AI Accounting Assistant";

}, []);


useEffect(() => {

    fetchSummary();

}, [dateFilter]);

    const data = [
        {
            name: "Income",
            value: summary.total_income
        },
        {
            name: "Expenses",
            value: summary.total_expenses
        }
    ];

    const COLORS = ["#00C49F", "#FF8042"];

    const downloadPDF = () => {

        const doc = new jsPDF();

        doc.setFontSize(20);
        doc.text("AI Accounting Assistant Report", 20, 20);

        doc.setFontSize(11);
        doc.text(
            `Generated on: ${new Date().toLocaleString()}`,
            20,
            30
        );

        autoTable(doc, {
            startY: 40,
            head: [["Summary", "Value"]],
            body: [
               [
    "Total Income",
    `Rs. ${(summary.total_income || 0).toFixed(2)}`
],

[
    "Total Expenses",
    `Rs. ${(summary.total_expenses || 0).toFixed(2)}`
],

[
    "Balance",
    `Rs. ${(summary.balance || 0).toFixed(2)}`
]
            ]
        });

        const firstTableY = doc.lastAutoTable
            ? doc.lastAutoTable.finalY
            : 40;

        doc.setFontSize(14);
        doc.text(
            "AI Financial Insight:",
            20,
            firstTableY + 15
        );

        doc.setFontSize(11);
        doc.text(
            summary.insight || "No insight available.",
            20,
            firstTableY + 25
        );

        doc.setFontSize(14);
        doc.text(
            "AI Recommendation:",
            20,
            firstTableY + 40
        );

        doc.setFontSize(11);
        doc.text(
            summary.recommendation || "No recommendation available.",
            20,
            firstTableY + 50
        );

        const categoryRows =
            categoryData.length > 0
                ? categoryData.map((item) => [
                      item.category,
                      `Rs. ${item.total}`
                  ])
                : [["No Data", "-"]];

        autoTable(doc, {
            startY: firstTableY + 60,
            head: [["Category", "Amount"]],
            body: categoryRows
        });

        doc.save("AI_Accounting_Report.pdf");

    };



const downloadAIReport = async () => {

    try {

        const token = localStorage.getItem("token");


        const response = await axios.get(
            "http://127.0.0.1:5000/ai/report",
            {
                headers: {
                    Authorization: `Bearer ${token}`
                },

                responseType: "blob"
            }
        );


        const file = new Blob(
            [response.data],
            {
                type: "application/pdf"
            }
        );


        const url = window.URL.createObjectURL(
            file
        );


        const link = document.createElement("a");

        link.href = url;

        link.download = "AI_Financial_Report.pdf";


        document.body.appendChild(link);

        link.click();


        link.remove();


    } catch (error) {

        console.log(error);

        alert(
            "Failed to generate AI report"
        );

    }

};

    if (loading) {

   return (

        <div className="loading-container">

            <div className="loading-spinner"></div>

            <p className="loading-text">
                Loading Dashboard...
            </p>

        </div>

    );

}


    return (

        <div className={darkMode ? "page-container dark" : "page-container"}>

            <Navbar />

            <h1 className="center-heading">
    AI Accounting Dashboard
</h1>


<div
    style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        flexWrap: "wrap",
        gap: "15px",
        marginBottom: "20px"
    }}
>

    <div>

        <label
            style={{
                fontWeight: "bold",
                marginRight: "10px"
            }}
        >
            Date Filter:
        </label>

        <select
            value={dateFilter}
            onChange={(e) => setDateFilter(e.target.value)}
            style={{
                padding: "10px",
                borderRadius: "8px",
                border: "1px solid #ccc",
                fontSize: "15px"
            }}
        >

            <option value="all">
                All Time
            </option>

            <option value="this_month">
                This Month
            </option>

            <option value="last_month">
                Last Month
            </option>

            <option value="this_year">
                This Year
            </option>

        </select>

    </div>


    <div
        style={{
            display: "flex",
            gap: "10px",
            flexWrap: "wrap"
        }}
    >

        <button
            onClick={() => {

                const newMode = !darkMode;

                setDarkMode(newMode);

                localStorage.setItem(
                    "darkMode",
                    String(newMode)
                );

            }}
            style={{
                padding: "10px 20px",
                backgroundColor: darkMode
                    ? "#fbc02d"
                    : "#333",
                color: darkMode
                    ? "black"
                    : "white",
                border: "none",
                borderRadius: "5px",
                cursor: "pointer",
                fontWeight: "bold"
            }}
        >

            {
                darkMode
                    ? "☀️ Light Mode"
                    : "🌙 Dark Mode"
            }

        </button>


        <button
            onClick={downloadPDF}
            style={{
                padding: "10px 20px",
                backgroundColor: "#1976D2",
                color: "white",
                border: "none",
                borderRadius: "5px",
                cursor: "pointer",
                fontWeight: "bold"
            }}
        >

            📄 Download PDF Report

        </button>

        <button
    onClick={downloadAIReport}
    style={{
        backgroundColor:"#1976D2",
        color:"white",
        padding:"10px 20px",
        border:"none",
        borderRadius:"5px",
        cursor:"pointer"
    }}
>
    🤖 Generate AI Financial Report
</button>

    </div>

</div>

<hr />
           
     <div className="cards">

    <div className="card income-card">

        <div className="card-icon">
            <FaMoneyBillWave />
        </div>

        <h2>Total Income</h2>

        <h3>
           Rs. {(summary.total_income || 0).toFixed(2)}
        </h3>

    </div>

    <div className="card expense-card">

        <div className="card-icon">
            <FaChartLine />
        </div>

        <h2>Total Expenses</h2>

        <h3>
            Rs. {(summary.total_expenses || 0).toFixed(2)}
        </h3>

    </div>

    <div className="card balance-card">

        <div className="card-icon">
            <FaWallet />
        </div>

        <h2>Balance</h2>

        <h3>
            Rs. {(summary.balance || 0).toFixed(2)}
        </h3>

    </div>



</div>

            <hr />

            <h2 className="chart-title">
                Income vs Expenses
            </h2>

          <div className="chart-container">

                <ResponsiveContainer width="100%" height={300}>

    <PieChart>

        <Pie
            data={data}
            cx="50%"
            cy="50%"
            outerRadius={100}
            dataKey="value"
            label
        >

            {data.map((entry, index) => (

                <Cell
                    key={`cell-${index}`}
                    fill={COLORS[index % COLORS.length]}
                />

            ))}

        </Pie>

        <Tooltip />

        <Legend />

    </PieChart>

</ResponsiveContainer>

            </div>

            <hr />

            <h2 className="chart-title">
                Income vs Expenses (Bar Chart)
            </h2>

           <div className="chart-container">

              <ResponsiveContainer width="100%" height={350}>

    <BarChart data={data}>

        <CartesianGrid strokeDasharray="3 3" />

        <XAxis dataKey="name" />

        <YAxis />

        <Tooltip />

        <Legend />

        <Bar
            dataKey="value"
            fill="#8884d8"
        />

    </BarChart>

</ResponsiveContainer>

            </div>

            <hr />

            <h2 className="chart-title">
                AI Financial Insight
            </h2>

            <div className="info-box insight">

                <p className="info-text insight-text">
                    💡 {summary.insight || "No insight available"}
                </p>

            </div>

            <hr />

            <h2 className="chart-title">
                AI Recommendation
            </h2>

            <div className="info-box recommendation">

               <p className="info-text recommendation-text">
                    📌 {summary.recommendation || "No recommendation available"}
                </p>

            </div>


            <hr />
    
<h2 className="chart-title">
    Expense Categories
</h2>

 <div className="chart-container">

    {
             (

            <ResponsiveContainer
                width="100%"
                height={300}
            >

                <PieChart>

                    <Pie
                        data={categoryData}
                        cx="50%"
                        cy="50%"
                        outerRadius={120}
                        dataKey="total"
                        nameKey="category"
                        label
                    >

                        {categoryData.map((entry, index) => (

                            <Cell
                                key={`category-cell-${index}`}
                                fill={COLORS[index % COLORS.length]}
                            />

                        ))}

                    </Pie>

                    <Tooltip />
                    <Legend />

                </PieChart>

            </ResponsiveContainer>

        )
    }

</div>

<hr />

<h2 className="chart-title">
    Expense Categories (Bar Chart)
</h2>

<div className="chart-container">

    <ResponsiveContainer width="100%" height={350}>

    <BarChart data={categoryData}>

        <CartesianGrid strokeDasharray="3 3" />

        <XAxis dataKey="category" />

        <YAxis />

        <Tooltip />

        <Legend />

        <Bar
            dataKey="total"
            fill="#82ca9d"
        />

    </BarChart>

</ResponsiveContainer>

</div>

<hr />

<h2 className="chart-title">
    Monthly Income vs Expenses
</h2>

<div
    style={{
        width: "100%",
        height: 400
    }}
>

    <ResponsiveContainer width="100%" height="100%">

        <LineChart data={monthlyData}>

            <CartesianGrid strokeDasharray="3 3" />

            <XAxis dataKey="month" />

            <YAxis />

            <Tooltip />

            <Legend />

            <Line
                type="monotone"
                dataKey="income"
                stroke="#4CAF50"
                strokeWidth={3}
            />

            <Line
                type="monotone"
                dataKey="expenses"
                stroke="#F44336"
                strokeWidth={3}
            />

        </LineChart>

    </ResponsiveContainer>

</div>
<AIChatWidget />
<Footer />

        </div>

    );

}

export default Dashboard;