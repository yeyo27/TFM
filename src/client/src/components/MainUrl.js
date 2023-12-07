function MainUrl() {
    return (
        <div className="p-2 flex flex-col justify-center items-center h-[100%]">
            <h1 className="text-5xl">Virtual Assistant</h1>
            <h2 className="text-base italic">powered by vector search</h2>
            <form className="p-10 w-[80%]">               
                <input className="w-[80%] rounded-l-md flex-1 bg-[#303133] border-1 py-1.5 pl-3 text-gray-300 placeholder:text-gray-400 focus:ring-0 sm:text-base sm:leading-6" type="text" placeholder="https://example.com" />
                <input className="hover:cursor-pointer p-1 border-2 rounded-r-md border-white bg-[#303133]" type="submit" value="Submit" />
            </form>
        </div>
    )
}

/*
<input type="text" name="username" id="username" autocomplete="username" class="block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6" placeholder="janesmith">
*/

export default MainUrl;