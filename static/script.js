class BoggleGame {
  // Create new game at this DOM id
  
  constructor(boardId, secs = 60) {
    this.secs = secs;
    this.showTimer();

    this.words = new Set();
    this.board = $("#" + boardId);
    this.score = 0;

    this.timer = setInterval(this.tick.bind(this), 1000)
  
    $(".add-guess").on("submit", this.handleSubmitGuess.bind(this));
  }

  // Show successful guesses in a list
  showWord(guess) {
  $(".words", this.board).append($("<li>", { text: guess }));
  }

  // Update timer in DOM
  showTimer() {
    $('.timer', this.board).text(this.secs);
  }

  // Set tick to handle seconds passing
  async tick() {
    this.secs -= 1;
    this.showTimer();

    if (this.secs === 0) {
      clearInterval(this.timer)
      await this.endGame();
    }
  }

  // Show a status message
  showMessage(msg, cls) {
    $(".msg")
      .text(msg)
      .removeClass()
      .addClass(`msg ${cls}`);
  }

  // Display score
  updateScore() {
    $('.score').text(this.score)
  }

  // Handle guess submission
  async handleSubmitGuess (evt) {
    evt.preventDefault();

    const $guess = $('.guess', this.board)
    let guess = $guess.val();

    if (!guess) return
    
    if (this.words.has(guess)) {
      this.showMessage(`Already found ${guess}`, "err");
      return;
    }
      
    // Check server for validity
    const resp = await axios.get("/check-guess", { params: { guess:guess }});
    if (resp.data.result === "not-word") {
      this.showMessage(`${guess} is not a valid English word`, "err");
    } else if (resp.data.result === "not-on-board") {
      this.showMessage(`${guess} is not a valid word on this board`,"err");
    } else {
      this.score += guess.length
      this.updateScore()
      this.showWord(guess);
      this.words.add(guess);
      this.showMessage(`Added: ${guess}`, "ok");
      }
      
      $guess.val("").focus();
    }

  // Submit final score to server, update highscore if applicable, and display final score
  async endGame() {
    $('.add-guess', this.board).hide();
    const resp = await axios.post('/end-game', {score: this.score});
    if (resp.data.newRecord) {
      this.showMessage(`Congrats, that's a new record of ${this.score}!`, 'ok');
    } else {
        this.showMessage(`Nice game! Your score was ${this.score}`, 'ok')
      }
  }

}