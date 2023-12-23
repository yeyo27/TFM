export default function MainHistory() {
    const loadHistory = true;

    return (
        <div className="flex flex-col justify-start p-4 gap-4">
                <h1 className="text-left">These are your most recent queries:</h1>
                {loadHistory ?
                <ul className="flex flex-col text-left gap-4">
                    {fakeHistory.map((history) => (
                        <li key={history.id}>
                            <p>{history.date}</p>
                            <p>{history.sourceName}</p>
                            <p>{history.query}</p>
                            <p>{history.response}</p>
                        </li>
                    ))}
                </ul> : <div>Loading history...</div>
                }
        </div>
    )
}
    

const fakeHistory = [
    {
        id: 1,
        sourceName: "url1.com",
        date: "2022-01-01 12:00:00",
        query: "What is the weather like?",
        response:"The weather is sunny",
    },
    {
        id: 2,
        sourceName: "url2.com",
        date: "2031-01-01 12:00:00",
        query: "What is the weather like?",
        response:"The weather is nothing",
    },
    {
        id: 3,
        sourceName: "url3.com",
        date: "2022-01-01 12:00:00",
        query: "What is the sñkfñodfksd like?",
        response:"The weather is skejfoiw",
    },
    {
        id: 4,
        sourceName: "pdf1",
        date: "2022-01-01 12:00:00",
        query: "What is the weather like?",
        response:"The weather is sunny",
    },
    {
        id: 5,
        sourceName: "pdf3",
        date: "2022-01-01 12:00:00",
        query: "What is the weather like?",
        response:"The weather is sunny",
    }
]