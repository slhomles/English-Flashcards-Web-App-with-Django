const recordButton = document.getElementById('startRecording');
const recognitionResult = document.getElementById('recognitionResult');
const pronunciationResult = document.getElementById('pronunciationResult');
let mediaRecorder;
let audioChunks = [];

// Ngăn sự kiện lật thẻ khi nhấn nút "Start Recording"
recordButton.addEventListener('click', (event) => {
    event.stopPropagation(); // Ngăn không cho sự kiện click lan đến thẻ lật
    
    // Bắt đầu ghi âm
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
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
                .then(response => response.json())
                .then(data => {
                    if (data.correct) {
                        pronunciationResult.textContent = "Correct";
                        pronunciationResult.style.color = "green";
                    } else {
                        pronunciationResult.textContent = "Try Again - Phát âm chưa đúng.";
                        pronunciationResult.style.color = "red";
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    recognitionResult.textContent = 'Lỗi khi gửi dữ liệu đến server.';
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
