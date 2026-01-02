// Online/Offline Check
window.addEventListener('online', updateStatus);
window.addEventListener('offline', updateStatus);

function updateStatus() {
    const status = document.getElementById('online-status');
    if (navigator.onLine) {
        status.innerText = "ONLINE";
        status.style.color = "#00ff00";
    } else {
        status.innerText = "OFFLINE - Check Connection";
        status.style.color = "#ff0000";
        alert("Bot signal nahi dega jab tak aap online nahi hotay.");
    }
}

function checkAuth() {
    const inputCode = document.getElementById('auth-code').value;
    if (inputCode === CONFIG.SECURITY_CODE) {
        document.getElementById('login-screen').style.display = 'none';
        document.getElementById('main-bot').style.display = 'block';
        updateStatus();
    } else {
        alert("Wrong Security Code!");
    }
}

async function generateSignal() {
    if (!navigator.onLine) return alert("You are offline!");

    const pair = document.getElementById('asset-pair').value;
    document.getElementById('signal-text').innerText = "ANALYZING MARKET...";

    // Simulated Gemini AI / Forex Logic
    // Haqeeqi API integration ke liye yahan fetch use karein
    setTimeout(() => {
        const signals = ["STRONG CALL ⬆️", "STRONG PUT ⬇️", "WAIT - NO SIGNAL"];
        const result = signals[Math.floor(Math.random() * signals.length)];
        
        const display = document.getElementById('signal-text');
        display.innerText = result;
        
        if(result.includes("CALL")) display.style.color = "#00ff00";
        else if(result.includes("PUT")) display.style.color = "#ff0000";
        else display.style.color = "#ffd700";

        startTimer();
    }, 2000);
}

function startTimer() {
    let timeLeft = 60;
    const timerElem = document.getElementById('timer');
    const interval = setInterval(() => {
        timeLeft--;
        timerElem.innerText = `Expiry: 00:${timeLeft < 10 ? '0'+timeLeft : timeLeft}`;
        if (timeLeft <= 0) clearInterval(interval);
    }, 1000);
}
