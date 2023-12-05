function HeaderElement({href, icon, text}) {
    return (
        <li>
            <a className="max-w-[70%] w-[120px] flex gap-1 text-zinc-300
            hover:text-white items-center transition duration-300 justify-center" 
            href={href}>
                <img src={icon} alt="" className="w-[25%] "/>
                <p>{text}</p>
            </a>
        </li>
    )
}

export default HeaderElement;