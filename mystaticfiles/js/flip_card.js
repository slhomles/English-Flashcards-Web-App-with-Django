function toggleFlip(card) {
  const cardInner = card.querySelector('.flip-card-inner');
  if (cardInner) {
      cardInner.classList.toggle('flipped');
  }
}