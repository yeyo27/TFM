import { useState } from "react";
import { useAuth } from "../auth/AuthProvider";
import { Navigate, useNavigate } from "react-router-dom";

const API_URL = "http://127.0.0.1:8080/api/v1/token";

function LogIn() {
    const [username, setUsername] = useState();
    const [password, setPassword] = useState();
    const [error, setError] = useState();

    const navigate = useNavigate();

    const auth = useAuth();

    async function handleSubmit(e) {
        e.preventDefault();

        if (!username || !password) {
            setError("Please fill in all fields");
            return;
        }

        const formData = new FormData();

        formData.append("username", username);
        formData.append("password", password);

        try {
            const response = await fetch(API_URL, {
                method: "POST",
                body: formData,
            });

            const responseData = await response.json();

            if (!response.ok) {
                setError(responseData.detail);
                throw new Error(`HTTP error!\n Status: ${response.status}\n details: ${responseData.detail}`);
            }

            console.log("User logged in");
            console.log('Response data:', responseData);

            navigate("/");

        } catch(error) {
            console.error(error.message);
        }
    }

    if (auth.isAuthenticated) {
        return <Navigate to="/" />;
    }

    return (
        <section className="bg-[#161718]">
            <div className="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
                <a href="/" className="flex items-center mb-6 text-2xl font-semibold text-gray-900 dark:text-white">
                    <h1>Virtual Assistant</h1>  
                </a>
                <div className="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700">
                    <div className="p-6 space-y-4 md:space-y-6 sm:p-8">
                        <h1 className="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
                            Sign in to your account
                        </h1>
                        {error && <p id="error" className="text-red-500 font-light">{error}</p>}
                        <form className="space-y-4 md:space-y-6" onSubmit={handleSubmit}>
                            <div>
                                <label htmlFor="username" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Your username</label>
                                <input type="username" name="username" id="username" onChange={(e) => setUsername(e.target.value)} className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="johndoe123" required="" />
                            </div>
                            <div>
                                <label htmlFor="password" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Password</label>
                                <input type="password" name="password" id="password" placeholder="••••••••"  onChange={(e) => setPassword(e.target.value)} className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" required="" />
                            </div>
                            <div className="flex items-center justify-between">
                                <div className="flex items-start">
                                    <div className="flex items-center h-5">
                                        <input id="remember" aria-describedby="remember" type="checkbox" className="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-primary-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-primary-600 dark:ring-offset-gray-800" required="" />
                                    </div>
                                    <div className="ml-3 text-sm">
                                        <label htmlFor="remember" className="text-gray-500 dark:text-gray-300">Remember me</label>
                                    </div>
                                </div>
                                <a href="/" className="text-sm font-medium text-primary-600 hover:underline text-blue-500">Forgot password?</a>
                            </div>
                            <button type="submit" className="w-full text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center">Sign in</button>
                            <p className="text-sm font-light text-gray-500 dark:text-gray-400">
                                Don't have an account yet? <a href="/signup" className="font-medium text-primary-600 hover:underline text-blue-500">Sign up</a>
                            </p>
                        </form>
                    </div>
                </div>
            </div>
            </section>
    )
}

export default LogIn;