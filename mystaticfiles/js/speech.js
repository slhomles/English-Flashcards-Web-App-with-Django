// JavaScript để xử lý nhận diện giọng nói
const startRecognitionButton = document.getElementById('startRecognition');
const recognitionResult = document.getElementById('recognitionResult');
const pronunciationResult = document.getElementById('pronunciationResult');

// Kiểm tra xem trình duyệt có hỗ trợ Web Speech API hay không
if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();

    recognition.lang = 'en-US';  // Thiết lập ngôn ngữ tiếng Anh
    recognition.interimResults = false;  // Chỉ lấy kết quả cuối cùng

    // Hàm viết hoa chữ cái đầu của từ
    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
    }

    // Xử lý kết quả khi người dùng phát âm
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript; // Nhận kết quả nhận diện
        const capitalizedTranscript = capitalizeFirstLetter(transcript); // Viết hoa chữ cái đầu

        // Hiển thị kết quả người dùng đã nói
        recognitionResult.textContent = `Bạn đã nói: ${capitalizedTranscript}`;

        // Từ cần kiểm tra 
        const correctWordElement = document.getElementById('correctWord');
        const correctWord = correctWordElement.dataset.word;

        // In ra để debug
        console.log("Kết quả đã nhận diện:", transcript);
        console.log("Kết quả sau khi viết hoa:", capitalizedTranscript);
        console.log("Từ cần kiểm tra từ Django:", correctWord);

        // So sánh với từ cần phát âm
        if (capitalizedTranscript.trim() === correctWord.trim()) {
            pronunciationResult.textContent = "Correct"; // Hiển thị chữ "Correct"
            pronunciationResult.style.color = "green"; // Màu xanh cho kết quả đúng
        } else {
            pronunciationResult.textContent = "Try Again - Phát âm chưa đúng."; // Chi tiết hơn cho kết quả sai
            pronunciationResult.style.color = "red"; // Màu đỏ cho kết quả sai
        }
    };

    recognition.onerror = (event) => {
        recognitionResult.textContent = `Lỗi: ${event.error}`;
        console.error(`Error occurred during recognition: ${event.error}`);
    };

    startRecognitionButton.addEventListener('click', (event) => {
        event.stopPropagation(); // Ngăn không cho lật thẻ
        recognition.start();
        recognitionResult.textContent = "Đang nghe, vui lòng nói...";
        pronunciationResult.textContent = ""; // Xóa kết quả trước khi bắt đầu ghi âm mới
    });
} else {
    recognitionResult.textContent = "Trình duyệt của bạn không hỗ trợ nhận diện giọng nói.";
}
