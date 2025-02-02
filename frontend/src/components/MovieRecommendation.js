import React, { useState } from "react";
import axios from "axios";
import "./MovieRecommendation.css";
import { FaStar, FaSearch } from "react-icons/fa";

const MovieRecommendation = () => {
    const [userInput, setUserInput] = useState("");
    const [recommendations, setRecommendations] = useState([]);

    const handleInputChange = (e) => {
        setUserInput(e.target.value);
    };

    const fetchRecommendations = async () => {
        try {
            const response = await axios.post("http://127.0.0.1:8002/recommend", {
                user_input: userInput,
            });
            setRecommendations(response.data.recommendations);
        } catch (error) {
            console.error("Error fetching recommendations:", error);
        }
    };

    return (
        <div className="container">
            <h1 className="title">🎬 Movie Recommendation System</h1>

            <div className="input-container">
                <input
                    type="text"
                    placeholder="Enter a movie or genre..."
                    value={userInput}
                    onChange={handleInputChange}
                />
                <button onClick={fetchRecommendations}>
                    <FaSearch className="search-icon" /> Get Recommendations
                </button>
            </div>

            {recommendations.length > 0 && (
                <div className="recommendations">
                    <h2>Recommended Movies:</h2>
                    {recommendations.map((movie, index) => (
                        <div className="movie-card" key={index}>
                            <h3>
                                {movie.title} <span className="year">({movie.year})</span>
                            </h3>
                            <p className="genre">{movie.genres}</p>
                            <p className="rating">
                                <FaStar className="star-icon" /> {movie.rating}
                            </p>
                            <p className="summary">{movie.summary}</p>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default MovieRecommendation;
