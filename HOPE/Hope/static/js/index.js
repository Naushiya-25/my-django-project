document.addEventListener('DOMContentLoaded', function() {
 
    document.getElementById('portfolioBtn').addEventListener('click', function() {
      const content = document.getElementById('portfolioContent');
      content.style.display = (content.style.display === 'block') ? 'none' : 'block';
    });
  
    
    document.querySelector("#reportForm").addEventListener('submit', function(event) {
      event.preventDefault();
      // Assuming form data is valid and processed
      window.location.href = 'thankyou.html';
    });
    const messagesContainer = document.getElementById('messages');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
  
    sendBtn.addEventListener('click', () => {
      const userMessage = userInput.value;
      if (userMessage) {
        addMessage('You', userMessage);
        respond(userMessage);
        userInput.value = '';
      }
    });
  
    const phoneInput = document.getElementById('phone');
    phoneInput.addEventListener('input', () => {
      const errorMessage = document.getElementById('phoneError');
      if (phoneInput.value.length !== 10) {
        errorMessage.style.display = 'block'; // Show error if not 10 digits
      } else {
        errorMessage.style.display = 'none'; // Hide error if valid
      }
    });
   
  });
  