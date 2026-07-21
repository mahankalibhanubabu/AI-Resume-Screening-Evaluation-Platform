const form = document.getElementById("resumeForm");
const fileInput = document.getElementById("resume");
const fileName = document.getElementById("fileName");
const submitBtn = document.getElementById("submitBtn");
const btnText = document.getElementById("btnText");
const btnSpinner = document.getElementById("btnSpinner");
const progressSection = document.getElementById("progressSection");
const progressMsg = document.getElementById("progressMsg");
const errorBanner = document.getElementById("errorBanner");
const errorMsg = document.getElementById("errorMsg");
const closeError = document.getElementById("closeError");
const resultSection = document.getElementById("resultSection");
const resetBtn = document.getElementById("resetBtn");
const stepElements = [
    document.getElementById("step1"),
    document.getElementById("step2"),
    document.getElementById("step3"),
    document.getElementById("step4"),
    document.getElementById("step5"),
];
const lineElements = document.querySelectorAll(".step-line");
const candidateNameInput = document.getElementById("candidateName");
const emailInput = document.getElementById("email");
const linkedinInput = document.getElementById("linkedin");
const atsScoreVal = document.getElementById("atsScoreVal");
const aiRatingVal = document.getElementById("aiRatingVal");
const compatibilityVal = document.getElementById("compatibilityVal");
const experienceVal = document.getElementById("experienceVal");
const recommendationVal = document.getElementById("recommendationVal");
const shortlistBadge = document.getElementById("shortlistBadge");
const shortlistedText = document.getElementById("shortlistedText");
const badgeIcon = document.getElementById("badgeIcon");
const skillsWrap = document.getElementById("skillsWrap");
const resultCandidateName = document.getElementById("resultCandidateName");
const ringFill = document.getElementById("ringFill");

const API_URL = "http://localhost:8000/api/analyze";

function updateFileLabel() {
    if (fileInput.files.length > 0) {
        fileName.classList.add("visible");
        fileName.innerHTML = `<i class="fa-regular fa-file"></i> ${fileInput.files[0].name}`;
    } else {
        fileName.classList.remove("visible");
        fileName.innerHTML = `<i class="fa-regular fa-file"></i> No file selected`;
    }
}

function hideError() {
    errorBanner.classList.add("hidden");
}

function showError(message) {
    errorMsg.textContent = message;
    errorBanner.classList.remove("hidden");
}

function setLoadingState(isLoading) {
    submitBtn.disabled = isLoading;
    btnText.classList.toggle("hidden", isLoading);
    btnSpinner.classList.toggle("hidden", !isLoading);
}

function setProgress(stepIndex, message) {
    progressSection.classList.remove("hidden");
    progressMsg.textContent = message;

    stepElements.forEach((step, index) => {
        step.classList.toggle("active", index === stepIndex);
        step.classList.toggle("done", index < stepIndex);
    });

    lineElements.forEach((line, index) => {
        line.classList.toggle("filled", index < stepIndex);
    });
}

function resetView() {
    form.reset();
    updateFileLabel();
    hideError();
    resultSection.classList.add("hidden");
    progressSection.classList.add("hidden");
    setLoadingState(false);
}

function escapeHtml(value) {
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/\"/g, "&quot;")
        .replace(/'/g, "&#39;");
}

function renderResult(payload) {
    const score = Number(payload.ats_score ?? 0);
    const circumference = 2 * Math.PI * 50;
    ringFill.style.strokeDasharray = circumference;
    ringFill.style.strokeDashoffset = circumference - (score / 100) * circumference;
    ringFill.style.stroke = "#6366f1";

    atsScoreVal.textContent = score;
    resultCandidateName.textContent = payload.candidate_name || candidateNameInput.value.trim();
    aiRatingVal.textContent = payload.ai_rating ?? "—";
    compatibilityVal.textContent = payload.compatibility_rating ?? "—";
    experienceVal.textContent = payload.experience || "—";
    recommendationVal.textContent = payload.recommendation || "—";

    const shortlisted = String(payload.shortlisted || "No").trim().toLowerCase();
    const isShortlisted = shortlisted === "yes";
    shortlistBadge.classList.toggle("yes", isShortlisted);
    shortlistBadge.classList.toggle("no", !isShortlisted);
    shortlistedText.textContent = isShortlisted ? "Shortlisted" : "Not Shortlisted";
    badgeIcon.className = `fa-solid ${isShortlisted ? "fa-check-circle" : "fa-xmark-circle"} badge-icon`;

    const skills = String(payload.skills || "")
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean);

    skillsWrap.innerHTML = skills.length
        ? skills.map((skill) => `<span class="skill-chip">${escapeHtml(skill)}</span>`).join("")
        : '<span class="detail-value">No skills detected</span>';

    resultSection.classList.remove("hidden");
    resultSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

fileInput.addEventListener("change", updateFileLabel);
closeError.addEventListener("click", hideError);
resetBtn.addEventListener("click", resetView);

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    hideError();

    const fullName = candidateNameInput.value.trim();
    const email = emailInput.value.trim();
    const linkedin = linkedinInput.value.trim();
    const resume = fileInput.files[0];

    if (!fullName || !email || !linkedin) {
        showError("Please fill in your name, email, and LinkedIn profile.");
        return;
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
        showError("Please provide a valid email address.");
        return;
    }

    if (!linkedin.startsWith("http://") && !linkedin.startsWith("https://")) {
        showError("Please provide a valid LinkedIn URL.");
        return;
    }

    if (!resume) {
        showError("Please upload a PDF resume before submitting.");
        return;
    }

    setLoadingState(true);
    setProgress(0, "Uploading Resume...");

    const formData = new FormData();
    formData.append("full_name", fullName);
    formData.append("email", email);
    formData.append("linkedin", linkedin);
    formData.append("resume", resume);

    try {
        setProgress(1, "Analyzing Resume...");
        const response = await fetch(API_URL, {
            method: "POST",
            body: formData,
        });

        const payload = await response.json().catch(() => null);

        if (!response.ok) {
            const detail = payload?.detail || `Request failed with status ${response.status}`;
            throw new Error(detail);
        }

        setProgress(2, "Generating ATS Report...");
        setProgress(3, "Sending Email...");
        setProgress(4, "Completed");

        const result = payload?.data || payload;
        renderResult(result);
    } catch (error) {
        console.error(error);
        setLoadingState(false);
        setProgress(0, "Analysis failed");
        showError(error.message || "Unable to connect to the backend server. Please try again.");
    } finally {
        setLoadingState(false);
    }
});

updateFileLabel();
resetView();
