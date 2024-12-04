import React, { useState } from "react";
import { ResultsData } from "../types";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

interface ActionProps {
    onFetchResults: (data: ResultsData) => void; // Callback to update results in the parent
}

const Action: React.FC<ActionProps> = ({ onFetchResults }) => {
    const [videoCount, setVideoCount] = useState<number>(1);
    const [loadingAnalysis, setLoadingAnalysis] = useState<boolean>(false);
    const [loadingDisplay, setLoadingDisplay] = useState<boolean>(false);

    const handleProcess = async () => {
        setLoadingAnalysis(true);
        console.log("Starting video analysis with count:", videoCount); // Debugging print
        try {
            const response = await fetch("http://127.0.0.1:5000/process", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ count: videoCount }),
            });
    
            console.log("Process response status:", response.status); // Debugging print
    
            const responseBody = await response.text(); // Read the response body as text
            console.log("Process response body:", responseBody); // Debugging print
    
            if (response.ok) {
                console.log("Process request succeeded. Fetching processed videos..."); // Debugging print
                const processedResponse = await fetch("http://127.0.0.1:5000/videos"); // Fetch processed videos
                const data: ResultsData = await processedResponse.json();
                console.log("Fetched processed videos:", data); // Debugging print
                onFetchResults(data); // Update results in the parent component
                alert("Analysis complete!")
            } else {
                console.error("Process request failed. Status:", response.status); // Debugging print
                alert(`Failed to process videos. Status: ${response.status}, Message: ${responseBody}`);
            }
        } catch (error) {
            console.error("Error during video analysis:", error); // Debugging print
            alert("An error occurred. Please try again.");
        } finally {
            setLoadingAnalysis(false);
            console.log("Video analysis process completed."); // Debugging print
        }
    };
    
    const handleDisplay = async () => {
        setLoadingDisplay(true);
        console.log("Fetching existing videos..."); // Debugging print
        try {
            const response = await fetch("http://127.0.0.1:5000/videos");
            console.log("Display response status:", response.status); // Debugging print
            const data: ResultsData = await response.json();
            console.log("Fetched video data:", data); // Debugging print

            if (response.ok) {
                onFetchResults(data); // Pass data to Results component
                console.log("Passed fetched videos to Results component."); // Debugging print

                // Add scroll animation after a short delay
                setTimeout(() => {
                    console.log("Scrolling to results section..."); // Debugging print
                    document.getElementById("results-section")?.scrollIntoView({ behavior: "smooth" });
                }, 500); // 0.5-second delay
            } else {
                console.error("Error fetching videos. Status:", response.status); // Debugging print
                alert("Failed to fetch videos. Please check the backend.");
            }
        } catch (error) {
            console.error("Error fetching videos:", error); // Debugging print
            alert("An error occurred. Please try again.");
        } finally {
            setLoadingDisplay(false);
            console.log("Display videos process completed."); // Debugging print
        }
    };

    return (
        <div id="action-section" className="h-screen flex items-center justify-between bg-gray-100 px-16">
            {/* Left Side: Start Analysis */}
            <div className="flex flex-col items-center space-y-4 w-1/3">
                <Label htmlFor="videoCount" className="text-lg text-gray-600">
                    Number of Videos (1-100):
                </Label>
                <Input
                    id="videoCount"
                    type="number"
                    min="1"
                    max="100"
                    value={videoCount}
                    onChange={(e) => setVideoCount(Number(e.target.value))}
                    className="border border-gray-300 rounded-md p-2 text-gray-700 w-full"
                />
                <Button
                    onClick={handleProcess}
                    disabled={loadingAnalysis}
                    className="bg-blue-500 text-white hover:bg-blue-600 px-6 py-3 rounded-md font-semibold"
                >
                    {loadingAnalysis ? "Processing..." : "Start Analysis"}
                </Button>
            </div>

            {/* Right Side: Display Existing Videos */}
            <div className="flex items-center justify-center w-1/3">
                <Button
                    onClick={handleDisplay}
                    disabled={loadingDisplay}
                    className="bg-green-500 text-white hover:bg-green-600 px-6 py-3 rounded-md font-semibold"
                >
                    {loadingDisplay ? "Loading..." : "Display Videos"}
                </Button>
            </div>
        </div>
    );
};

export default Action;
