const form = document.getElementById("edu-form");
const task = document.getElementById("task");
const level = document.getElementById("level");
const levelLabel = document.getElementById("level-label");
const input = document.getElementById("input-text");
const inputLabel = document.getElementById("input-label");
const result = document.getElementById("result");
const status = document.getElementById("status");
const submitButton = document.getElementById("submit-button");
const clearButton = document.getElementById("clear-button");

const taskConfig = {
    qa: {
        label: "Your question",
        placeholder: "Example: What is the largest ocean?",
        showLevel: false
    },
    explain: {
        label: "Topic to explain",
        placeholder: "Example: Explain the Pythagoras theorem.",
        showLevel: true
    },
    quiz: {
        label: "Passage for quiz generation",
        placeholder: "Paste at least 20 characters of educational text here.",
        showLevel: false
    },
    summarize: {
        label: "Text to summarize",
        placeholder: "Paste an educational passage here.",
        showLevel: false
    },
    learn: {
        label: "Topic for a learning path",
        placeholder: "Example: SQL",
        showLevel: true
    }
};

function updateForm() {
    const config = taskConfig[task.value];
    inputLabel.textContent = config.label;
    input.placeholder = config.placeholder;
    levelLabel.classList.toggle("hidden", !config.showLevel);
    level.classList.toggle("hidden", !config.showLevel);
}

task.addEventListener("change", updateForm);
updateForm();

function showStatus(message, isError = false) {
    status.textContent = message;
    status.classList.remove("hidden", "error");
    if (isError) status.classList.add("error");
}

function hideStatus() {
    status.classList.add("hidden");
}

function renderText(text) {
    result.textContent = text;
    result.classList.remove("hidden");
}

function renderQuiz(data) {
    result.innerHTML = "";
    data.questions.forEach((q, index) => {
        const wrapper = document.createElement("article");
        wrapper.className = "quiz-question";

        const heading = document.createElement("h3");
        heading.textContent = `${index + 1}. ${q.question}`;
        wrapper.appendChild(heading);

        q.options.forEach(option => {
            const div = document.createElement("div");
            div.className = "option";
            div.textContent = option;
            if (option === q.correct_answer) div.classList.add("correct");
            wrapper.appendChild(div);
        });

        const explanation = document.createElement("p");
        explanation.innerHTML = `<strong>Answer:</strong> ${escapeHtml(q.correct_answer)}<br>${escapeHtml(q.explanation)}`;
        wrapper.appendChild(explanation);

        result.appendChild(wrapper);
    });
    result.classList.remove("hidden");
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const text = input.value.trim();
    if (!text) return;

    submitButton.disabled = true;
    hideStatus();
    result.classList.add("hidden");
    showStatus("EduGenie is thinking...");

    const endpoint = {
        qa: "/qa",
        explain: "/explain",
        quiz: "/quiz",
        summarize: "/summarize",
        learn: "/learn/recommendations"
    }[task.value];

    const body = task.value === "qa"
        ? { question: text }
        : task.value === "explain"
            ? { topic: text, level: level.value }
            : task.value === "quiz"
                ? { text, count: 3 }
                : task.value === "summarize"
                    ? { text, max_sentences: 5 }
                    : { topic: text, level: level.value };

    try {
        const response = await fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "The request failed.");
        }

        hideStatus();

        if (task.value === "qa") renderText(data.answer);
        else if (task.value === "explain") renderText(data.explanation);
        else if (task.value === "quiz") renderQuiz(data);
        else if (task.value === "summarize") renderText(data.summary);
        else renderText(data.recommendations);
    } catch (error) {
        showStatus(error.message, true);
    } finally {
        submitButton.disabled = false;
    }
});

clearButton.addEventListener("click", () => {
    input.value = "";
    result.innerHTML = "";
    result.classList.add("hidden");
    hideStatus();
});
