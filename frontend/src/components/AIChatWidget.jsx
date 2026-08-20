import { useState } from "react";
import API from "../services/api";


function AIChatWidget() {

    const [isOpen, setIsOpen] = useState(false);

    const [message, setMessage] = useState("");

    const [loading, setLoading] = useState(false);

    const [messages, setMessages] = useState([
        {
            sender: "AI",
            text: "👋 Hello! I am your AI Financial Assistant. Ask me anything about your finances."
        }
    ]);


    const sendMessage = async () => {

        if (!message.trim() || loading) return;

        const currentMessage = message.trim();

        const userMessage = {
            sender: "You",
            text: currentMessage
        };

        setMessages((prev) => [
            ...prev,
            userMessage
        ]);

        setMessage("");
        setLoading(true);


        try {

            const token = localStorage.getItem("token");

            const response = await API.post(
                "/ai/chat",
                {
                    message: currentMessage
                },
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                        "Content-Type": "application/json"
                    }
                }
            );


            setMessages((prev) => [
                ...prev,
                {
                    sender: "AI",
                    text:
                        response.data.reply ||
                        "I could not generate a response."
                }
            ]);

        }
        catch (error) {

    console.log(
        "AI CHAT ERROR:",
        error.response?.data || error.message || error
    );

    let errorMessage = "❌ Unable to generate AI response.";

    if (error.response?.status === 401) {

        errorMessage =
            "🔐 Your session has expired. Please login again.";

    }
    else if (error.response?.data?.message) {

        errorMessage =
            `❌ ${error.response.data.message}`;

    }
    else if (error.response?.data?.error) {

        errorMessage =
            `❌ ${error.response.data.error}`;

    }

    setMessages((prev) => [
        ...prev,
        {
            sender: "AI",
            text: errorMessage
        }
    ]);

}
        finally {

            setLoading(false);

        }

    };


    return (

        <>

            {/* Chat Button */}

            <button
                onClick={() => setIsOpen(!isOpen)}
                style={{
                    position: "fixed",
                    bottom: "25px",
                    right: "25px",
                    width: "65px",
                    height: "65px",
                    borderRadius: "50%",
                    border: "none",
                    background: "#1976D2",
                    color: "white",
                    fontSize: "26px",
                    cursor: "pointer",
                    boxShadow:
                        "0 4px 10px rgba(0,0,0,0.3)",
                    zIndex: 9999
                }}
            >
                {isOpen ? "✕" : "💬"}
            </button>


            {/* Chat Window */}

            {isOpen && (

                <div
                    style={{
                        position: "fixed",
                        bottom: "100px",
                        right: "25px",
                        width: "350px",
                        height: "500px",
                        background: "#1E1E1E",
                        color: "white",
                        borderRadius: "12px",
                        display: "flex",
                        flexDirection: "column",
                        boxShadow:
                            "0 5px 20px rgba(0,0,0,0.4)",
                        zIndex: 9999,
                        overflow: "hidden"
                    }}
                >

                    {/* Header */}

                    <div
                        style={{
                            padding: "15px",
                            background: "#1976D2",
                            fontWeight: "bold",
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "space-between"
                        }}
                    >

                        <span>
                            🤖 AI Financial Assistant
                        </span>

                    </div>


                    {/* Messages */}

                    <div
                        style={{
                            flex: 1,
                            overflowY: "auto",
                            padding: "15px"
                        }}
                    >

                        {messages.map((msg, index) => (

                            <div
                                key={index}
                                style={{
                                    marginBottom: "15px",
                                    display: "flex",
                                    flexDirection: "column",
                                    alignItems:
                                        msg.sender === "You"
                                            ? "flex-end"
                                            : "flex-start"
                                }}
                            >

                                <div
                                    style={{
                                        fontSize: "12px",
                                        fontWeight: "bold",
                                        marginBottom: "5px",
                                        color:
                                            msg.sender === "You"
                                                ? "#90CAF9"
                                                : "#81C784"
                                    }}
                                >
                                    {msg.sender === "You"
                                        ? "You"
                                        : "🤖 AI Assistant"}
                                </div>


                                <div
                                    style={{
                                        background:
                                            msg.sender === "You"
                                                ? "#1976D2"
                                                : "#333333",
                                        padding: "10px 12px",
                                        borderRadius: "10px",
                                        maxWidth: "85%",
                                        lineHeight: "1.5",
                                        fontSize: "14px",
                                        whiteSpace: "pre-line",
                                        wordBreak: "break-word"
                                    }}
                                >
                                    <div
    style={{
        whiteSpace: "pre-wrap",
        lineHeight: "1.6",
        fontSize: "14px"
    }}
>
    {msg.text}
</div>
                                </div>

                            </div>

                        ))}


                        {loading && (

                            <div
                                style={{
                                    color: "#81C784",
                                    fontSize: "14px",
                                    padding: "10px"
                                }}
                            >
                                🤖 AI is thinking...
                            </div>

                        )}

                    </div>


                    {/* Input */}

                    <div
                        style={{
                            display: "flex",
                            padding: "10px",
                            gap: "8px",
                            borderTop:
                                "1px solid #444"
                        }}
                    >

                        <input
                            type="text"
                            placeholder="Ask your financial assistant..."
                            value={message}
                            disabled={loading}
                            onChange={(e) =>
                                setMessage(e.target.value)
                            }
                            onKeyDown={(e) => {

                                if (
                                    e.key === "Enter" &&
                                    !loading
                                ) {
                                    sendMessage();
                                }

                            }}
                            style={{
                                flex: 1,
                                padding: "10px",
                                borderRadius: "6px",
                                border: "none",
                                outline: "none"
                            }}
                        />


                        <button
                            onClick={sendMessage}
                            disabled={loading}
                            style={{
                                background:
                                    loading
                                        ? "#666"
                                        : "#1976D2",
                                color: "white",
                                border: "none",
                                padding: "10px 15px",
                                borderRadius: "6px",
                                cursor:
                                    loading
                                        ? "not-allowed"
                                        : "pointer",
                                fontWeight: "bold"
                            }}
                        >

                            {loading ? "..." : "Send"}

                        </button>

                    </div>

                </div>

            )}

        </>

    );

}

export default AIChatWidget;