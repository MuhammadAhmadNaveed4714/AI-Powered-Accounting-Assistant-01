import { useState, useEffect } from "react";
import API from "../services/api";
import Navbar from "../components/Navbar";
import { CSVLink } from "react-csv";
import { toast } from "react-toastify";
import "../styles/forms.css";
import Footer from "../components/Footer";
import "../styles/expenses.css";
function Expenses() {

    const [expenseName, setExpenseName] = useState("");
    const [category, setCategory] = useState("Food");
    const [amount, setAmount] = useState("");
    const [expenseDate, setExpenseDate] = useState("");
    const [notes, setNotes] = useState("");

    const [expenses, setExpenses] = useState([]);
    const [editingExpenseId, setEditingExpenseId] = useState(null);
    const [searchTerm, setSearchTerm] = useState("");

    const fetchExpenses = async () => {

        try {

            const token = localStorage.getItem("token");

            const response = await API.get(
                "/expenses",
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            setExpenses(response.data);

        } catch (error) {

            console.log(error);

        }

    };

    useEffect(() => {

    document.title = "Expenses | AI Accounting Assistant";

    fetchExpenses();

}, []);

    const handleSubmit = async (e) => {

        e.preventDefault();

        if (editingExpenseId !== null) {

            updateExpense();
            return;

        }

        try {

            const token = localStorage.getItem("token");

            await API.post(
                "/expenses",
                {
                    expense_name: expenseName,
                    category: category,
                    amount: amount,
                    expense_date: expenseDate,
                    notes: notes
                },
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            fetchExpenses();

            toast.success("Expense saved successfully!");

            setExpenseName("");
            setCategory("Food");
            setAmount("");
            setExpenseDate("");
            setNotes("");

        } catch (error) {

           toast.error(
    error.response?.data?.message ||
    "Failed to add expense."
);

        }

    };


    // Delete Expense
    const deleteExpense = async (expenseId) => {

        try {

            const token = localStorage.getItem("token");

            await API.delete(
                `/expenses/${expenseId}`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            fetchExpenses();

            toast.success("Expense deleted successfully!");

        } catch (error) {

           toast.error(
    error.response?.data?.message ||
    "Failed to delete expense."
);

        }

    };


    // Start Editing
    const startEditing = (expense) => {

        setEditingExpenseId(expense.expense_id);

        setExpenseName(expense.expense_name);
        setCategory(expense.category);
        setAmount(expense.amount);
        setExpenseDate(expense.expense_date);
        setNotes(expense.notes || "");

    };


    // Update Expense
    const updateExpense = async () => {

        try {

            const token = localStorage.getItem("token");

            await API.put(
                `/expenses/${editingExpenseId}`,
                {
                    expense_name: expenseName,
                    category: category,
                    amount: amount,
                    expense_date: expenseDate,
                    notes: notes
                },
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            fetchExpenses();

            toast.success("Expense updated successfully!");

            setEditingExpenseId(null);

            setExpenseName("");
            setCategory("Food");
            setAmount("");
            setExpenseDate("");
            setNotes("");

        } catch (error) {

           toast.error(
    error.response?.data?.message ||
    "Failed to update expense."
);

        }

    };


    // Search Expenses
    const filteredExpenses = expenses.filter((expense) =>
        expense.expense_name
            .toLowerCase()
            .includes(searchTerm.toLowerCase())
    );


    const csvData = [
    [
        "Expense Name",
        "Category",
        "Amount",
        "Date",
        "Notes"
    ],

    ...filteredExpenses.map((expense) => [
        expense.expense_name,
        expense.category,
        expense.amount,
        expense.expense_date,
        expense.notes
    ])
];



  return (

    <>

        <Navbar />

        <div>

            <h1>Expense Management</h1>

<div className="form-card">

    <form onSubmit={handleSubmit}>

        <div className="form-grid">

            <input
                type="text"
                placeholder="Expense Name"
                value={expenseName}
                onChange={(e) => setExpenseName(e.target.value)}
            />

            <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
            >
                <option>Food</option>
                <option>Transport</option>
                <option>Shopping</option>
                <option>Electronics</option>
                <option>Bills</option>
                <option>Other</option>
            </select>

            <input
                type="number"
                placeholder="Amount"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
            />

            <input
                type="date"
                value={expenseDate}
                onChange={(e) => setExpenseDate(e.target.value)}
            />

            <textarea
                placeholder="Notes"
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
            />

        </div>

        <button
            type="submit"
            className="submit-btn"
        >
            {editingExpenseId !== null
                ? "Update Expense"
                : "Add Expense"}
        </button>

    </form>

</div>

            <hr />

            <h2>Expense List</h2>



            <div
    style={{
        display: "flex",
        justifyContent: "flex-end",
        marginBottom: "15px"
    }}
>

    <CSVLink
        data={csvData}
        filename={"Expenses_Report.csv"}
        style={{
            backgroundColor: "#28a745",
            color: "white",
            padding: "10px 20px",
            textDecoration: "none",
            borderRadius: "5px",
            fontWeight: "bold"
        }}
    >
        📥 Download CSV
    </CSVLink>

</div>


            <div
                style={{
                    display: "flex",
                    gap: "10px",
                    alignItems: "center",
                    marginBottom: "20px"
                }}
            >

                <input
                    type="text"
                    placeholder="🔍 Search expense by name..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    style={{
                        padding: "10px",
                        width: "300px",
                        borderRadius: "5px",
                        border: "1px solid #ccc"
                    }}
                />

                <button
                    type="button"
                    onClick={() => setSearchTerm("")}
                    style={{
                        padding: "10px 15px",
                        cursor: "pointer"
                    }}
                >
                    Clear
                </button>

            </div>
            

  
             <div className="table-responsive">
            <table border="1" cellPadding="10">

                <thead>

                    <tr>
                        <th>Name</th>
                        <th>Category</th>
                        <th>Amount</th>
                        <th>Date</th>
                        <th>Notes</th>
                        <th>Action</th>
                    </tr>

                </thead>

                <tbody>

                    {filteredExpenses.length === 0 ? (

                        <tr>

                            <td colSpan="6">
                                No expenses found.
                            </td>

                        </tr>

                    ) : (

                        filteredExpenses.map((expense) => (

                            <tr key={expense.expense_id}>

                                <td>{expense.expense_name}</td>
                                <td>{expense.category}</td>
                                <td>{expense.amount}</td>
                                <td>{expense.expense_date}</td>
                                <td>{expense.notes}</td>

                                <td>

                                    <button
    type="button"
    className="edit-btn"
    onClick={() => startEditing(expense)}
>
    Edit
</button>

                                    {" "}

                                    <button className="delete-btn"
                                        type="button"
                                        onClick={() => {

                                            if (
                                                window.confirm(
                                                    "Are you sure you want to delete this expense?"
                                                )
                                            ) {

                                                deleteExpense(expense.expense_id);

                                            }

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
            </div>
<Footer />
        </div>

    </>

);

}

export default Expenses;