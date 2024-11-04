// Lấy tất cả các thẻ flashcard
const cards = document.querySelectorAll('.flashcard-inner');

// Lặp qua từng thẻ và thêm sự kiện click để lật thẻ
cards.forEach(card => {
    card.addEventListener('click', function () {
        card.classList.toggle('flipped');
    });
});
