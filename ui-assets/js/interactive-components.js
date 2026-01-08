// Interactive Components for AI Fundamentals Course

// Knowledge Check Component
function initKnowledgeChecks() {
  document.querySelectorAll('.knowledge-check').forEach(container => {
    const submitBtn = container.querySelector('.knowledge-check-submit');
    if (submitBtn) {
      submitBtn.addEventListener('click', function() {
        const selected = container.querySelector('input[type="radio"]:checked');
        const correct = container.dataset.correct;
        const feedbackDiv = container.querySelector('.knowledge-check-feedback');
        
        if (!selected) {
          feedbackDiv.textContent = 'Please select an answer.';
          feedbackDiv.style.display = 'block';
          feedbackDiv.className = 'knowledge-check-feedback warning';
          return;
        }
        
        const isCorrect = selected.value === correct;
        feedbackDiv.textContent = isCorrect 
          ? '✓ ' + container.dataset.correctFeedback
          : '✗ ' + container.dataset.incorrectFeedback;
        feedbackDiv.className = 'knowledge-check-feedback ' + (isCorrect ? 'correct' : 'incorrect');
        feedbackDiv.style.display = 'block';
        
        // Disable all inputs
        container.querySelectorAll('input[type="radio"]').forEach(input => {
          input.disabled = true;
        });
        submitBtn.disabled = true;
      });
    }
  });
}

// Sorting Activity Component
function allowDrop(ev) {
  ev.preventDefault();
}

function drag(ev) {
  ev.dataTransfer.setData("text", ev.target.dataset.value);
  ev.target.style.opacity = "0.5";
}

function drop(ev, activityId) {
  ev.preventDefault();
  const data = ev.dataTransfer.getData("text");
  const item = document.querySelector(`[data-activity-id="${activityId}"] [data-value="${data}"]`);
  const target = document.getElementById(`target-${activityId}`);
  
  if (item && target && !target.querySelector(`[data-value="${data}"]`)) {
    const clone = item.cloneNode(true);
    clone.style.opacity = "1";
    clone.draggable = true;
    clone.ondragstart = function(e) { drag(e); };
    target.appendChild(clone);
    item.remove();
  }
}

function checkSorting(activityId, correctOrder) {
  const target = document.getElementById(`target-${activityId}`);
  if (!target) return;
  
  const items = Array.from(target.querySelectorAll('.sortable-item'));
  const currentOrder = items.map(item => item.dataset.value);
  const isCorrect = JSON.stringify(currentOrder) === JSON.stringify(correctOrder);
  const feedback = document.getElementById(`feedback-${activityId}`);
  
  if (feedback) {
    feedback.textContent = isCorrect 
      ? '✓ Correct! Items are in the right order.'
      : '✗ Incorrect. Please try again.';
    feedback.className = 'sorting-feedback ' + (isCorrect ? 'correct' : 'incorrect');
    feedback.style.display = 'block';
  }
}

function initSortingActivities() {
  document.querySelectorAll('.sortable-item').forEach(item => {
    item.ondragstart = function(e) { drag(e); };
  });
}

// Accordion Component
function toggleAccordion(button) {
  const item = button.closest('.accordion-item');
  const content = item.querySelector('.accordion-content');
  const icon = button.querySelector('.accordion-icon');
  const isOpen = content.style.display !== 'none';
  
  content.style.display = isOpen ? 'none' : 'block';
  icon.textContent = isOpen ? '▼' : '▲';
  item.classList.toggle('active', !isOpen);
}

// Flashcards Component
const flashcardData = {};

function initFlashcards(cardSetId, cards) {
  flashcardData[cardSetId] = {
    cards: cards,
    currentIndex: 0,
    isFlipped: false
  };
  const totalSpan = document.getElementById(`total-${cardSetId}`);
  if (totalSpan) {
    totalSpan.textContent = cards.length;
  }
}

function showCard(cardSetId, index, question, answer) {
  const data = flashcardData[cardSetId];
  if (!data) return;
  
  data.currentIndex = index;
  data.isFlipped = false;
  
  const card = document.getElementById(`card-${cardSetId}`);
  if (!card) return;
  
  const cardInner = card.querySelector('.flashcard-inner');
  if (cardInner) {
    cardInner.classList.remove('flipped');
  }
  
  const frontContent = card.querySelector('.flashcard-front .flashcard-content');
  const backContent = card.querySelector('.flashcard-back .flashcard-content');
  if (frontContent) frontContent.textContent = question;
  if (backContent) backContent.textContent = answer;
  
  const currentSpan = document.getElementById(`current-${cardSetId}`);
  if (currentSpan) {
    currentSpan.textContent = index + 1;
  }
  
  // Update active thumb
  document.querySelectorAll(`[data-card-set="${cardSetId}"] .flashcard-thumb`).forEach((thumb, i) => {
    thumb.classList.toggle('active', i === index);
  });
}

function flipCard(cardElement) {
  const inner = cardElement.querySelector('.flashcard-inner');
  if (inner) {
    inner.classList.toggle('flipped');
  }
}

function nextCard(cardSetId) {
  const data = flashcardData[cardSetId];
  if (!data || !data.cards.length) return;
  
  const nextIndex = (data.currentIndex + 1) % data.cards.length;
  const card = data.cards[nextIndex];
  showCard(cardSetId, nextIndex, card.question, card.answer);
}

function previousCard(cardSetId) {
  const data = flashcardData[cardSetId];
  if (!data || !data.cards.length) return;
  
  const prevIndex = (data.currentIndex - 1 + data.cards.length) % data.cards.length;
  const card = data.cards[prevIndex];
  showCard(cardSetId, prevIndex, card.question, card.answer);
}

// Interactive Process Component
const processData = {};

function initProcess(processId, totalSteps) {
  processData[processId] = {
    currentStep: 0,
    totalSteps: totalSteps
  };
  const totalSpan = document.getElementById(`total-steps-${processId}`);
  if (totalSpan) {
    totalSpan.textContent = totalSteps;
  }
  updateProcessUI(processId);
}

function nextStep(processId) {
  const data = processData[processId];
  if (data && data.currentStep < data.totalSteps - 1) {
    data.currentStep++;
    updateProcessUI(processId);
  }
}

function previousStep(processId) {
  const data = processData[processId];
  if (data && data.currentStep > 0) {
    data.currentStep--;
    updateProcessUI(processId);
  }
}

function resetProcess(processId) {
  const data = processData[processId];
  if (data) {
    data.currentStep = 0;
    updateProcessUI(processId);
  }
}

function updateProcessUI(processId) {
  const data = processData[processId];
  if (!data) return;
  
  const container = document.querySelector(`[data-process-id="${processId}"]`);
  if (!container) return;
  
  const steps = container.querySelectorAll('.process-step');
  const prevBtn = container.querySelector('.process-btn.prev');
  const nextBtn = container.querySelector('.process-btn.next');
  const progressFill = document.getElementById(`progress-${processId}`);
  const currentStepSpan = document.getElementById(`current-step-${processId}`);
  
  steps.forEach((step, index) => {
    step.classList.toggle('active', index === data.currentStep);
    step.classList.toggle('completed', index < data.currentStep);
  });
  
  if (prevBtn) prevBtn.disabled = data.currentStep === 0;
  if (nextBtn) nextBtn.disabled = data.currentStep === data.totalSteps - 1;
  
  if (progressFill) {
    const progress = ((data.currentStep + 1) / data.totalSteps) * 100;
    progressFill.style.width = progress + '%';
  }
  
  if (currentStepSpan) {
    currentStepSpan.textContent = data.currentStep + 1;
  }
}

// Initialize all components on page load
document.addEventListener('DOMContentLoaded', function() {
  initKnowledgeChecks();
  initSortingActivities();
  
  // Initialize processes
  document.querySelectorAll('.interactive-process').forEach(container => {
    const processId = container.dataset.processId;
    const totalSteps = container.querySelectorAll('.process-step').length;
    if (processId && totalSteps > 0) {
      initProcess(processId, totalSteps);
    }
  });
});
