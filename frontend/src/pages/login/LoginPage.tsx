import { useState } from "react";

export default function LoginPage() {
    const [email, setEmail] = useState("");

    return (
        <div>
            <h2>Login</h2>
            <input
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />
            <button>Login</button>
        </div>
    );
}