import React, { useEffect, useState } from 'react'

const API_URL = (import.meta.env.API_URL as string) || 'http://localhost:8000'

const App: React.FC = () => {
    const [data, setData] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            const response = await fetch(API_URL);
            const result = await response.json();
            setData(result);
        };

        fetchData();
    }, []);

    return (
        <div>
            <h1>Tic Tac Toe</h1>
            {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
        </div>
    );
};

export default App;
