import { useState, useEffect } from "react";
import API from "../services/api";
import Navbar from "../components/Navbar";
import { toast } from "react-toastify";
import "../styles/forms.css";
import Footer from "../components/Footer";
import "../styles/income.css";
import { CSVLink } from "react-csv";
function Income() {

    const [incomeSource, setIncomeSource] = useState("");
    const [amount, setAmount] = useState("");
    const [incomeDate, setIncomeDate] = useState("");
    const [notes, setNotes] = useState("");

    const [incomes, setIncomes] = useState([]);
    const [editingIncomeId, setEditingIncomeId] = useState(null);
    const [searchTerm, setSearchTerm] = useState("");
    const fetchIncome = async () => {

        try {

            const token = localStorage.getItem("token");

            const response = await API.get(
                "/income",
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            setIncomes(response.data);

        } catch (error) {

            console.log(error);

        }

    };

    useEffect(() => {

    fetchIncome();

}, []);

const handleSubmit = async (e) => {

    e.preventDefault();

    if (editingIncomeId !== null) {

        updateIncome();
        return;

    }

    try {

        const token = localStorage.getItem("token");

        await API.post(
            "/income",
            {
                income_source: incomeSource,
                amount: amount,
                income_date: incomeDate,
                notes: notes
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        fetchIncome();

        toast.success("Income saved successfully!");

        setIncomeSource("");
        setAmount("");
        setIncomeDate("");
        setNotes("");

    } catch (error) {

        toast.error(
    error.response?.data?.message ||
    "Failed to add income."
);

    }

};


// Delete Income
const deleteIncome = async (incomeId) => {

    try {

        const token = localStorage.getItem("token");

        await API.delete(
            `/income/${incomeId}`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        fetchIncome();

        toast.success("Income deleted successfully!");

    } catch (error) {

toast.error(
    error.response?.data?.message ||
    "Failed to delete income."
);

    }

};


// Start Editing
const startEditing = (income) => {

    setEditingIncomeId(income.income_id);

    setIncomeSource(income.income_source);
    setAmount(income.amount);
    setIncomeDate(income.income_date);
    setNotes(income.notes || "");

};


// Update Income
const updateIncome = async () => {

    try {

        const token = localStorage.getItem("token");

        await API.put(
            `/income/${editingIncomeId}`,
            {
                income_source: incomeSource,
                amount: amount,
                income_date: incomeDate,
                notes: notes
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        fetchIncome();

        toast.success("Income updated successfully!");

        setEditingIncomeId(null);
        setIncomeSource("");
        setAmount("");
        setIncomeDate("");
        setNotes("");

    } catch (error) {

        toast.error(
    error.response?.data?.message ||
    "Failed to update income."
);

    }

};


// Search Income
const filteredIncome = incomes.filter((income) =>
    income.income_source
        .toLowerCase()
        .includes(searchTerm.toLowerCase())
);

// Download CSV Data

const csvData = filteredIncome.map((income) => ({

    Source: income.income_source,

    Amount: income.amount,

    Date: income.income_date,

    Notes: income.notes

}));

 return (

    <>

        <Navbar />

        <div className="income-page">

            <h1 className="income-title">
                Income Management
            </h1>


            <div className="income-form">

                <form onSubmit={handleSubmit}>

                    <div className="form-grid">

                        <input
                            type="text"
                            placeholder="Income Source"
                            value={incomeSource}
                            onChange={(e) => setIncomeSource(e.target.value)}
                        />


                        <input
                            type="number"
                            placeholder="Amount"
                            value={amount}
                            onChange={(e) => setAmount(e.target.value)}
                        />


                        <input
                            type="date"
                            value={incomeDate}
                            onChange={(e) => setIncomeDate(e.target.value)}
                        />


                        <textarea
                            placeholder="Notes"
                            value={notes}
                            onChange={(e) => setNotes(e.target.value)}
                        />


                    </div>


                    <button
                        type="submit"
                        className="save-btn"
                    >

                        {
                            editingIncomeId !== null
                                ? "Update Income"
                                : "Add Income"
                        }

                    </button>


                </form>

            </div>


            <hr />


            <h2>
                Income List
            </h2>


            <div className="search-box">
            

            <CSVLink
    data={csvData}
    filename="income_report.csv"
    style={{
        backgroundColor: "#4CAF50",
        color: "white",
        padding: "10px 15px",
        borderRadius: "6px",
        textDecoration: "none",
        fontWeight: "bold"
    }}
>
    📥 Download CSV
</CSVLink>




                <input
                    type="text"
                    placeholder="🔍 Search income by source..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />


                <button
                    type="button"
                    onClick={() => setSearchTerm("")}
                >

                    Clear

                </button>


            </div>



            <div className="table-responsive">


                <table className="income-table">


                    <thead>

                        <tr>

                            <th>
                                Source
                            </th>

                            <th>
                                Amount
                            </th>

                            <th>
                                Date
                            </th>

                            <th>
                                Notes
                            </th>

                            <th>
                                Actions
                            </th>


                        </tr>


                    </thead>



                    <tbody>


                        {
                            filteredIncome.length === 0 ? (

                                <tr>

                                    <td colSpan="5">

                                        No income found.

                                    </td>


                                </tr>


                            ) : (


                                filteredIncome.map((income) => (


                                    <tr key={income.income_id}>


                                        <td>
                                            {income.income_source}
                                        </td>


                                        <td>
                                            {income.amount}
                                        </td>


                                        <td>
                                            {income.income_date}
                                        </td>


                                        <td>
                                            {income.notes}
                                        </td>



                                        <td>


                                            <button
                                                type="button"
                                                className="edit-btn"
                                                onClick={() => startEditing(income)}
                                            >

                                                Edit

                                            </button>



                                            <button
                                                type="button"
                                                className="delete-btn"
                                                onClick={() => {

                                                    if (
                                                        window.confirm(
                                                            "Are you sure you want to delete this income?"
                                                        )
                                                    ) {

                                                        deleteIncome(
                                                            income.income_id
                                                        );

                                                    }

                                                }}
                                            >

                                                Delete

                                            </button>


                                        </td>


                                    </tr>


                                ))

                            )

                        }


                    </tbody>


                </table>


            </div>


            <Footer />


        </div>


    </>

);

}

export default Income;