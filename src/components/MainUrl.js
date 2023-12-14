import { useState } from "react";
import SubmitButton from "./SubmitButton";
import { useNavigate } from "react-router-dom";

function MainUrl() {
    const [textInput, setTextInput] = useState('');
    const navigate = useNavigate();

    async function handleButtonClick() {
        const apiUrl = "http://127.0.0.1:8080/api/v1/url";

        try {
            if (textInput === '') {
                throw new Error('No text input');
            }

            const url = new URL(textInput);

            const data = {
                'href': url.href,
                'origin': url.origin,
                'hostname': url.hostname,
                'pathname': url.pathname
            }


            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const responseData = await response.json();
            console.log('Response data:', responseData);
            navigate(`../query/${responseData.collection_id}/${encodeURIComponent(url.href)}`);

        } catch (error) {
            console.error('Error:', error.message);
            // TODO diplay error message
        }
    }
    

    return (
        <div className="p-2 flex flex-col justify-center items-center h-[100%]">
            <h1 className="text-5xl">Virtual Assistant</h1>
            <h2 className="text-base italic">powered by vector search</h2>
            <form className="p-10 w-[80%]">               
                <input className="w-[80%] rounded-l-md flex-1 bg-[#303133] border-1 py-1.5 pl-3 text-gray-300 placeholder:text-gray-400 focus:ring-0 sm:text-base sm:leading-6"
                type="text" onChange={(e) => setTextInput(e.target.value)}
                placeholder="https://example.com" />
                <SubmitButton handleButtonClick={handleButtonClick} />
            </form>
        </div>
    )
}

/*
<input type="text" name="username" id="username" autocomplete="username" class="block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6" placeholder="janesmith">
*/

export default MainUrl;