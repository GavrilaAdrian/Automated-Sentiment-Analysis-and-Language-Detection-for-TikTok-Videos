import React, { useState } from "react";
import { Landing } from "../sections/Landing";
import Action from "../sections/Action";
import { Results } from "../sections/Results";
import { ResultsData } from "../types";

const MainPage: React.FC = () => {
    const [results, setResults] = useState<ResultsData | null>(null);

    // Specify the type of the `data` parameter as ResultsData
    const handleFetchResults = (data: ResultsData) => {
        console.log("Fetched data in handleFetchResults:", data); // Debug log
        setResults(data);
    };

    return (
        <div className="flex flex-col">
            <Landing />
            <Action onFetchResults={handleFetchResults} />
            <Results data={results} />
        </div>
    );
};

export default MainPage;
