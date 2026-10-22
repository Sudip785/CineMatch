
const API_URL = "/api";

const searchForm = document.getElementById("search-form");
const movieInput = document.getElementById("movie-input");
const statusMessage = document.getElementById("status-message");
const matchingMovies = document.getElementById("matching-movies");
const recommendations = document.getElementById("recommendations");
const resultsTitle = document.getElementById("results-title");
const resultsCount = document.getElementById("results-count");
const searchButton = searchForm.querySelector("button");

function clearSearchMessages() {
    statusMessage.textContent = "";
    matchingMovies.replaceChildren();
}

function showMessage(message) {
    statusMessage.textContent = message;
}

function showMatchingMovies(titles) {
    matchingMovies.replaceChildren();

    titles.forEach((title) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "match-option";
        button.textContent = title;

        button.addEventListener("click", () => {
            movieInput.value = title;
            searchForm.requestSubmit();
        });

        matchingMovies.appendChild(button);
    });
}

function showRecommendations(movies, searchedMovie) {
    recommendations.replaceChildren();

    resultsTitle.textContent = `Movies similar to ${searchedMovie}`;
    resultsCount.textContent = `${movies.length} recommendations`;

    if (movies.length === 0) {
        recommendations.textContent = "No recommendations found.";
        return;
    }

    movies.forEach((movie, index) => {
        const card = document.createElement("article");
        card.className = "movie-card";

        const poster = document.createElement("img");
        poster.className = "movie-poster";
        poster.alt = `Poster for ${movie.title}`;
        poster.loading = "lazy";

        poster.onerror = () => {
            poster.onerror = null;
            poster.src =
                "https://placehold.co/500x750/202033/ffffff?text=Poster+Unavailable";
        };

        poster.src =
            movie.poster_url ||
            "https://placehold.co/500x750/202033/ffffff?text=Poster+Unavailable";

        const number = document.createElement("span");
        number.className = "movie-number";
        number.textContent = String(index + 1).padStart(2, "0");

        const title = document.createElement("h3");
        title.textContent = movie.title;

        const genreList = document.createElement("div");
        genreList.className = "genre-list";

        const genres = movie.genres
            ? movie.genres.split("|")
            : [];

        genres.forEach((genre) => {
            const tag = document.createElement("span");
            tag.className = "genre-tag";
            tag.textContent = genre;
            genreList.appendChild(tag);
        });

        const details = document.createElement("div");
        details.className = "movie-details";
        details.append(title, genreList);

        card.append(number, poster, details);
        recommendations.appendChild(card);
    });
}

searchForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const movie = movieInput.value.trim();

    if (!movie) {
        showMessage("Please enter a movie name.");
        return;
    }

    clearSearchMessages();
    searchButton.disabled = true;
    searchButton.textContent = "Searching...";
    resultsCount.textContent = "";

    try {
        const url = new URL(
            `${API_URL}/recommend`,
            window.location.origin
        );

        url.searchParams.set("movie", movie);
        url.searchParams.set("count", "5");

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(
                `The server returned an error: ${response.status}`
            );
        }

        const data = await response.json();

        if (data.matching_titles) {
            showMessage(
                data.message || "Select the correct movie:"
            );
            showMatchingMovies(data.matching_titles);
        } else if (data.recommendations) {
            clearSearchMessages();

            showRecommendations(
                data.recommendations,
                data.searched_movie || movie
            );
        } else {
            showMessage(data.message || "No results found.");
        }
    } catch (error) {
        showMessage(
            "Could not connect to CineMatch. Make sure the backend is running."
        );
        console.error("CineMatch request failed:", error);
    } finally {
        searchButton.disabled = false;
        searchButton.innerHTML = 'Find Movies <span>→</span>';
    }
});
