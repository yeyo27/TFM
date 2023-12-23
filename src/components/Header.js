import HeaderElementRight from './HeaderElementRight';
import HeaderElementLeft from './HeaderElementLeft';
import HistoryIcon from '../icons/HistoryIcon.svg';
import MenuIcon from '../icons/MenuIcon.svg';
import SignInIcon from '../icons/SignInIcon.svg';
import UserIcon from '../icons/UserIcon.svg';
import { useAuth } from '../auth/AuthProvider';

function Header() {
    const auth = useAuth();

    const userEmail = "user@email.com";

    return (
    <nav className="w-[100%] h-[100%] flex flex-row justify-between">
        <div className="p-2 w-[70%] h-[100%]">
            <ul className="flex flex-row justify-start h-[100%] w-[100%]">
                <HeaderElementLeft href="/url" text="From URL"/>
                <HeaderElementLeft href="/pdf" text="From PDF"/>
            </ul>
        </div>
        <div className="p-2 h-[100%]">
            <ul className="flex flex-row justify-between h-[100%] w-[100%] gap-8 p-6">
                <HeaderElementRight href="/history" icon={HistoryIcon} text="History"/>

                <HeaderElementRight href="/" icon={MenuIcon} text="Menu"/>

                {auth.isAuthenticated ? <HeaderElementRight href="/history" icon={UserIcon} text={userEmail}/> :
                    <HeaderElementRight href="/login" icon={SignInIcon} text="Sign In"/>}
            </ul>
        </div>
    </nav>
    );
}

export default Header;