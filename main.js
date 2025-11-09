// static/js/main.js
document.addEventListener("DOMContentLoaded", function() {
    
    // Find the elements on the dashboard page
    const recommendBtn = document.getElementById("recommend-btn");
    const skillsInput = document.getElementById("skills-input");
    const resultsList = document.getElementById("results-list");
    const loadingSpinner = document.getElementById("loading-spinner");

    // Only run if the recommend button exists on the page
    if (recommendBtn) {
        recommendBtn.addEventListener("click", function() {
            const skillsText = skillsInput.value;
            
            if (skillsText.trim() === "") {
                alert("Please enter at least one skill.");
                return;
            }

            // Split the comma-separated string into an array of strings
            // Also trim whitespace and filter out any empty strings
            const skillsArray = skillsText.split(',')
                                         .map(skill => skill.trim()) 
                                         .filter(skill => skill.length > 0); 

            // Show loading, clear old results
            loadingSpinner.style.display = "block";
            resultsList.innerHTML = ""; // Clear previous results

            // Call our Flask API using fetch()
            fetch("/api/recommend", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ skills: skillsArray })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // Hide loading spinner
                loadingSpinner.style.display = "none";

                // 'data' is the JSON array of job titles from our API
                if (data && data.length > 0) {
                    data.forEach(jobTitle => {
                        const li = document.createElement("li");
                        li.textContent = jobTitle;
                        resultsList.appendChild(li);
                    });
                } else {
                    resultsList.innerHTML = "<li>No recommendations found. Try different skills.</li>";
                }
            })
            .catch(error => {
                // Handle any errors
                loadingSpinner.style.display = "none";
                console.error("Error fetching recommendations:", error);
                resultsList.innerHTML = "<li>An error occurred. Please check the console or try again.</li>";
            });
        });
    }
});