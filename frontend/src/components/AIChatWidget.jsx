import { useState } from "react";
import axios from "axios";

const API = axios.create({
    baseURL: "http://127.0.0.1:5000"
});

function AIChatWidget() {

    const [isOpen, setIsOpen] = useState(false);

    const [message, setMessage] = useState("");

    const [messages, setMessages] = useState([
        {
            sender: "AI",
            text: "👋 Hello! I am your AI Financial Assistant."
        }
    ]);

    const sendMessage = async () => {

        if (!message.trim()) return;

        const userMessage = {
            sender: "You",
            text: message
        };

        setMessages((prev) => [...prev, userMessage]);

        try {

            const token = localStorage.getItem("token");

            const response = await API.post(
                "/ai/chat",
                {
                    message: message
                },
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            setMessages((prev) => [
                ...prev,
                {
                    sender: "AI",
                    text: response.data.reply
                }
            ]);

        } catch (error) {

            setMessages((prev) => [
                ...prev,
                {
                    sender: "AI",
                    text: "❌ Failed to contact AI."
                }
            ]);

        }

        setMessage("");

    };

    return (

        <>

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
                    boxShadow: "0 4px 10px rgba(0,0,0,0.3)",
                    zIndex: 9999
                }}
            >
                💬
            </button>

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
                        borderRadius: "10px",
                        display: "flex",
                        flexDirection: "column",
                        boxShadow: "0 5px 20px rgba(0,0,0,0.4)",
                        zIndex: 9999
                    }}
                >

                    <div
                        style={{
                            padding: "15px",
                            background: "#1976D2",
                            fontWeight: "bold"
                        }}
                    >
                        🤖 AI Financial Assistant
                    </div>

                    <div
                        style={{
                            flex: 1,
                            overflowY: "auto",
                            padding: "10px"
                        }}
                    >

                        {messages.map((msg, index) => (

                            <div
                                key={index}
                                style={{
                                    marginBottom: "12px"
                                }}
                            >
                                <strong>
                                    {msg.sender}:
                                </strong>

                                <br />

                                {msg.text}

                            </div>

                        ))}

                    </div>

                    <div
                        style={{
                            display: "flex",
                            padding: "10px",
                            gap: "8px"
                        }}
                    >

                        <input
                            type="text"
                            placeholder="Ask AI..."
                            value={message}
                            onChange={(e) =>
                                setMessage(e.target.value)
                            }
                            onKeyDown={(e) => {
                                if (e.key === "Enter") {
                                    sendMessage();
                                }
                            }}
                            style={{
                                flex: 1,
                                padding: "10px",
                                borderRadius: "5px",
                                border: "none"
                            }}
                        />

                        <button
                            onClick={sendMessage}
                            style={{
                                background: "#1976D2",
                                color: "white",
                                border: "none",
                                padding: "10px 15px",
                                borderRadius: "5px",
                                cursor: "pointer"
                            }}
                        >
                            Send
                        </button>

                    </div>

                </div>

            )}

        </>

    );

}

export default AIChatWidget;