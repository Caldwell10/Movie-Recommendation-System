import React, {useState} from "react";
import axios from "axios";
import "./MovieRecommendation.css"

const MovieRecommendation = () => {
    const [userInput, setUserInput] = useState("");
    const [recommendations, setRecommendations] = useState(null)
    const [error, setError] = useState(null)
    const [loading, setLoading] = useState(false)

    const handleInputChange = (e) => {
        setUserInput(e.target.value);
    };
    const fetchRecommendations = async () => {
        if(!userInput.trim()){
            setError("Please enter a movie name.");
            return
        }
        setLoading(true);
        setError(null);

        try {
            const response = await axios.post("http://127.0.0.1:8002/recommend", {
                user_input: userInput,
            });
            setRecommendations(response.data.recommendations);
        }catch (error) {
            console.error("Error fetching recommendations:", error)
            setError("Failed to fetch recommendations. Please try again.");
        }finally{
            setLoading(false);
        }
    };
    return (
        <div className="container">
            <h1>🎬 Movie Recommendation System</h1>
            <div className="input-container">
                <input
                    type="text"
                    placeholder="Enter a movie title..."
                    value={userInput}
                    onChange={handleInputChange}
                />
                <button onClick={fetchRecommendations} disabled={loading}>
                    {loading ? "Loading..." : "Get Recommendations"}
                </button>
            </div>

            {error && <p className="error-message">{error}</p>}

            {recommendations && recommendations.length > 0 && (
                <div className="recommendations">
                    <h2>Recommended Movies:</h2>
                    <ul>
                        {recommendations.map((movie, index) => (
                            <li key={index}>
                                <strong>{movie.title}</strong> ({movie.year}) - ⭐ {movie.rating} <br />
                                <em>{movie.genres}</em> <br />
                                <p>{movie.summary}</p>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default MovieRecommendation;