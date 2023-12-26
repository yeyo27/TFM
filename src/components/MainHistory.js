import { useEffect, useState } from "react";
import { useAuth } from "../auth/AuthProvider";

export default function MainHistory() {
    const [history, setHistory] = useState();
    const auth = useAuth();

    useEffect(() => {
        async function getHistory () {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/history`, {
                "method": "GET",
                "headers": {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${auth.accessToken}`
                }
            });
    
            const responseData = await response.json(); // this is a list of json
            setHistory(responseData);
        }
        getHistory();
    }, [auth.accessToken]);

    return (
        <div className="flex flex-col justify-start p-4 gap-4">
                <h1 className="text-left">These are your most recent queries:</h1>
                <ul className="flex flex-col text-left gap-4">
                    {history?.map((history) => (
                        <div className="rounded-sm border-t-2 border-b-2 border-b-white">
                            <li className="flex flex-col gap-1" key={history.id}>
                            <p>{history.date}</p>
                            <p>{history.source_name}</p>
                            <p>{history.query}</p>
                            <ul className="list-disc list-inside">
                                {history.responses.map(response => <li key={response.id}>{response.payload.answer}</li>)}
                            </ul>
                        </li>
                        </div>
                        
                    ))}
                </ul>
        </div>
    )
}