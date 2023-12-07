import HeaderElementRight from './HeaderElementRight';
import HeaderElementLeft from './HeaderElemenLeft';
import HistoryIcon from '../icons/HistoryIcon.svg';
import MenuIcon from '../icons/MenuIcon.svg';
import SignInIcon from '../icons/SignInIcon.svg';

function Header() {
    return (
    <nav className="w-[100%] h-[100%] flex flex-row gap-2 justify-between">
        <div className="p-2 w-[50%] h-[100%]">
            <ul className="flex flex-row justify-start h-[100%] w-[100%]">
                <HeaderElementLeft href="/" text="From URL"/>
                <HeaderElementLeft href="/" text="From File"/>
            </ul>
        </div>
        <div className="p-2 h-[100%]">
            <ul className="flex flex-row justify-end h-[100%] w-[100%] -space-x-2">
                <HeaderElementRight href="/" icon={HistoryIcon} text="History"/>

                <HeaderElementRight href="/" icon={MenuIcon} text="Menu"/>

                <HeaderElementRight href="/" icon={SignInIcon} text="Sign In"/>
            </ul>
        </div>
    </nav>
    );
}

export default Header;