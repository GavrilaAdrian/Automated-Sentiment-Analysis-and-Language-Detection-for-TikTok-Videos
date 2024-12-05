import React from "react";
import { Button } from "../components/ui/button";

export const Landing: React.FC = () => {
    const handleScroll = () => {
        document.getElementById("action-section")?.scrollIntoView({ behavior: "smooth" });
    };

    return (
        <div className="h-screen flex flex-col justify-center items-center bg-gradient-to-r from-purple-700 via-pink-500 to-red-400 text-white relative">
            <div className="absolute inset-0 opacity-30 bg-[url('https://source.unsplash.com/featured/?abstract,gradient')] bg-cover bg-center"></div>
            <div className="z-10 text-center px-4">
                <h1 className="text-5xl font-extrabold mb-6">
                    <span className="text-white">TikTok</span> <span className="text-yellow-300">Analyzer</span>
                </h1>
                <p className="text-xl max-w-3xl mx-auto mb-8">
                    Discover the influence of TikTok videos with just one click. Analyze their impact,
                    classification, and more in seconds.
                </p>
                <Button
                    onClick={handleScroll}
                    className="bg-yellow-400 text-black hover:bg-yellow-300 font-semibold px-6 py-3"
                >
                    Get Started
                </Button>
            </div>
        </div>
    );
};
