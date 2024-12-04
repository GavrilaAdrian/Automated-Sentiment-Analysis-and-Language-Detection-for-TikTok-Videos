import React from "react";
import { Card, CardHeader, CardContent } from "../components/ui/card";
import { ResultsData } from "../types";

interface ResultsProps {
    data: ResultsData | null;
}

export const Results: React.FC<ResultsProps> = ({ data }) => {
    // Log the incoming data to check structure
    console.log("Data received in Results component:", data);

    // Check if processed_videos array exists and log its contents
    if (data?.processed_videos) {
        console.log("Processed videos array:", data.processed_videos);
        console.log("First video object (if exists):", data.processed_videos[0]);
    }

    if (!data || !Array.isArray(data.processed_videos)) {
        console.log("Data is null or processed_videos is not an array.");
        return (
            <div className="h-screen flex items-center justify-center bg-gray-100">
                <p className="text-lg text-gray-500">No results yet. Analyze videos to see results.</p>
            </div>
        );
    }

    // Deduplicate videos by `video_id`
    const uniqueVideos = Array.from(
        new Map(data.processed_videos.map((video) => [video.video_id, video]))
    ).map(([_, video]) => video);

    console.log("Unique videos after deduplication:", uniqueVideos);

    // Sort videos by timestamp in descending order (newest first)
    const sortedVideos = [...uniqueVideos].sort((a, b) => {
        const dateA = new Date(a.video_timestamp);
        const dateB = new Date(b.video_timestamp);
    return dateB.getTime() - dateA.getTime(); // Descending order
    });


    return (
        <div id="results-section" className="h-screen bg-gray-100 p-8">
            <h2 className="text-3xl font-bold mb-6 text-center">Results</h2>
            <p className="text-lg mb-4 text-center">
                Total Videos Processed: {sortedVideos.length}
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {sortedVideos.map((video, index) => {
                    console.log(`Rendering video ${index + 1}:`, video); // Log each video object during rendering
                    return (
                        <Card key={video.video_id || index}>
                            <CardHeader>
                                <h3 className="text-lg font-semibold">Video {index + 1}</h3>
                            </CardHeader>
                            <CardContent>
                                <p>
                                    <strong>Video File:</strong> {video.video_file || "N/A"}
                                </p>
                                <p>
                                    <strong>Author:</strong> {video.author_name || "N/A"} (@{video.author_username || "N/A"})
                                </p>
                                <p>
                                    <strong>Play Count:</strong> {video.video_playcount || "0"}
                                </p>
                                <p>
                                    <strong>Sentiment Score:</strong> {video.sentiment_score || "N/A"}
                                </p>
                                <p>
                                    <strong>Language:</strong> {video.language || "N/A"}
                                </p>
                                <p>
                                    <strong>
                                        <a
                                            href={`/details?id=${video.video_id}`}
                                            className="text-blue-700 font-bold underline"
                                        >
                                            View Details
                                        </a>
                                    </strong>
                                </p>
                            </CardContent>
                        </Card>
                    );
                })}
            </div>
        </div>
    );
};
