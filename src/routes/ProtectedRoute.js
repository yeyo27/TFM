import { Outlet } from "react-router-dom";
import { useAuth } from "../auth/AuthProvider";

export default function ProtectedRoute() {
    const auth = useAuth();

    return auth.isAuthenticated ? <Outlet /> :
    <div className="text-xl p-4">
        Please, <a href="/login" className="text-blue-500">sign in </a>to gain access.
    </div>
}