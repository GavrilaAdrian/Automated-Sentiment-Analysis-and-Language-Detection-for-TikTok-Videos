// src/types.ts
export interface ProcessedVideo {
    _id: {
        $oid: string;
    };
    video_id: string;
    video_timestamp: string;
    video_duration: string;
    video_locationcreated: string;
    video_sharecount: string;
    video_commentcount: string;
    video_playcount: string;
    video_is_ad: string;
    author_username: string;
    author_name: string;
    author_followercount: string;
    author_followingcount: string;
    author_heartcount: string;
    author_videocount: string;
    author_verified: string;
    language: string;
    sentence: string;
    sentiment_score: string;
    video_file: string;
}

// ResultsData remains the same
export interface ResultsData {
    total_videos: number;
    processed_videos: ProcessedVideo[];
}
