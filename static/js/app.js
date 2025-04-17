// Wait for DOM to load
document.addEventListener("DOMContentLoaded", () => {
  // Elements
  const splashScreen = document.getElementById("splash-screen");
  const messageInput = document.getElementById("message-input");
  const sendButton = document.getElementById("send-button");
  const voiceButton = document.getElementById("voice-button");
  const pulseAnimation = document.getElementById("pulse-animation");
  const chatContainer = document.getElementById("chat-container");
  const statusElement = document.getElementById("status");
  const themeToggle = document.getElementById("theme-toggle");

  // Theme management
  function initTheme() {
    const savedTheme = localStorage.getItem("stella-theme");
    if (savedTheme === "light") {
      document.body.classList.add("light-theme");
      themeToggle.checked = true;
    }

    // Apply theme to all themed elements
    applyThemeToElements();
  }

  function toggleTheme() {
    document.body.classList.toggle("light-theme");
    const isLightTheme = document.body.classList.contains("light-theme");
    localStorage.setItem("stella-theme", isLightTheme ? "light" : "dark");

    // Apply theme to all themed elements
    applyThemeToElements();
  }

  function applyThemeToElements() {
    const isLightTheme = document.body.classList.contains("light-theme");
    const bgColor = isLightTheme ? "#f0f5ff" : "#0a0e17";
    const cardColor = isLightTheme ? "#ffffff" : "#0F1724";
    const inputBgColor = isLightTheme ? "#f3f4f6" : "#1a202c";
    const textColor = isLightTheme ? "#1f2937" : "#e0e0e0";
    const borderColor = isLightTheme
      ? "rgba(59, 130, 246, 0.2)"
      : "rgba(30, 64, 175, 0.3)";

    // Update themed elements
    document.querySelectorAll(".bg-[\\#0F1724]").forEach((el) => {
      el.style.backgroundColor = cardColor;
    });

    document.querySelectorAll(".bg-[\\#1a202c]").forEach((el) => {
      el.style.backgroundColor = inputBgColor;
    });

    document.querySelectorAll(".border-blue-900\\/30").forEach((el) => {
      el.style.borderColor = borderColor;
    });

    // Update text colors in messages
    if (isLightTheme) {
      document.querySelectorAll(".text-gray-200").forEach((el) => {
        el.classList.remove("text-gray-200");
        el.classList.add("text-gray-700");
      });
    } else {
      document.querySelectorAll(".text-gray-700").forEach((el) => {
        el.classList.remove("text-gray-700");
        el.classList.add("text-gray-200");
      });
    }
  }

  // Theme toggle event listener
  themeToggle.addEventListener("change", toggleTheme);

  // Initialize theme
  initTheme();

  // Speech recognition
  let recognition;
  let isRecording = false;

  // Check if speech recognition is supported
  if ("webkitSpeechRecognition" in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-US";

    recognition.onstart = () => {
      updateStatus("Listening...");
      isRecording = true;
      pulseAnimation.classList.remove("hidden");
      voiceButton.classList.remove("bg-blue-500");
      voiceButton.classList.add("bg-red-500");
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      messageInput.value = transcript;
    };

    recognition.onend = () => {
      updateStatus("Ready");
      isRecording = false;
      pulseAnimation.classList.add("hidden");
      voiceButton.classList.remove("bg-red-500");
      voiceButton.classList.add("bg-blue-500");

      if (messageInput.value.trim() !== "") {
        sendMessage();
      }
    };

    recognition.onerror = (event) => {
      console.error("Speech recognition error", event.error);
      updateStatus(`Error: ${event.error}`);
      isRecording = false;
      pulseAnimation.classList.add("hidden");
      voiceButton.classList.remove("bg-red-500");
      voiceButton.classList.add("bg-blue-500");
    };
  }

  // Hide splash screen after 3 seconds with a smooth fade out
  setTimeout(() => {
    splashScreen.style.opacity = "0";
    splashScreen.style.transition = "opacity 0.8s ease-in-out";
    setTimeout(() => (splashScreen.style.display = "none"), 800);
  }, 2500);

  // Event listeners
  messageInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  });

  sendButton.addEventListener("click", () => {
    sendMessage();
  });

  voiceButton.addEventListener("click", () => {
    if (recognition) {
      if (!isRecording) {
        recognition.start();
      } else {
        recognition.stop();
      }
    } else {
      alert("Speech recognition is not supported in your browser.");
    }
  });

  // Add typing animation to inputs for better feedback
  messageInput.addEventListener("focus", () => {
    const inputArea = messageInput.closest(".input-area");
    inputArea.classList.add("ring-2", "ring-blue-500", "ring-opacity-50");
  });

  messageInput.addEventListener("blur", () => {
    const inputArea = messageInput.closest(".input-area");
    inputArea.classList.remove("ring-2", "ring-blue-500", "ring-opacity-50");
  });

  // Function to send message
  function sendMessage() {
    const message = messageInput.value.trim();
    if (message === "") return;

    // Add user message to chat
    addMessage(message, "user");

    // Clear input
    messageInput.value = "";

    // Add focus back to input
    messageInput.focus();

    // Send to backend
    sendToBackend(message);
  }

  // Add message to chat
  function addMessage(text, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.className = "flex items-start fadeIn mb-4";

    // Format timestamp
    const now = new Date();
    const timeString = now.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

    if (sender === "user") {
      messageDiv.innerHTML = `
                <div class="flex-1"></div>
                <div class="user-bubble p-4 rounded-lg max-w-[80%]">
                    <div class="flex justify-between items-center mb-1">
                        <p class="text-blue-200 font-semibold">You</p>
                        <span class="text-xs text-blue-300/70">${timeString}</span>
                    </div>
                    <p class="text-gray-200">${escapeHTML(text)}</p>
                </div>
                <div class="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-blue-700 flex items-center justify-center ml-3 flex-shrink-0 shadow-lg">
                    <span class="text-white font-bold">U</span>
                </div>
            `;
    } else {
      messageDiv.innerHTML = `
                <div class="w-10 h-10 rounded-full bg-gradient-to-br from-green-500 to-green-700 flex items-center justify-center mr-3 flex-shrink-0 shadow-lg">
                    <span class="text-white font-bold">S</span>
                </div>
                <div class="bot-bubble p-4 rounded-lg max-w-[80%]">
                    <div class="flex justify-between items-center mb-1">
                        <p class="text-green-400 font-semibold">Stella</p>
                        <span class="text-xs text-green-300/70">${timeString}</span>
                    </div>
                    <p class="text-gray-200">${formatResponse(
                      escapeHTML(text)
                    )}</p>
                </div>
            `;
    }

    chatContainer.querySelector(".space-y-4").appendChild(messageDiv);
    scrollToBottom();
  }

  // Format AI response with markdown-like formatting
  function formatResponse(text) {
    // Bold text between **
    text = text.replace(
      /\*\*(.*?)\*\*/g,
      '<strong class="text-blue-300">$1</strong>'
    );

    // Italic text between *
    text = text.replace(/\*(.*?)\*/g, "<em>$1</em>");

    // Convert URLs to links
    text = text.replace(
      /(https?:\/\/[^\s]+)/g,
      '<a href="$1" target="_blank" class="text-blue-400 underline hover:text-blue-300">$1</a>'
    );

    // Convert line breaks to <br>
    text = text.replace(/\n/g, "<br>");

    return text;
  }

  // Function to scroll chat to bottom
  function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  // Send message to backend
  function sendToBackend(message) {
    updateStatus("Processing...");

    fetch("/api/message", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    })
      .then((response) => response.json())
      .then((data) => {
        updateStatus("Ready");

        if (data.response) {
          // Small delay to simulate thinking
          setTimeout(() => {
            addMessage(data.response, "stella");
            speakResponse(data.response);
          }, 500);
        }

        if (data.error) {
          console.error("Error:", data.error);
          addMessage(`Sorry, I encountered an error: ${data.error}`, "stella");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        updateStatus("Ready");
        addMessage(
          "Sorry, I could not process your request at this time.",
          "stella"
        );
      });
  }

  // Update status display
  function updateStatus(message) {
    statusElement.textContent = message;
  }

  // Helper function to escape HTML
  function escapeHTML(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  // Text to speech
  function speakResponse(text) {
    if ("speechSynthesis" in window) {
      const speech = new SpeechSynthesisUtterance();

      // Strip html/markdown content for speech
      const plainText = text
        .replace(/<[^>]*>/g, "")
        .replace(/\*\*(.*?)\*\*/g, "$1")
        .replace(/\*(.*?)\*/g, "$1");
      speech.text = plainText;
      speech.volume = 1;
      speech.rate = 1;
      speech.pitch = 1;

      // Try to use a female voice if available
      const voices = speechSynthesis.getVoices();
      const femaleVoice = voices.find(
        (voice) =>
          voice.name.includes("female") ||
          voice.name.includes("Google") ||
          voice.name.includes("Samantha")
      );
      if (femaleVoice) {
        speech.voice = femaleVoice;
      }

      speechSynthesis.speak(speech);
    }
  }

  // Load voices (needed for some browsers)
  if ("speechSynthesis" in window) {
    speechSynthesis.onvoiceschanged = () => {
      speechSynthesis.getVoices();
    };
  }

  // Initialize by scrolling to bottom
  scrollToBottom();
});
