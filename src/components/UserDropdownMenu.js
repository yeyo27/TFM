import { useConfirmation } from '../confirmation/ConfirmationProvider';
import { useAuth } from '../auth/AuthProvider';

function UserDropdownMenu() {
    const auth = useAuth();
    const { openConfirmation } = useConfirmation();

    function handleClickSignOut() {
        localStorage.removeItem("token");
        window.location.reload();
        console.log("User logged out");
    }

    function handleClickDeleteAccount() {
        openConfirmation(handleDeleteAccount);
    }

    async function handleDeleteAccount() {
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/users/me`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${auth.accessToken}`
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            localStorage.removeItem("token");
            window.location.reload();

            const responseData = await response.json();
            console.log(responseData);

        } catch (error) {
            console.log(error);
        }
    }

    return (
        <div className="rounded-bl-lg z-10 bg-zinc-900 shadow-md transition-all duration-300 linear">
            <ul>
                <li onClick={handleClickSignOut} className="text-white hover:cursor-pointer hover:bg-zinc-800 transition-all duration-300 linear">Sign Out</li>
                <li onClick={handleClickDeleteAccount} className="text-white rounded-bl-lg hover:cursor-pointer hover:bg-zinc-800 transition-all duration-300 linear">Delete Account</li>
            </ul>
        </div>
    );
};

export default UserDropdownMenu;