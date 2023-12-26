import { useState } from "react";
import SubmitQuery from "./SubmitQuery";
import { useParams } from 'react-router-dom';
import {useAuth} from "../auth/AuthProvider";

function MainQuery() {
    const [textInput, setTextInput] = useState();
    const [responses, setResponses] = useState();

    const auth = useAuth();

    const { collectionId, sourceName } = useParams();
    async function handleButtonClick() {
        try {
            if (!textInput) {
                throw new Error('No text input');
            }
            const url = `${process.env.REACT_APP_API_URL}/query?collection_id=${encodeURIComponent(collectionId)}
            &query=${encodeURIComponent(textInput)}&source_name=${encodeURIComponent(sourceName)}`;
            
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${auth.accessToken}`
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const responseData = await response.json();
            setResponses(responseData.hits);
            console.log(sourceName);
            responseData.hits.forEach(hit => {
                console.log(hit.payload.answer);
            })

        } catch (error) {
            console.error('Error:', error.message);
        }
      }
    

    return (
        <div className="p-2 flex flex-col justify-center items-center h-[100%] gap-10">
            <div className="p-10">
                <h1 className="text-5xl">Virtual Assistant</h1>
                <h2 className="text-base italic">powered by vector search</h2>
            </div>
            <div className="w-[80%]">
                <p className="w-[100%] text-left p-1">Currently querying: {sourceName}</p> 
                <form className="w-[100%] flex" onSubmit={e => e.preventDefault()}>           
                    <textarea className="w-[80%] rounded-l-md flex-1 bg-[#303133] border-1 py-1.5 pl-3 text-gray-300 placeholder:text-gray-400 focus:ring-0 sm:text-base sm:leading-6"
                    onChange={(e) => setTextInput(e.target.value)}
                    placeholder="Ask anything about your source..." name="input_query"
                    autoComplete="off" spellCheck="false" autoCorrect="off" autoCapitalize="off"
                    />
                    <SubmitQuery handleButtonClick={handleButtonClick} />
                </form>
            </div>
            
            {responses 
                ? (
                <div className="flex flex-col gap-2">
                    <p className="text-left">These are the fragments of your source that best match your question:</p>
                    <ul className="flex flex-col gap-4">
                        {responses.map(response => <li key={response.id}>{response.payload.answer}</li>)}
                    </ul>
                </div>) 
                : <div></div>}
        </div>
    )
}

/*
<input type="text" name="username" id="username" autocomplete="username" class="block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6" placeholder="janesmith">
*/

export default MainQuery;