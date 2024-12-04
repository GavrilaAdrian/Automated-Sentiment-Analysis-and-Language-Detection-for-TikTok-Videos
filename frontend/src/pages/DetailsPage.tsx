import React, { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { Card, CardHeader, CardContent } from "../components/ui/card";
import { Separator } from "../components/ui/separator";
import { Button } from "../components/ui/button";
import { ProcessedVideo } from "../types";
import { IconArrowLeft } from "@tabler/icons-react";

const DetailsPage: React.FC = () => {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const [videoDetails, setVideoDetails] = useState<ProcessedVideo | null>(null);
    const [loading, setLoading] = useState<boolean>(true);

    useEffect(() => {
        const fetchDetails = async () => {
            const id = searchParams.get("id");
            if (id) {
                try {
                    const response = await fetch(`http://127.0.0.1:5000/video/${id}`);
                    if (!response.ok) {
                        console.error("Error fetching video details:", response.status);
                        return;
                    }
                    const data = await response.json();
                    setVideoDetails(data || null);
                } catch (error) {
                    console.error("Error fetching video details:", error);
                } finally {
                    setLoading(false);
                }
            } else {
                setLoading(false);
            }
        };

        fetchDetails();
    }, [searchParams]);

    if (loading) {
        return (
            <div className="h-screen flex items-center justify-center bg-gray-100">
                <p className="text-lg text-gray-500">Loading video details...</p>
            </div>
        );
    }

    if (!videoDetails) {
        return (
            <div className="h-screen flex items-center justify-center bg-gray-100">
                <div className="text-center">
                    <p className="text-2xl text-red-500 font-bold mb-4">No video found!</p>
                    <p className="text-lg text-gray-600">
                        We couldn't find any video with the provided ID. Please check the URL or try again.
                    </p>
                    <a
                        href="/"
                        className="mt-6 inline-block bg-blue-500 text-white font-semibold py-2 px-4 rounded hover:bg-blue-600"
                    >
                        Go Back to Home
                    </a>
                </div>
            </div>
        );
    }

    return (
        <div className="bg-gray-50 min-h-screen p-8">
            <div className="max-w-5xl mx-auto bg-white shadow rounded-lg p-6">
                <div className="flex justify-between items-center mb-6">
                    <h1 className="text-3xl font-bold text-gray-800">Video Details</h1>
                    <Button
                        onClick={() => navigate("/")}
                        className="flex items-center space-x-2 bg-amber-300 text-stone-500 hover:bg-amber-400 hover:text-stone-700 px-4 py-2 rounded-md"
                    >
                        <IconArrowLeft size={18} />
                        <span>Go Home</span>
                    </Button>
                </div>

                <Separator className="mb-6" />

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Video Information Card */}
                    <Card className="shadow-md border border-gray-200 rounded-lg">
                        <CardHeader>
                            <h2 className="text-lg font-semibold text-gray-700">Video Information</h2>
                        </CardHeader>
                        <CardContent className="space-y-2">
                            <div className="flex justify-between items-center">
                                <p className="text-gray-600">Video ID:</p>
                                <p className="font-medium text-gray-800">{videoDetails.video_id}</p>
                            </div>
                            <div className="flex justify-between items-center">
                                <p className="text-gray-600">Timestamp:</p>
                                <p className="font-medium text-gray-800">{videoDetails.video_timestamp}</p>
                            </div>
                            <div className="flex justify-between items-center">
                                <p className="text-gray-600">Duration:</p>
                                <p className="font-medium text-gray-800">{videoDetails.video_duration} seconds</p>
                            </div>
                            <div className="flex justify-between items-center">
                                <p className="text-gray-600">Play Count:</p>
                                <p className="font-medium text-gray-800">{videoDetails.video_playcount}</p>
                            </div>
                            <div className="flex justify-between items-center">
                                <p className="text-gray-600">Share Count:</p>
                                <p className="font-medium text-gray-800">{videoDetails.video_sharecount}</p>
                            </div>
                            <div className="flex justify-between items-center">
                                <p className="text-gray-600">Is Ad:</p>
                                <p className="font-medium text-gray-800">
                                    {videoDetails.video_is_ad === "True" ? "Yes" : "No"}
                                </p>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Author Information Card */}
                    <Card className="shadow-md border border-gray-200 rounded-lg">
                        <CardHeader>
                            <h2 className="text-lg font-semibold text-gray-700">Author Information</h2>
                        </CardHeader>
                        <CardContent className="space-y-2">
                            <div className="flex justify-between items-center">
                                <p className="text-gray-600">Name:</p>
                                <p className="font-medium text-gray-800">
                                    {videoDetails.author_name} (@{videoDetails.author_username})
                                </p>
                            </div>
                            <div className="flex justify-between items-center">
                                <p className="text-gray-600">Followers:</p>
                                <p className="font-medium text-gray-800">{videoDetails.author_followercount}</p>
                            </div>
                            <div className="flex justify-between items-center">
                                <p className="text-gray-600">Videos:</p>
                                <p className="font-medium text-gray-800">{videoDetails.author_videocount}</p>
                            </div>
                            <div className="flex justify-between items-center">
                                <p className="text-gray-600">Verified:</p>
                                <p className="font-medium text-gray-800">
                                    {videoDetails.author_verified === "True" ? "Yes" : "No"}
                                </p>
                            </div>
                        </CardContent>
                    </Card>
                </div>

                <Separator className="my-6" />

                {/* Video Transcript */}
                <div>
                    <h2 className="text-lg font-semibold text-gray-700 mb-4">Video Transcript</h2>
                    <Card className="bg-gray-100 p-4 rounded-lg">
                        <p className="text-gray-800 leading-relaxed">{videoDetails.sentence}</p>
                    </Card>
                </div>

                <Separator className="my-6" />

                {/* Video Player */}
                <div className="flex justify-center items-center">
                    <div>
                        <h2 className="text-lg font-semibold text-gray-700 mb-4">Video Player</h2>
                        <video
                            src={`http://127.0.0.1:5000/video-files/${videoDetails.video_file}`}
                            controls
                            className="max-w-full max-h-[80vh] rounded-lg shadow-md"
                            style={{ objectFit: "contain" }}
                        >
                            Your browser does not support the video tag.
                        </video>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DetailsPage;
