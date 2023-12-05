import HeaderElement from './HeaderElement';
import HistoryIcon from '../icons/HistoryIcon.svg';
import MenuIcon from '../icons/MenuIcon.svg';
import SignInIcon from '../icons/SignInIcon.svg';

function Header() {
    return (
    <nav className="w-[100%] h-[50%] flex flex-col gap-2">
        <div className="p-2">
            <ul className="flex flex-row justify-end w-[100%] -space-x-2">
                <HeaderElement href="/" icon={HistoryIcon} text="History"/>

                <HeaderElement href="/" icon={MenuIcon} text="Menu"/>

                <HeaderElement href="/" icon={SignInIcon} text="Sign In"/>
            </ul>
        </div>
    </nav>
    );
}

export default Header;