function SubmitButton({handleButtonClick}) {
    return (<input className="hover:cursor-pointer p-1 border-2 rounded-r-md border-white bg-[#303133]"
            type="button" onClick={handleButtonClick} id="submit" value="Submit"/>)
}

export default SubmitButton;