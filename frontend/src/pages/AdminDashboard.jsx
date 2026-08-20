import { useState, useEffect } from "react";
import API from "../services/api";
import { toast } from "react-toastify";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import axios from "axios";
import AIChatWidget from "../components/AIChatWidget";
function AdminDashboard() {

    const user = JSON.parse(
        localStorage.getItem("user")
    );

    const [users, setUsers] = useState([]);
    const [expenses, setExpenses] = useState([]);
    const [income, setIncome] = useState([]);
    const [search, setSearch] = useState("");
    const [expenseSearch, setExpenseSearch] = useState("");
    const [incomeSearch, setIncomeSearch] = useState("");
    const [expenseDate, setExpenseDate] = useState("");
    const [incomeDate, setIncomeDate] = useState("");
    const [aiSummary, setAiSummary] = useState("");
    const [aiLoading, setAiLoading] = useState(false);
    const [receipts, setReceipts] = useState([]);
    const [bills, setBills] = useState([]);
    const [stats, setStats] = useState({
    total_users: 0,
    total_admins: 0,
    total_income: 0,
    total_expenses: 0
});
    const fetchUsers = async () => {

        try {

            const token = localStorage.getItem("token");

            const response = await API.get(
                "/admin/users",
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            setUsers(response.data.users);

        } catch (error) {

            console.log(error);

            toast.error(
                "Failed to load users."
            );

        }

    };

    const fetchExpenses = async () => {

    try {

        const token = localStorage.getItem("token");

        const response = await API.get(
            "/admin/expenses",
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        setExpenses(response.data.expenses);

    } catch (error) {

        console.log(error);

        toast.error(
            "Failed to load expenses."
        );

    }

};



const fetchIncome = async () => {

    try {

        const token = localStorage.getItem("token");

        const response = await API.get(
            "/admin/income",
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        setIncome(response.data.income);

    } catch (error) {

        console.log(error);

        toast.error("Failed to load income.");

    }

};

const fetchReceipts = async () => {

    try {

        const token = localStorage.getItem("token");

        const response = await API.get(
            "/admin/receipts",
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        setReceipts(
            Array.isArray(response.data.receipts)
                ? response.data.receipts
                : []
        );

    } catch (error) {

        console.log(error);

        toast.error(
            "Failed to load receipts."
        );

    }

};


const fetchBills = async () => {

    try {

        const token = localStorage.getItem("token");

        const response = await API.get(
            "/admin/bills",
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        setBills(
            Array.isArray(response.data.bills)
                ? response.data.bills
                : []
        );

    } catch (error) {

        console.log(error);

        toast.error(
            "Failed to load bills."
        );

    }

};



const fetchStats = async () => {

    try {

        const token = localStorage.getItem("token");

        const response = await API.get(
            "/admin/stats",
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        setStats(response.data);

    } catch (error) {

        console.log(error);

        toast.error("Failed to load statistics.");

    }

};



    useEffect(() => {

    fetchUsers();
    fetchExpenses();
    fetchIncome();
    fetchReceipts();
    fetchBills();
    fetchStats();

}, []);

    const handleDeleteUser = async (userId) => {

    const confirmDelete = window.confirm(
        "Are you sure you want to delete this user?"
    );

    if (!confirmDelete) {
        return;
    }

    try {

        const token = localStorage.getItem("token");

        await API.delete(
            `/admin/users/${userId}`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        toast.success("User deleted successfully.");

        fetchUsers();

    } catch (error) {

        console.log(error);

        toast.error(
            error.response?.data?.message ||
            "Failed to delete user."
        );

    }

};


const handleDeleteExpense = async (expenseId) => {

    const confirmDelete = window.confirm(
        "Are you sure you want to delete this expense?"
    );

    if (!confirmDelete) {
        return;
    }

    try {

        const token = localStorage.getItem("token");

        await API.delete(
            `/admin/expenses/${expenseId}`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        toast.success("Expense deleted successfully.");

        fetchExpenses();

    } catch (error) {

        console.log(error);

        toast.error(
            error.response?.data?.message ||
            "Failed to delete expense."
        );

    }

};



const handleDeleteIncome = async (incomeId) => {

    const confirmDelete = window.confirm(
        "Are you sure you want to delete this income?"
    );

    if (!confirmDelete) {
        return;
    }

    try {

        const token = localStorage.getItem("token");

        await API.delete(
            `/admin/income/${incomeId}`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        toast.success("Income deleted successfully.");

        fetchIncome();

    } catch (error) {

        console.log(error);

        toast.error(
            error.response?.data?.message ||
            "Failed to delete income."
        );

    }

};


const handleRoleChange = async (userId, newRole) => {

    try {

        const token = localStorage.getItem("token");

        await API.put(
            `/admin/users/${userId}/role`,
            {
                role: newRole
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        toast.success("User role updated successfully.");

        fetchUsers();

    } catch (error) {

        console.log(error);

        toast.error(
            error.response?.data?.message ||
            "Failed to update user role."
        );

    }

};

const filteredUsers = users.filter((u) => {

    const searchText = search.toLowerCase();

    return (
        u.username.toLowerCase().includes(searchText) ||
        u.email.toLowerCase().includes(searchText)
    );

});

const filteredExpenses = expenses.filter((expense) => {

    const matchesSearch =

        expense.username
            .toLowerCase()
            .includes(expenseSearch.toLowerCase())

        ||

        expense.expense_name
            .toLowerCase()
            .includes(expenseSearch.toLowerCase())

        ||

        expense.category
            .toLowerCase()
            .includes(expenseSearch.toLowerCase());

    const matchesDate =

        expenseDate === "" ||

        expense.expense_date === expenseDate;

    return matchesSearch && matchesDate;

});


const filteredIncome = income.filter((item) => {

    const matchesSearch =

        item.username
            .toLowerCase()
            .includes(incomeSearch.toLowerCase())

        ||

        item.source
            .toLowerCase()
            .includes(incomeSearch.toLowerCase());

    const matchesDate =

        incomeDate === "" ||

        item.income_date === incomeDate;

    return matchesSearch && matchesDate;

});

const generateAdminAI = async () => {

    try {

        setAiLoading(true);

        const token = localStorage.getItem("token");

        const response = await API.get(
            "/admin/ai-summary",
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        setAiSummary(
            response.data.ai_summary
        );

        toast.success(
            "AI Admin Summary generated successfully."
        );

    } catch (error) {

        console.log("AI Summary Error:", error);

        toast.error(
            error.response?.data?.message ||
            "Failed to generate AI summary."
        );

    } finally {

        setAiLoading(false);

    }

};


const downloadPDF = () => {

    const doc = new jsPDF();

    doc.setFontSize(18);

    doc.text(
        "AI Accounting Assistant - Admin Report",
        14,
        20
    );

    doc.setFontSize(12);

    doc.text(
        `Total Users: ${stats.total_users}`,
        14,
        35
    );

    doc.text(
        `Total Admins: ${stats.total_admins}`,
        14,
        43
    );

    doc.text(
        `Total Income: Rs. ${stats.total_income}`,
        14,
        51
    );

    doc.text(
        `Total Expenses: Rs. ${stats.total_expenses}`,
        14,
        59
    );

    autoTable(doc, {

        startY: 70,

        head: [[
            "ID",
            "Username",
            "Email",
            "Role"
        ]],

        body: users.map((u) => [

            u.user_id,
            u.username,
            u.email,
            u.role

        ])

        

    });

    autoTable(doc, {

    startY: doc.lastAutoTable.finalY + 15,

    head: [[
        "ID",
        "User",
        "Expense",
        "Category",
        "Amount",
        "Date"
    ]],

    body: expenses.map((expense) => [

        expense.expense_id,
        expense.username,
        expense.expense_name,
        expense.category,
        `Rs. ${expense.amount}`,
        expense.expense_date

    ])

});


    autoTable(doc, {

    startY: doc.lastAutoTable.finalY + 15,

    head: [[
        "ID",
        "User",
        "Source",
        "Amount",
        "Date"
    ]],

    body: income.map((item) => [

        item.income_id,
        item.username,
        item.source,
        `Rs. ${item.amount}`,
        item.income_date

    ])

});

    doc.save("Admin_Report.pdf");

};


    return (

       <div
    className="page-container"
    style={{
        background: "#f5f5f5",
        minHeight: "100vh",
        color: "#222"
    }}
>

            <Navbar />

            <h1
                style={{
                    textAlign: "center",
                    marginTop: "20px"
                }}
            >
                👨‍💼 Admin Dashboard
            </h1>

          <div
    style={{
        maxWidth: "900px",
        margin: "30px auto",
        padding: "25px",
        background: "#ffffff",
        borderRadius: "10px",
        boxShadow: "0 2px 10px rgba(0,0,0,0.1)"
    }}
>

                <h2>
                    Welcome to the Admin Dashboard
                </h2>

                 <div
    style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
        gap: "20px",
        marginTop: "20px",
        marginBottom: "20px"
    }}
>

    <div
        style={{
            background: "#1976D2",
            color: "white",
            padding: "20px",
            borderRadius: "10px",
            textAlign: "center"
        }}
    >
        <h3>👥 Total Users</h3>

        <h2>
            {stats.total_users}
        </h2>
    </div>

    <div
        style={{
            background: "#1B5E20",
            color: "white",
            padding: "20px",
            borderRadius: "10px",
            textAlign: "center"
        }}
    >
        <h3>👨‍💼 Total Admins</h3>

        <h2>
            {stats.total_admins}
        </h2>
    </div>

    <div
        style={{
            background: "#EF6C00",
            color: "white",
            padding: "20px",
            borderRadius: "10px",
            textAlign: "center"
        }}
    >
        <h3>💰 Total Income</h3>

        <h2>
            Rs. {stats.total_income}
        </h2>
    </div>

    <div
        style={{
            background: "#E53935",
            color: "white",
            padding: "20px",
            borderRadius: "10px",
            textAlign: "center"
        }}
    >
        <h3>💸 Total Expenses</h3>

        <h2>
            Rs. {stats.total_expenses}
        </h2>
    </div>

</div>

                <h3>
                    Admin Features
                </h3>
                
                <ul>
                    <li>👥 Manage Users</li>
                    <li>💰 View All Income</li>
                    <li>💸 View All Expenses</li>
                    <li>📊 View System Reports</li>
                    <li>⚙️ Manage Application</li>
                </ul>

                
                <button
    onClick={downloadPDF}
    style={{
       backgroundColor: "#2E7D32",
color: "white",
border: "none",
padding: "10px 18px",
borderRadius: "6px",
cursor: "pointer",
fontWeight: "bold"
    }}
>
    📄 Download PDF Report
</button>

<button

onClick={generateAdminAI}

style={{
    backgroundColor: "#6A1B9A",
color: "white",
border: "none",
padding: "10px 18px",
borderRadius: "6px",
cursor: "pointer",
fontWeight: "bold"
}}

>

{
 aiLoading
 ?
 "Generating AI..."
 :
 "🤖 Generate Admin AI Summary"
}

</button>




{
aiSummary &&

<div
style={{
    marginTop:"20px",
    padding:"20px",
    background:"#f4f4f4",
    borderRadius:"10px"
}}
>

<h2>
🤖 AI Admin Analysis
</h2>


<p>
{aiSummary}
</p>


</div>

}

                <hr />

<h3>
    Registered Users
</h3>

<table
    style={{
        width: "100%",
        borderCollapse: "collapse",
        marginTop: "20px",
        backgroundColor: "#ffffff",
color: "#222222",
border: "1px solid #ddd"
    }}
>

    <thead>

        <tr
    style={{
       backgroundColor: "#1976D2",
color: "#ffffff"
    }}
>

            <th style={{ padding: "10px" }}>
                ID
            </th>

            <th style={{ padding: "10px" }}>
                Username
            </th>

            <th style={{ padding: "10px" }}>
                Email
            </th>

            <th style={{ padding: "10px" }}>
                Role
            </th>

            <th style={{ padding: "10px" }}>
                Actions
            </th>

        </tr>

    </thead>

    <tbody>

        {filteredUsers.length === 0 ? (

            <tr>

                <td
                    colSpan="5"
                    style={{
                        textAlign: "center",
                        padding: "20px"
                    }}
                >
                    No users found.
                </td>

            </tr>

        ) : (

            filteredUsers.map((u) => (

                <tr key={u.user_id}>

                    <td style={{ padding: "10px",borderBottom: "1px solid #ddd" }}>
                        {u.user_id}
                    </td>

                    <td style={{ padding: "10px",borderBottom: "1px solid #ddd" }}>
                        {u.username}
                    </td>

                    <td style={{ padding: "10px",borderBottom: "1px solid #ddd" }}>
                        {u.email}
                    </td>

                    <td style={{ padding: "10px",borderBottom: "1px solid #ddd" }}>

    <select
    value={u.role}
    disabled={u.user_id === user?.user_id}
    onChange={(e) =>
        handleRoleChange(
            u.user_id,
            e.target.value
        )
    }
    style={{
        padding: "6px",
        borderRadius: "5px"
    }}
>

        <option value="user">
            User
        </option>

        <option value="admin">
            Admin
        </option>

    </select>

</td>
    
                   <td style={{ padding: "10px",borderBottom: "1px solid #ddd" }}>

    {u.user_id === user?.user_id ? (

        <span
            style={{
                color: "gray",
                fontWeight: "bold"
            }}
        >
            Current Admin
        </span>

    ) : u.role === "admin" ? (

        <span
            style={{
                color: "#1976D2",
                fontWeight: "bold"
            }}
        >
            Protected
        </span>

    ) : (

        <button
            onClick={() => handleDeleteUser(u.user_id)}
            style={{
                backgroundColor: "#d32f2f",
                transition: "0.3s",
                color: "white",
                border: "none",
                padding: "8px 12px",
                borderRadius: "5px",
                cursor: "pointer"
            }}
        >
            Delete
        </button>

    )}

</td>


                </tr>

            ))

        )}

    </tbody>

</table>


<hr />

<h3>
    All Expenses
</h3>

<div
    style={{
        marginTop: "15px",
        marginBottom: "15px"
    }}
>
    <input
        type="text"
        placeholder="🔍 Search by user, expense or category..."
        value={expenseSearch}
        onChange={(e) => setExpenseSearch(e.target.value)}
        style={{
            width: "100%",
            padding: "10px",
            borderRadius: "6px",
            border: "1px solid #ccc",
            backgroundColor: "#ffffff",
            color: "#222",
            fontSize: "16px",
            outline: "none"
        }}
    />

    <div
        style={{
            marginBottom: "15px",
            marginTop: "15px"
        }}
    >
        <input
            type="date"
            value={expenseDate}
            onChange={(e) => setExpenseDate(e.target.value)}
            style={{
                width: "100%",
                padding: "10px",
                borderRadius: "6px",
                border: "1px solid #ccc",
                backgroundColor: "#ffffff",
                color: "#222",
                fontSize: "16px",
                outline: "none"
            }}
        />
    </div>
</div>



<table
    style={{
        width: "100%",
        borderCollapse: "collapse",
        marginTop: "20px",
        backgroundColor: "#ffffff",
color: "#222222",
border: "1px solid #ddd"
    }}
>

    <thead>

       <tr
    style={{
      backgroundColor: "#1976D2",
color: "#ffffff"
    }}
>

            <th style={{ padding: "10px" }}>
                ID
            </th>

            <th style={{ padding: "10px" }}>
                User
            </th>

            <th style={{ padding: "10px" }}>
                Expense
            </th>

            <th style={{ padding: "10px" }}>
                Category
            </th>

            <th style={{ padding: "10px" }}>
                Amount
            </th>

            <th style={{ padding: "10px" }}>
                Date
            </th>

              <th style={{ padding: "10px" }}>
                Actions
            </th> 

        </tr>

    </thead>

    <tbody>

        {filteredExpenses.length === 0 ? (

            <tr>

                <td
                    colSpan="7"
                    style={{
                        textAlign: "center",
                        padding: "20px"
                    }}
                >
                    No expenses found.
                </td>

            </tr>

        ) : (

            filteredExpenses.map((expense) => (

                <tr key={expense.expense_id}>

                    <td style={{ padding: "10px",borderBottom: "1px solid #ddd" }}>
                        {expense.expense_id}
                    </td>

                    <td style={{ padding: "10px",borderBottom: "1px solid #ddd" }}>
                        {expense.username}
                    </td>

                    <td style={{ padding: "10px",borderBottom: "1px solid #ddd" }}>
                        {expense.expense_name}
                    </td>

                    <td style={{ padding: "10px",borderBottom: "1px solid #ddd" }}>
                        {expense.category}
                    </td>

                    <td style={{ padding: "10px",borderBottom: "1px solid #ddd" }}>
                        Rs. {expense.amount}
                    </td>

                    <td style={{ padding: "10px",borderBottom: "1px solid #ddd" }}>
                        {expense.expense_date}
                    </td>



                    <td>

    <button
        onClick={() => handleDeleteExpense(expense.expense_id)}
        style={{
            backgroundColor: "#d32f2f",
            transition: "0.3s",
            color: "white",
            border: "none",
            padding: "8px 12px",
            borderRadius: "5px",
            cursor: "pointer"
        }}
    >
        Delete
    </button>

</td>

                </tr>

            ))

        )}

    </tbody>

</table>


<hr />

<h3>
    All Income
</h3>


<input
    type="text"
    placeholder="🔍 Search by user or income source..."
    value={incomeSearch}
    onChange={(e) => setIncomeSearch(e.target.value)}
    style={{
        width: "100%",
        padding: "10px",
        borderRadius: "6px",
        border: "1px solid #ccc",
        backgroundColor: "#ffffff",
        color: "#222",
        fontSize: "16px",
        outline: "none"
    }}
/>

<div
    style={{
        marginBottom: "15px",
        marginTop: "15px"
    }}
>
    <input
        type="date"
        value={incomeDate}
        onChange={(e) => setIncomeDate(e.target.value)}
        style={{
            width: "100%",
            padding: "10px",
            borderRadius: "6px",
            border: "1px solid #ccc",
            backgroundColor: "#ffffff",
            color: "#222",
            fontSize: "16px",
            outline: "none"
        }}
    />
</div>

<table
    style={{
        width: "100%",
        borderCollapse: "collapse",
        marginTop: "20px",
        backgroundColor: "#ffffff",
color: "#222222",
border: "1px solid #ddd"
    }}
>

    <thead>

       <tr
    style={{
       backgroundColor: "#1976D2",
color: "#ffffff"
    }}
>

            <th style={{ padding: "10px" }}>
                ID
            </th>

            <th style={{ padding: "10px" }}>
                User
            </th>

            <th style={{ padding: "10px" }}>
                Source
            </th>

            <th style={{ padding: "10px" }}>
                Amount
            </th>

            <th style={{ padding: "10px" }}>
                Date
            </th>

            <th style={{ padding: "10px" }}>
                Actions
            </th>

        </tr>

    </thead>

    <tbody>

        {filteredIncome.length === 0 ? (

            <tr>

                <td
                    colSpan="6"
                    style={{
                        textAlign: "center",
                        padding: "20px",
                        color: "#cccccc"
                    }}
                >
                    No income found.
                </td>

            </tr>

        ) : (

            filteredIncome.map((item) => (

                <tr key={item.income_id}>

                    <td style={{ padding: "10px",borderBottom: "1px solid #ddd" }}>
                        {item.income_id}
                    </td>

                    <td style={{ padding: "10px" ,borderBottom: "1px solid #ddd"}}>
                        {item.username}
                    </td>

                    <td style={{ padding: "10px",borderBottom: "1px solid #ddd" }}>
                        {item.source}
                    </td>

                    <td style={{ padding: "10px",borderBottom: "1px solid #ddd" }}>
                        Rs. {item.amount}
                    </td>

                    <td style={{ padding: "10px",borderBottom: "1px solid #ddd" }}>
                        {item.income_date}
                    </td>

                    <td>

                        <button
                            onClick={() => handleDeleteIncome(item.income_id)}
                            style={{
                                backgroundColor: "#d32f2f",
                                transition: "0.3s",
                                color: "white",
                                border: "none",
                                padding: "8px 12px",
                                borderRadius: "5px",
                                cursor: "pointer"
                            }}
                        >
                            Delete
                        </button>

                    </td>

                </tr>

            ))

        )}

    </tbody>

</table>

<hr />

<h3>
    🧾 All Receipts
</h3>

<table
    style={{
        width: "100%",
        borderCollapse: "collapse",
        marginTop: "20px",
        backgroundColor: "#ffffff",
        color: "#222222",
        border: "1px solid #ddd"
    }}
>

    <thead>

        <tr
            style={{
                backgroundColor: "#1976D2",
                color: "#ffffff"
            }}
        >

            <th style={{ padding: "10px" }}>
                ID
            </th>

            <th style={{ padding: "10px" }}>
                User
            </th>

            <th style={{ padding: "10px" }}>
                Amount
            </th>

            <th style={{ padding: "10px" }}>
                Receiver
            </th>

            <th style={{ padding: "10px" }}>
                Sender
            </th>

            <th style={{ padding: "10px" }}>
                Transaction ID
            </th>

            <th style={{ padding: "10px" }}>
                Transaction Date
            </th>

        </tr>

    </thead>


    <tbody>

        {receipts.length === 0 ? (

            <tr>

                <td
                    colSpan="7"
                    style={{
                        textAlign: "center",
                        padding: "20px"
                    }}
                >
                    No receipts found.
                </td>

            </tr>

        ) : (

            receipts.map((receipt) => (

                <tr key={receipt.receipt_id}>

                    <td
                        style={{
                            padding: "10px",
                            borderBottom: "1px solid #ddd"
                        }}
                    >
                        {receipt.receipt_id}
                    </td>


                    <td
                        style={{
                            padding: "10px",
                            borderBottom: "1px solid #ddd"
                        }}
                    >
                        {receipt.username}
                    </td>


                    <td
                        style={{
                            padding: "10px",
                            borderBottom: "1px solid #ddd"
                        }}
                    >
                        Rs. {receipt.amount}
                    </td>


                    <td
                        style={{
                            padding: "10px",
                            borderBottom: "1px solid #ddd"
                        }}
                    >
                        {receipt.receiver}
                    </td>


                    <td
                        style={{
                            padding: "10px",
                            borderBottom: "1px solid #ddd"
                        }}
                    >
                        {receipt.sender}
                    </td>


                    <td
                        style={{
                            padding: "10px",
                            borderBottom: "1px solid #ddd"
                        }}
                    >
                        {receipt.transaction_id}
                    </td>


                    <td
                        style={{
                            padding: "10px",
                            borderBottom: "1px solid #ddd"
                        }}
                    >
                        {receipt.transaction_date}
                    </td>

                </tr>

            ))

        )}

    </tbody>

</table>

<hr />

<h3>
    🧾 All Bills
</h3>

<table
    style={{
        width: "100%",
        borderCollapse: "collapse",
        marginTop: "20px",
        backgroundColor: "#ffffff",
        color: "#222222",
        border: "1px solid #ddd"
    }}
>

    <thead>

        <tr
            style={{
                backgroundColor: "#1976D2",
                color: "#ffffff"
            }}
        >

            <th style={{ padding: "10px" }}>
                ID
            </th>

            <th style={{ padding: "10px" }}>
                User
            </th>

            <th style={{ padding: "10px" }}>
                Name
            </th>

            <th style={{ padding: "10px" }}>
                Issue Date
            </th>

            <th style={{ padding: "10px" }}>
                Bill Month
            </th>

            <th style={{ padding: "10px" }}>
                Due Date
            </th>

            <th style={{ padding: "10px" }}>
                Reference No
            </th>

            <th style={{ padding: "10px" }}>
                Payable Within Due Date
            </th>

            <th style={{ padding: "10px" }}>
                Payable After Due Date
            </th>

        </tr>

    </thead>


    <tbody>

        {bills.length === 0 ? (

            <tr>

                <td
                    colSpan="9"
                    style={{
                        textAlign: "center",
                        padding: "20px"
                    }}
                >
                    No bills found.
                </td>

            </tr>

        ) : (

            bills.map((bill) => (

                <tr key={bill.bill_id}>

                    <td
                        style={{
                            padding: "10px",
                            borderBottom: "1px solid #ddd"
                        }}
                    >
                        {bill.bill_id}
                    </td>


                    <td
                        style={{
                            padding: "10px",
                            borderBottom: "1px solid #ddd"
                        }}
                    >
                        {bill.username}
                    </td>


                    <td
                        style={{
                            padding: "10px",
                            borderBottom: "1px solid #ddd"
                        }}
                    >
                        {bill.name}
                    </td>


                    <td
                        style={{
                            padding: "10px",
                            borderBottom: "1px solid #ddd"
                        }}
                    >
                        {bill.issue_date}
                    </td>


                    <td
                        style={{
                            padding: "10px",
                            borderBottom: "1px solid #ddd"
                        }}
                    >
                        {bill.bill_month}
                    </td>


                    <td
                        style={{
                            padding: "10px",
                            borderBottom: "1px solid #ddd"
                        }}
                    >
                        {bill.due_date}
                    </td>


                    <td
                        style={{
                            padding: "10px",
                            borderBottom: "1px solid #ddd"
                        }}
                    >
                        {bill.reference_no}
                    </td>


                    <td
                        style={{
                            padding: "10px",
                            borderBottom: "1px solid #ddd"
                        }}
                    >
                        Rs. {bill.payable_within_due_date}
                    </td>


                    <td
                        style={{
                            padding: "10px",
                            borderBottom: "1px solid #ddd"
                        }}
                    >
                        Rs. {bill.payable_after_due_date}
                    </td>

                </tr>

            ))

        )}

    </tbody>

</table>




       <input
    type="text"
    placeholder="🔍 Search by user or income source..."
    value={incomeSearch}
    onChange={(e) => setIncomeSearch(e.target.value)}
    style={{
        width: "100%",
        padding: "10px",
        borderRadius: "6px",
        border: "1px solid #ccc",
        backgroundColor: "#ffffff",
        color: "#222",
        fontSize: "16px",
        outline: "none"
    }}
/>

<div
    style={{
        marginBottom: "15px",
        marginTop: "15px"
    }}
>
    <input
        type="date"
        value={incomeDate}
        onChange={(e) => setIncomeDate(e.target.value)}
        style={{
            width: "100%",
            padding: "10px",
            borderRadius: "6px",
            border: "1px solid #ccc",
            backgroundColor: "#ffffff",
            color: "#222",
            fontSize: "16px",
            outline: "none"
        }}
    />
</div>



            </div>
            <AIChatWidget /> 
            <Footer />

        </div>

    );

}

export default AdminDashboard;