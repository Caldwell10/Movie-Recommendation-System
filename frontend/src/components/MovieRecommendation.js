import React, {useState} from "react";
import axios from "axios";

const MovieRecommendation = () => {
    const [userInput, setUserInput] = useState("");
    const [recommendations, setRecommendations] = useState(null)

    const handleInputChange = (e) => {
        setUserInput(e.target.value);
    };
    const fetchRecommendations = async () => {
        try {
            const response = await axios.post("http://127.0.0.1:8002/recommend", {
                user_input: userInput,
            });
            setRecommendations(response.data.recommendations);
        }catch (error) {
            console.error("Error fetching recommendations:", error)
        }
    };
    return (
        <div>
            <h1>Movie Recommendation System</h1>
            <input
                type="text"
                placeholder="Enter your movie preferences"
                value={userInput}
                onChange={handleInputChange}
            />
            <button onClick={fetchRecommendations}>Get Recommendations</button>

            {recommendations && (
                <div>
                    <h2>Recommendations:</h2>
                    <ul>
                        {Object.entries(recommendations).map(([genre, score]) => (
                            <li key={genre}>
                                {genre}: {score.toFixed(2)}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};
export default MovieRecommendation;