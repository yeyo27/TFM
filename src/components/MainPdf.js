import { useState } from "react";
import SubmitButton from "./SubmitButton";
import LoadingIcon from "./LoadingIcon";
import { useNavigate } from "react-router-dom";
import {useAuth} from "../auth/AuthProvider";

function MainPdf() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();
    const auth = useAuth();

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
      };

    async function handleButtonClick() {
        setIsLoading(true);

        const formData = new FormData();

        try {
            if (!selectedFile) {
                throw new Error('No file selected');
            }

            formData.append('pdf', selectedFile);

            const response = await fetch(`${process.env.REACT_APP_API_URL}/pdf`, {
                headers: {
                    'Authorization': `Bearer ${auth.accessToken}`
                },
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const responseData = await response.json();
            // TODO verify that responseData.total_vectors > 0 before redirecting
            console.log('Response data:', responseData);
            const lastDotIndex = selectedFile.name.lastIndexOf(".");
            const fileName = selectedFile.name.slice(0, lastDotIndex);
            navigate(`/../query/${responseData.collection_id}/${encodeURIComponent(fileName)}`);

        } catch(error) {
            console.error('Error uploading file', error);
            setIsLoading(false);
            // TODO display error message
        }
      }
    

    return (
        <div className="p-2 flex flex-col justify-center items-center h-[100%]">
            <h1 className="text-5xl">Virtual Assistant</h1>
            <h2 className="text-base italic">powered by vector search</h2>
            <form className="p-10 w-[80%]">               
                <input className="w-[80%] rounded-l-md flex-1 bg-[#303133] border-1 py-1.5 pl-3 text-gray-300 placeholder:text-gray-400 focus:ring-0 sm:text-base sm:leading-6"
                type="file" onChange={handleFileChange} name="pdf" accept=".pdf"/>
                <SubmitButton handleButtonClick={handleButtonClick} />
            </form>
            {isLoading && <LoadingIcon />}
        </div>
    )
}

/*
<input type="text" name="username" id="username" autocomplete="username" class="block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6" placeholder="janesmith">
*/

export default MainPdf;