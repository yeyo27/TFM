import { useState } from "react";
import SubmitButton from "./SubmitButton";
import LoadingIcon from "./LoadingIcon";
import { useNavigate } from "react-router-dom";

function MainPdf() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
      };

    async function handleButtonClick() {
        setLoading(true);

        const apiUrl = "http://127.0.0.1:8080/api/v1/pdf";

        const formData = new FormData();

        try {
            if (!selectedFile) {
                throw new Error('No file selected');
            }

            formData.append('pdf', selectedFile);

            const response = await fetch(apiUrl, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const responseData = await response.json();
            console.log('Response data:', responseData);
            navigate(`../query/${responseData.collection_id}/${encodeURIComponent(selectedFile.name)}`);

        } catch(error) {
            console.error('Error uploading file', error);
            setLoading(false);
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
            {loading && <LoadingIcon />}
        </div>
    )
}

/*
<input type="text" name="username" id="username" autocomplete="username" class="block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6" placeholder="janesmith">
*/

export default MainPdf;