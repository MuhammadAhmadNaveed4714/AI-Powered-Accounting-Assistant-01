import { useState, useEffect } from "react";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import axios from "axios";

function Documents() {

    const [documentType, setDocumentType] = useState("Receipt");
    const [selectedFile, setSelectedFile] = useState(null);

    const [documents, setDocuments] = useState([]);
    const [receipts, setReceipts] = useState([]);
    const [bills, setBills] = useState([]);

    const [activeSection, setActiveSection] = useState("documents");


    // =====================================================
    // Upload Document
    // =====================================================

    const handleUpload = async () => {

        if (!selectedFile) {
            alert("Please select a file.");
            return;
        }

        const token = localStorage.getItem("token");

        const formData = new FormData();

        formData.append("file", selectedFile);
        formData.append("document_type", documentType);

        try {

            const response = await axios.post(
                "/documents/upload",
                formData,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                        
                    }
                }
            );

            alert(response.data.message);

            setSelectedFile(null);

            fetchDocuments();
            fetchReceipts();
            fetchBills();

        } catch (error) {

            console.log(error);

            alert(
                error.response?.data?.message ||
                "Upload failed."
            );

        }

    };


    // =====================================================
    // Fetch Documents
    // =====================================================

    const fetchDocuments = async () => {

        try {

            const token = localStorage.getItem("token");

            const response = await axios.get(
                "/documents",
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            setDocuments(
                Array.isArray(response.data)
                    ? response.data
                    : []
            );

        } catch (error) {

            console.log(error);

        }

    };


    // =====================================================
    // Fetch Receipts
    // =====================================================

    const fetchReceipts = async () => {

        try {

            const token = localStorage.getItem("token");

            const response = await axios.get(
                "/receipts",
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            setReceipts(
                Array.isArray(response.data)
                    ? response.data
                    : []
            );

        } catch (error) {

            console.log(error);

        }

    };


    // =====================================================
    // Fetch Bills
    // =====================================================

    const fetchBills = async () => {

        try {

            const token = localStorage.getItem("token");

            const response = await axios.get(
                "/bills",
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            setBills(
                Array.isArray(response.data)
                    ? response.data
                    : []
            );

        } catch (error) {

            console.log(error);

        }

    };


    // =====================================================
    // Initial Load
    // =====================================================

    useEffect(() => {

        fetchDocuments();
        fetchReceipts();
        fetchBills();

    }, []);


    // =====================================================
    // Button Style
    // =====================================================

    const menuButtonStyle = (active) => ({

        padding: "10px 18px",

        marginRight: "10px",

        border: "none",

        borderRadius: "5px",

        cursor: "pointer",

        backgroundColor: active
            ? "#1976D2"
            : "#e0e0e0",

        color: active
            ? "white"
            : "black",

        fontWeight: active
            ? "bold"
            : "normal"

    });


    return (

        <>

            <Navbar />

            <div
                style={{
                    maxWidth: "1100px",
                    margin: "40px auto",
                    padding: "25px"
                }}
            >

                <h1>📂 Financial Documents</h1>

                <p>
                    Upload and manage your financial documents securely.
                </p>


                {/* =================================================
                    SECTION BUTTONS
                ================================================= */}

                <div
                    style={{
                        marginTop: "25px",
                        marginBottom: "25px"
                    }}
                >

                    <button
                        style={menuButtonStyle(
                            activeSection === "documents"
                        )}
                        onClick={() => setActiveSection("documents")}
                    >
                        📄 Documents
                    </button>


                    <button
                        style={menuButtonStyle(
                            activeSection === "receipts"
                        )}
                        onClick={() => setActiveSection("receipts")}
                    >
                        🧾 Receipts
                    </button>


                    <button
                        style={menuButtonStyle(
                            activeSection === "bills"
                        )}
                        onClick={() => setActiveSection("bills")}
                    >
                        📄 Bills
                    </button>

                </div>


                {/* =================================================
                    UPLOAD SECTION
                ================================================= */}

                {activeSection === "documents" && (

                    <>

                        <label>
                            Document Type
                        </label>


                        <select
                            value={documentType}
                            onChange={(e) =>
                                setDocumentType(e.target.value)
                            }
                            style={{
                                width: "100%",
                                padding: "10px",
                                marginTop: "10px",
                                marginBottom: "20px"
                            }}
                        >

                            <option value="Receipt">
                                Receipt
                            </option>

                            <option value="Bill">
                                Bill
                            </option>

                        </select>


                        <input
                            type="file"
                            accept=".pdf,.jpg,.jpeg,.png"
                            onChange={(e) =>
                                setSelectedFile(
                                    e.target.files[0]
                                )
                            }
                        />


                        <br />
                        <br />


                        <button onClick={handleUpload}>
                            Upload Document
                        </button>

                    </>

                )}


                <hr
                    style={{
                        margin: "30px 0"
                    }}
                />


                {/* =================================================
                    DOCUMENTS
                ================================================= */}

                {activeSection === "documents" && (

                    <>

                        <h2>
                            Uploaded Documents
                        </h2>


                        {documents.length === 0 ? (

                            <p>
                                No documents uploaded yet.
                            </p>

                        ) : (

                            <table
                                style={{
                                    width: "100%",
                                    borderCollapse: "collapse",
                                    marginTop: "20px"
                                }}
                            >

                                <thead>

                                    <tr
                                        style={{
                                            backgroundColor: "#1976D2",
                                            color: "white"
                                        }}
                                    >

                                        <th style={{ padding: "10px" }}>
                                            ID
                                        </th>

                                        <th style={{ padding: "10px" }}>
                                            Type
                                        </th>

                                        <th style={{ padding: "10px" }}>
                                            File Name
                                        </th>

                                        <th style={{ padding: "10px" }}>
                                            Upload Date
                                        </th>

                                        <th style={{ padding: "10px" }}>
                                            Actions
                                        </th>

                                    </tr>

                                </thead>


                                <tbody>

                                    {documents.map((doc) => (

                                        <tr key={doc.document_id}>

                                            <td style={{ padding: "10px" }}>
                                                {doc.document_id}
                                            </td>

                                            <td style={{ padding: "10px" }}>
                                                {doc.document_type}
                                            </td>

                                            <td style={{ padding: "10px" }}>
                                                {doc.file_name}
                                            </td>

                                            <td style={{ padding: "10px" }}>
                                                {doc.upload_date}
                                            </td>

                                            <td style={{ padding: "10px" }}>

                                                <button
                                                    onClick={() =>
                                                        window.open(
                                                            `/uploads/${doc.file_name}`,
                                                            "_blank"
                                                        )
                                                    }
                                                >
                                                    👁 View
                                                </button>

                                            </td>

                                        </tr>

                                    ))}

                                </tbody>

                            </table>

                        )}

                    </>

                )}


                {/* =================================================
                    RECEIPTS
                ================================================= */}

                {activeSection === "receipts" && (

                    <>

                        <h2>
                            🧾 Receipts
                        </h2>


                        {receipts.length === 0 ? (

                            <p>
                                No receipts found.
                            </p>

                        ) : (

                            <table
                                style={{
                                    width: "100%",
                                    borderCollapse: "collapse",
                                    marginTop: "20px"
                                }}
                            >

                                <thead>

                                    <tr
                                        style={{
                                            backgroundColor: "#1976D2",
                                            color: "white"
                                        }}
                                    >

                                        <th style={{ padding: "10px" }}>
                                            ID
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
                                            Date
                                        </th>

                                    </tr>

                                </thead>


                                <tbody>

                                    {receipts.map((receipt) => (

                                        <tr key={receipt.receipt_id}>

                                            <td style={{ padding: "10px" }}>
                                                {receipt.receipt_id}
                                            </td>

                                            <td style={{ padding: "10px" }}>
                                                {receipt.amount}
                                            </td>

                                            <td style={{ padding: "10px" }}>
                                                {receipt.receiver}
                                            </td>

                                            <td style={{ padding: "10px" }}>
                                                {receipt.sender}
                                            </td>

                                            <td style={{ padding: "10px" }}>
                                                {receipt.transaction_id}
                                            </td>

                                            <td style={{ padding: "10px" }}>
                                                {receipt.transaction_date}
                                            </td>

                                        </tr>

                                    ))}

                                </tbody>

                            </table>

                        )}

                    </>

                )}


                {/* =================================================
                    BILLS
                ================================================= */}

                {activeSection === "bills" && (

                    <>

                        <h2>
                            📄 Bills
                        </h2>


                        {bills.length === 0 ? (

                            <p>
                                No bills found.
                            </p>

                        ) : (

                            <table
                                style={{
                                    width: "100%",
                                    borderCollapse: "collapse",
                                    marginTop: "20px"
                                }}
                            >

                                <thead>

                                    <tr
                                        style={{
                                            backgroundColor: "#1976D2",
                                            color: "white"
                                        }}
                                    >

                                        <th style={{ padding: "10px" }}>
                                            ID
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

                                    {bills.map((bill) => (

                                        <tr key={bill.bill_id}>

                                            <td style={{ padding: "10px" }}>
                                                {bill.bill_id}
                                            </td>

                                            <td style={{ padding: "10px" }}>
                                                {bill.name}
                                            </td>

                                            <td style={{ padding: "10px" }}>
                                                {bill.issue_date}
                                            </td>

                                            <td style={{ padding: "10px" }}>
                                                {bill.bill_month}
                                            </td>

                                            <td style={{ padding: "10px" }}>
                                                {bill.due_date}
                                            </td>

                                            <td style={{ padding: "10px" }}>
                                                {bill.reference_no}
                                            </td>

                                            <td style={{ padding: "10px" }}>
                                                {bill.payable_within_due_date}
                                            </td>

                                            <td style={{ padding: "10px" }}>
                                                {bill.payable_after_due_date}
                                            </td>

                                        </tr>

                                    ))}

                                </tbody>

                            </table>

                        )}

                    </>

                )}

            </div>

            <Footer />

        </>

    );

}

export default Documents;
