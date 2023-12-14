function HeaderElementLeft({href, text}) {
    return (
        <li className="flex items-center justify-center w-[30%]">
            <a className="max-w-[50%] w-[150px] flex gap-1 text-zinc-300
            hover:text-white hover:border-b-2 hover:border-b-white items-center transition duration-300 justify-center" 
            href={href}>
                <p>{text}</p>
            </a>
        </li>
    )
}

export default HeaderElementLeft;