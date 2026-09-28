const task = document.getElementById("task");
const level = document.getElementById("level");
const levelLabel = document.getElementById("levelLabel");
const inputLabel = document.getElementById("inputLabel");
const inputText = document.getElementById("inputText");
const submitButton = document.getElementById("submitButton");
const resultCard = document.getElementById("resultCard");
const result = document.getElementById("result");
const statusBadge = document.getElementById("statusBadge");
const copyButton = document.getElementById("copyButton");

const taskConfig = {
    qa: {
        label: "Your question",
        placeholder: "Example: Which is the largest ocean?",
    },
    explain: {
        label: "Concept to explain",
        placeholder: "Example: Explain the Pythagoras theorem simply.",
    },
    quiz: {
        label: "Passage or topic",
        placeholder: "Paste a passage or enter a topic from which to create 3 MCQs.",
    },
    summarize: {
        label: "Text to summarize",
        placeholder: "Paste an educational passage here.",
    },
    learn: {
        label: "Topic to learn",
        placeholder: "Example: SQL",
    },
};

function updateForm() {
    const selected = task.value;
    const config = taskConfig[selected];

    inputLabel.textContent = config.label;
    inputText.placeholder = config.placeholder;

    const learning = selected === "learn";

    level.classList.toggle("hidden", !learning);
    levelLabel.classList.toggle("hidden", !learning);
}

task.addEventListener("change", updateForm);
updateForm();

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function renderText(value) {
    result.innerHTML = `<div class="result-content">${escapeHtml(value)}</div>`;
}

function renderQuiz(data) {
    result.innerHTML = "";

    data.questions.forEach((q, index) => {
        const wrapper = document.createElement("div");
        wrapper.className = "quiz-question";

        wrapper.innerHTML = `
            <strong>${index + 1}. ${escapeHtml(q.question)}</strong>
        `;

        q.options.forEach((option) => {
            const button = document.createElement("button");

            button.className = "option";
            button.textContent = option;

            button.addEventListener("click", () => {
                wrapper.querySelectorAll(".option").forEach((b) => {
                    b.disabled = true;
                });

                const feedback = document.createElement("div");
                feedback.className = "feedback";

                if (option === q.correct_answer) {
                    button.classList.add("correct");
                    feedback.textContent = `Correct. ${q.explanation}`;
                } else {
                    button.classList.add("incorrect");

                    feedback.textContent =
                        `Not quite. Correct answer: ${q.correct_answer}. ${q.explanation}`;

                    wrapper.querySelectorAll(".option").forEach((b) => {
                        if (b.textContent === q.correct_answer) {
                            b.classList.add("correct");
                        }
                    });
                }

                wrapper.appendChild(feedback);
            });

            wrapper.appendChild(button);
        });

        result.appendChild(wrapper);
    });
}

async function runTask() {
    const text = inputText.value.trim();

    if (!text) {
        resultCard.classList.remove("hidden");
        result.innerHTML =
            '<div class="error">Please enter some text first.</div>';
        return;
    }

    submitButton.disabled = true;
    statusBadge.textContent = "Thinking…";

    resultCard.classList.remove("hidden");

    result.innerHTML =
        '<div class="result-content">EduGenie is working…</div>';

    let endpoint;
    let body;

    if (task.value === "qa") {
        endpoint = "/qa";
        body = { text };
    } else if (task.value === "explain") {
        endpoint = "/explain";
        body = { text };
    } else if (task.value === "quiz") {
        endpoint = "/quiz";
        body = { text };
    } else if (task.value === "summarize") {
        endpoint = "/summarize";
        body = { text };
    } else {
        endpoint = "/learn/recommendations";
        body = {
            topic: text,
            level: level.value,
        };
    }

    try {
        const response = await fetch(endpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(body),
        });

        /*
         * Read the response as text first.
         * This prevents the confusing:
         * "Unexpected token 'I', 'Internal S'..."
         * error when FastAPI returns a plain-text 500 error.
         */
        const responseText = await response.text();

        let data;

        try {
            data = JSON.parse(responseText);
        } catch (parseError) {
            if (!response.ok) {
                throw new Error(
                    `Server error (${response.status}): ${responseText}`
                );
            }

            throw new Error(
                `The server returned an invalid response: ${responseText}`
            );
        }

        if (!response.ok) {
            throw new Error(
                data.detail || data.message || "Request failed."
            );
        }

        if (task.value === "qa") {
            renderText(data.answer);
        } else if (task.value === "explain") {
            renderText(data.explanation);
        } else if (task.value === "quiz") {
            renderQuiz(data);
        } else if (task.value === "summarize") {
            renderText(data.summary);
        } else {
            renderText(data.recommendations);
        }

        statusBadge.textContent = "Complete";

    } catch (error) {
        console.error("EduGenie error:", error);

        result.innerHTML =
            `<div class="error">${escapeHtml(error.message)}</div>`;

        statusBadge.textContent = "Error";

    } finally {
        submitButton.disabled = false;
    }
}

submitButton.addEventListener("click", runTask);

copyButton.addEventListener("click", async () => {
    try {
        await navigator.clipboard.writeText(result.innerText);

        const original = copyButton.textContent;
        copyButton.textContent = "Copied";

        setTimeout(() => {
            copyButton.textContent = original;
        }, 1200);

    } catch (error) {
        console.error("Copy failed:", error);
    }
});