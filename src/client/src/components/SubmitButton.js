function SubmitButton({handleButtonClick}) {
    return (<input className="Submit hover:cursor-pointer p-1 border-2 rounded-r-md border-white bg-[#303133]"
            type="button" onClick={handleButtonClick} value="Submit"/>)
}

export default SubmitButton;