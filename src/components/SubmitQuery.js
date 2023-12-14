import SearchIcon from "../icons/SearchIcon.svg"

function SubmitQuery({handleButtonClick}) {
    return (<input className="hover:cursor-pointer p-1 border-2 rounded-r-md border-white bg-[#303133]"
            type="image" onClick={handleButtonClick} id="submit" src={SearchIcon} alt="Search"/>)
}

export default SubmitQuery;