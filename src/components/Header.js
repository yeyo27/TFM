import HeaderElementRight from './HeaderElementRight';
import HeaderElementLeft from './HeaderElementLeft';
import HistoryIcon from '../icons/HistoryIcon.svg';
import MenuIcon from '../icons/MenuIcon.svg';
import SignInIcon from '../icons/SignInIcon.svg';
import { useAuth } from '../auth/AuthProvider';

function Header() {
    const auth = useAuth();

    const signInText = auth.isAuthenticated ? "user@email.com": "Sign In";

    return (
    <nav className="w-[100%] h-[100%] flex flex-row gap-2 justify-between">
        <div className="p-2 w-[50%] h-[100%]">
            <ul className="flex flex-row justify-start h-[100%] w-[100%]">
                <HeaderElementLeft href="/url" text="From URL"/>
                <HeaderElementLeft href="/pdf" text="From PDF"/>
            </ul>
        </div>
        <div className="p-2 h-[100%]">
            <ul className="flex flex-row justify-end h-[100%] w-[100%] -space-x-2">
                <HeaderElementRight href="/" icon={HistoryIcon} text="History"/>

                <HeaderElementRight href="/" icon={MenuIcon} text="Menu"/>

                <HeaderElementRight href="/login" icon={SignInIcon} text={signInText}/>
            </ul>
        </div>
    </nav>
    );
}

export default Header;