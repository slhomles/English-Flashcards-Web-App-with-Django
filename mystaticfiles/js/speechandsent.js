const recordButton = document.getElementById('startRecording');
const recognitionResult = document.getElementById('recognitionResult');
const pronunciationResult = document.getElementById('pronunciationResult');
let mediaRecorder;
let audioChunks = [];

// Xử lý sự kiện nhấn nút ghi âm
recordButton.addEventListener('click', (event) => {
    event.stopPropagation(); // Ngăn không cho sự kiện click lan đến thẻ lật
    
    // Bắt đầu ghi âm
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = []; // Đặt lại danh sách âm thanh để tránh lỗi thêm dữ liệu vào cũ
            mediaRecorder.start();

            recognitionResult.textContent = "Đang ghi âm, vui lòng nói...";

            mediaRecorder.addEventListener('dataavailable', event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener('stop', () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const formData = new FormData();
                formData.append('audio', audioBlob, 'recording.wav');

                // Gửi file âm thanh đến backend để kiểm tra
                fetch('/check-pronunciation/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        // Xử lý các lỗi HTTP khác như 404, 500
                        if (response.status === 404) {
                            throw new Error('Không tìm thấy URL yêu cầu (404).');
                        } else if (response.status === 500) {
                            throw new Error('Lỗi server (500). Vui lòng thử lại sau.');
                        } else {
                            throw new Error(`Lỗi mạng: ${response.status} - ${response.statusText}`);
                        }
                    }
                    
                    // Kiểm tra content-type để đảm bảo phản hồi là JSON
                    const contentType = response.headers.get("content-type");
                    if (contentType && contentType.includes("application/json")) {
                        return response.json();
                    } else {
                        throw new Error("Phản hồi không phải là JSON hợp lệ.");
                    }
                })
                .then(data => {
                    if (data.correct) {
                        // Hiển thị từ mà hệ thống đã nhận diện được và kết quả đúng
                        recognitionResult.textContent = `Bạn đã nói: ${data.transcript}`;
                        pronunciationResult.textContent = "Correct";
                        pronunciationResult.style.color = "green";
                    } else {
                        // Hiển thị từ mà hệ thống đã nhận diện được và kết quả sai
                        recognitionResult.textContent = `Bạn đã nói: ${data.transcript}`;
                        pronunciationResult.textContent = "Try Again - Phát âm chưa đúng.";
                        pronunciationResult.style.color = "red";
                    }
                })
                .catch(error => {
                    console.error('Error:', error);

                    // Hiển thị thông báo lỗi chi tiết hơn
                    if (error.message.includes('404')) {
                        recognitionResult.textContent = 'Lỗi: Không tìm thấy URL yêu cầu (404).';
                    } else if (error.message.includes('500')) {
                        recognitionResult.textContent = 'Lỗi: Server gặp vấn đề (500). Vui lòng thử lại sau.';
                    } else if (error.message.includes('Phản hồi không phải là JSON hợp lệ')) {
                        recognitionResult.textContent = 'Lỗi: Phản hồi từ server không phải là JSON hợp lệ.';
                    } else {
                        recognitionResult.textContent = 'Đã xảy ra lỗi khi gửi dữ liệu đến server. Vui lòng kiểm tra kết nối mạng và thử lại.';
                    }
                });
            });

            // Dừng ghi âm sau 3 giây
            setTimeout(() => {
                mediaRecorder.stop();
                recognitionResult.textContent = "Đã dừng ghi âm.";
            }, 3000);
        })
        .catch(error => {
            console.error('Microphone access denied:', error);
            recognitionResult.textContent = 'Không thể truy cập micro. Vui lòng kiểm tra quyền truy cập.';
        });
});

// Hàm lấy CSRF token từ cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
