const username = document.getElementById("username");
const saveScoreBtn = document.getElementById("saveScoreBtn");
const finalScore = document.getElementById("finalScore");
const mostRecentScore = localStorage.getItem("mostRecentScore");
const res = document.getElementById("res");
const img = document.getElementById("imgres");

const highScores = JSON.parse(localStorage.getItem("highScores")) || [];

const MAX_HIGH_SCORES = 5;

// finalScore.innerText = mostRecentScore;

if (mostRecentScore > 1000) {
    finalScore.innerText = "Your Mental Health Status is good";
    res.innerText = "According to your answers, your mental health status is good";
    img.src = "../static/images/ParloWithPhone.png";
} else {
    finalScore.innerText = "You need to take an action";
    res.innerText = "According to your answers, you may have symptoms of depression";
    img.src = "../../static/images/SadParlo.png";
}

username.addEventListener("keyup", () => {
    saveScoreBtn.disabled = !username.value;
});

saveHighScore = (e) => {
    e.preventDefault();

    const score = {
        score: mostRecentScore,
        name: username.value,
    };
    highScores.push(score);
    highScores.sort((a, b) => b.score - a.score);
    highScores.splice(5);

    localStorage.setItem("highScores", JSON.stringify(highScores));
    window.location.assign("/");
};
