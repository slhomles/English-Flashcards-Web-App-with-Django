// Cài đặt trò chơi
const hangmanImages = [
    "/static/images/hangman0.jpg",
    "/static/images/hangman1.jpg",
    "/static/images/hangman2.jpg",
    "/static/images/hangman3.jpg",
    "/static/images/hangman4.jpg",
    "/static/images/hangman5.jpg",
    "/static/images/hangman6.jpg"
];

const maxAttempts = 6;
let currentImageIndex = 0;
let word = "EXAMPLE"; // Bạn có thể thay đổi từ này hoặc lấy từ backend để ngẫu nhiên
let displayWord = "_ ".repeat(word.length).trim();
let attempts = 0;

// Khởi tạo hiển thị từ
document.getElementById("word-display").textContent = displayWord;

// Hàm cập nhật ảnh hangman
function updateHangmanImage() {
    document.getElementById("hangman-image").src = hangmanImages[currentImageIndex];
}
function startGame() {
    const imageElement = document.getElementById("hangman-image");
    if (imageElement) {
        imageElement.src = hangmanImages[0];
    }
    attempts = 0;
    currentImageIndex = 0;
    displayWord = "_ ".repeat(word.length).trim();
    document.getElementById("word-display").textContent = displayWord;
    document.getElementById("message").style.display = "none";
}

// Hàm đoán chữ
function guessLetter(letter, buttonElement) {
    if (attempts >= maxAttempts || displayWord === word) return; // Kết thúc trò chơi nếu thua hoặc đoán đúng
    
    let newDisplay = "";
    let correctGuess = false;

    // Kiểm tra từng chữ cái trong từ
    for (let i = 0; i < word.length; i++) {
        if (word[i] === letter) {
            newDisplay += letter + " ";
            correctGuess = true;
        } else {
            newDisplay += displayWord[i * 2] + " "; // giữ lại các ký tự đã đoán đúng
        }
    }

    // Cập nhật displayWord nếu đoán đúng
    displayWord = newDisplay.trim();
    document.getElementById("word-display").textContent = displayWord;

    // Thêm lớp CSS dựa trên kết quả đoán
    if (correctGuess) {
        buttonElement.classList.add("correct");
    } else {
        buttonElement.classList.add("incorrect");
        attempts++;
        currentImageIndex++;
        updateHangmanImage();
    }

    // Kiểm tra điều kiện thua
    if (attempts >= maxAttempts) {
        document.getElementById("message").style.display = "block";
        document.getElementById("correct-word").textContent = word;
    }

    // Kiểm tra điều kiện thắng
    if (displayWord.replace(/\s+/g, '') === word) {
        document.getElementById("message").style.display = "block";
        document.getElementById("message").style.color = "rgb(0, 128, 0)"; // Màu xanh lá cây
        document.getElementById("message").textContent = "Congratulations! You've guessed the word!";
    }
}

