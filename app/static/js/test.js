const question = document.getElementById("question");
const choices = Array.from(document.getElementsByClassName("choice-text"));
const progressText = document.getElementById("progressText");
const scoreText = document.getElementById("score");
const progressBarFull = document.getElementById("progressBarFull");
let currentQuestion = {};
let acceptingAnswers = false;
let score = 0;
let questionCounter = 0;
let availableQuesions = [];

let questions = [
    {
        question: "How often do you feel overwhelmed by stress?",
        choice1: "Not at All",
        choice2: "Several Days",
        choice3: "More than Half the Days",
        choice4: "Nearly Every Day",
        answer: 1,
    },
    {
        question: "Are you experiencing any changes in your sleep patterns?",
        choice1: "Not at All",
        choice2: "Several Days",
        choice3: "More than Half the Days",
        choice4: "Nearly Every Day",
        answer: 3,
    },
    {
        question: "Do you often feel sad or depressed for no apparent reason?",
        choice1: "Not at All",
        choice2: "Several Days",
        choice3: "More than Half the Days",
        choice4: "Nearly Every Day",
        answer: 4,
    },
    {
        question: "How often do you feel overwhelmed by stress?",
        choice1: "Not at All",
        choice2: "Several Days",
        choice3: "More than Half the Days",
        choice4: "Nearly Every Day",
        answer: 1,
    },
    {
        question: "Have you noticed a loss of interest or pleasure in activities you used to enjoy?",
        choice1: "Not at All",
        choice2: "Several Days",
        choice3: "More than Half the Days",
        choice4: "Nearly Every Day",
        answer: 3,
    },
    {
        question: "Are you experiencing any changes in your appetite or weight?",
        choice1: "Not at All",
        choice2: "Several Days",
        choice3: "More than Half the Days",
        choice4: "Nearly Every Day",
        answer: 4,
    },
    {
        question: "Do you frequently experience racing thoughts or difficulty concentrating?",
        choice1: "Not at All",
        choice2: "Several Days",
        choice3: "More than Half the Days",
        choice4: "Nearly Every Day",
        answer: 1,
    },
    {
        question: "Have you noticed a lack of energy or motivation?",
        choice1: "Not at All",
        choice2: "Several Days",
        choice3: "More than Half the Days",
        choice4: "Nearly Every Day",
        answer: 3,
    },
    {
        question: "Do you find it challenging to control your temper or anger?",
        choice1: "Not at All",
        choice2: "Several Days",
        choice3: "More than Half the Days",
        choice4: "Nearly Every Day",
        answer: 4,
    },
    {
        question: "Are you engaging in risky behaviors or substance abuse?",
        choice1: "Not at All",
        choice2: "Several Days",
        choice3: "More than Half the Days",
        choice4: "Nearly Every Day",
        answer: 1,
    },
    {
        question: "Are you overly concerned about your appearance or body image?",
        choice1: "Not at All",
        choice2: "Several Days",
        choice3: "More than Half the Days",
        choice4: "Nearly Every Day",
        answer: 3,
    },
    {
        question: "Have you noticed a decline in your academic or work performance?",
        choice1: "Not at All",
        choice2: "Several Days",
        choice3: "More than Half the Days",
        choice4: "Nearly Every Day",
        answer: 4,
    },
    {
        question: "Do you have difficulty in making decisions or often second-guess yourself?",
        choice1: "Not at All",
        choice2: "Several Days",
        choice3: "More than Half the Days",
        choice4: "Nearly Every Day",
        answer: 1,
    },
    {
        question: "Have you had any thoughts of self-harm?",
        choice1: "Not at All",
        choice2: "Several Days",
        choice3: "More than Half the Days",
        choice4: "Nearly Every Day",
        answer: 3,
    },
    {
        question: "Are you excessively dependent on substances or behaviors (e.g., drugs, alcohol, gambling)?",
        choice1: "Not at All",
        choice2: "Several Days",
        choice3: "More than Half the Days",
        choice4: "Nearly Every Day",
        answer: 4,
    },
    {
        question: "Do you have difficulties in establishing or maintaining boundaries with others?",
        choice1: "Not at All",
        choice2: "Several Days",
        choice3: "More than Half the Days",
        choice4: "Nearly Every Day",
        answer: 1,
    },
    {
        question: "Have you noticed any changes in your social interactions or relationships?",
        choice1: "Not at All",
        choice2: "Several Days",
        choice3: "More than Half the Days",
        choice4: "Nearly Every Day",
        answer: 3,
    },
    {
        question: "Are you having recurrent thoughts of death or suicidal ideation?",
        choice1: "Not at All",
        choice2: "Several Days",
        choice3: "More than Half the Days",
        choice4: "Nearly Every Day",
        answer: 4,
    },
];

//CONSTANTS
const CORRECT_BONUS = 10;
const MAX_QUESTIONS = 12;

startGame = () => {
    questionCounter = 0;
    score = 0;
    availableQuesions = [...questions];
    getNewQuestion();
};

getNewQuestion = () => {
    if (availableQuesions.length === 0 || questionCounter >= MAX_QUESTIONS) {
        localStorage.setItem("mostRecentScore", score);
        //go to the end page
        return window.location.assign("/test_yourself/score");
    }
    questionCounter++;
    progressText.innerText = `Question ${questionCounter}/${MAX_QUESTIONS}`;
    //Update the progress bar
    progressBarFull.style.width = `${(questionCounter / MAX_QUESTIONS) * 100}%`;

    const questionIndex = Math.floor(Math.random() * availableQuesions.length);
    currentQuestion = availableQuesions[questionIndex];
    question.innerText = currentQuestion.question;

    choices.forEach((choice) => {
        const number = choice.dataset["number"];
        choice.innerText = currentQuestion["choice" + number];
    });

    availableQuesions.splice(questionIndex, 1);
    acceptingAnswers = true;
};

choices.forEach((choice) => {
    choice.addEventListener("click", (e) => {
        if (!acceptingAnswers) return;

        acceptingAnswers = false;
        const selectedChoice = e.target;
        const selectedAnswer = selectedChoice.dataset["number"];

        const classToApply = selectedAnswer == currentQuestion.answer ? "correct" : "incorrect";

        if (classToApply === "correct") {
            incrementScore(CORRECT_BONUS);
        }

        selectedChoice.parentElement.classList.add(classToApply);

        setTimeout(() => {
            selectedChoice.parentElement.classList.remove(classToApply);
            getNewQuestion();
        }, 1000);
    });
});

incrementScore = (num) => {
    score += num;
    scoreText.innerText = score;
};

startGame();
