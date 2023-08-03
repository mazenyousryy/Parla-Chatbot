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
        question: "Have you noticed any changes in your mood or behavior during recent interactions with your family or friends?",
        choice1: "I avoid talking to some people and I think a lot",
        choice2: "I feel I share absolutely nothing in common with others, including my friends and family",
        choice3: "More than Half the Days",
        choice4: "Feeling afraid, as if something awful might happen",
    },
    {
        question: "How would you describe your overall mood lately?",
        choice1: "I feel anxious and on edge most of the time.",
        choice2: "I often feel sad or down.",
        choice3: "I experience frequent mood swings.",
        choice4: "I feel consistently happy and content.",
    },
    {
        question: "How well have you been sleeping?",
        choice1: "I have been sleeping soundly and waking up refreshed.",
        choice2: "I have trouble falling asleep or staying asleep.",
        choice3: "I have been experiencing nightmares or vivid dreams.",
        choice4: "I often feel restless and have difficulty relaxing enough to sleep.",
    },
    {
        question: "Are you experiencing changes in appetite or weight?",
        choice1: "My appetite and weight have remained stable.",
        choice2: "I have noticed a significant increase in appetite and weight.",
        choice3: "I have noticed a significant decrease in appetite and weight.",
        choice4: "I experience fluctuations in appetite and weight, often related to stress.",
    },
    {
        question: "How would you rate your level of energy and motivation?",
        choice1: "I feel consistently energized and motivated.",
        choice2: "I often feel lethargic and lack motivation.",
        choice3: "I experience bursts of energy followed by periods of exhaustion.",
        choice4: "I struggle with low energy and find it difficult to stay motivated.",
    },
    {
        question: "Have you been able to concentrate and focus on tasks?",
        choice1: "I have no issues with concentration or focus.",
        choice2: "I often feel mentally foggy and have trouble completing tasks.",
        choice3: "I experience racing thoughts and have difficulty focusing.",
        choice4: "I find it challenging to concentrate and easily get distracted.",
    },
    {
        question: "Do you frequently experience feelings of guilt or worthlessness?",
        choice1: "I rarely feel guilty or worthless.",
        choice2: "I experience occasional feelings of guilt or worthlessness.",
        choice3: "I frequently feel guilty or worthless without a specific reason.",
        choice4: "I have persistent and overwhelming feelings of guilt or worthlessness.",
    },
    {
        question: "Are you withdrawing from social activities or isolating yourself?",
        choice1: "I have completely withdrawn from social activities and feel isolated.",
        choice2: "I find myself avoiding social interactions more often than not.",
        choice3: "I occasionally feel the need to withdraw, but it's not a major concern.",
        choice4: "I actively engage in social activities and enjoy being around others.",
    },
    {
        question: "Do you find it challenging to control your temper or anger?",
        choice1: "Not at All",
        choice2: "Several Days",
        choice3: "More than Half the Days",
        choice4: "Nearly Every Day",
    },
    {
        question: "Are you experiencing any physical symptoms without a clear medical cause?",
        choice1: "I am not experiencing any unexplained physical symptoms.",
        choice2: "I have occasional headaches or stomachaches without an apparent cause.",
        choice3: "I frequently experience physical symptoms like headaches, stomachaches, or muscle tension.",
        choice4: "I have persistent and debilitating physical symptoms that doctors cannot explain.",
    },
    {
        question: "Are you overly concerned about your appearance or body image?",
        choice1: "Not at All, I don't care",
        choice2: "Several Days, I look to the mirror",
        choice3: "Only when someone give me comment on my body",
        choice4: "Nearly Every Day, I am not satisfied with my body shape",
    },
    {
        question: "How would you describe your ability to cope with stress and difficult emotions?",
        choice1: "I have effective coping strategies and can manage stress well.",
        choice2: "I struggle at times but can generally find ways to cope with stress.",
        choice3: "I feel completely overwhelmed and have no effective coping mechanisms.",
        choice4: " I often feel overwhelmed and have difficulty coping with stress.",
    },
    {
        question: "Do you have a support system or people you can confide in?",
        choice1: "I have a strong support system and can confide in them whenever needed.",
        choice2: "I have a few people I can talk to but wish I had more support.",
        choice3: "I feel isolated and lack a reliable support system.",
        choice4: "I have no one to turn to and feel completely alone.",
    },
    {
        question: "How would you rate your overall satisfaction with life?",
        choice1: "I feel completely dissatisfied and find no joy or fulfillment in my life.",
        choice2: "I often feel dissatisfied and unfulfilled in various aspects of my life.",
        choice3: "I have moments of satisfaction but also areas of dissatisfaction.",
        choice4: "I am generally satisfied and content with my life.",
    },
];

//CONSTANTS
const CORRECT_BONUS = 10;
const MAX_QUESTIONS = 12;

startTest = () => {
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

startTest();
