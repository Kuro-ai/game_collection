const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const gameOverMessage = document.getElementById("gameOverMessage");
const restartButton = document.getElementById("restartButton");

const box = 20; // Size of each cell
let snake;
let direction;
let food;
let game;
let score = 0;
function initializeGame() {
    snake = [{ x: 8 * box, y: 8 * box }];
    direction = "RIGHT";
    food = {
        x: Math.floor(Math.random() * 20) * box,
        y: Math.floor(Math.random() * 20) * box,
    };
    score = 0; // Reset score
    document.getElementById("score").textContent = `Score: ${score}`; // Update score display
    gameOverMessage.classList.add("hidden");
    clearInterval(game);
    game = setInterval(draw, 100);
}

document.addEventListener("keydown", changeDirection);
restartButton.addEventListener("click", initializeGame);

function changeDirection(event) {
    const key = event.key.toLowerCase();
    if (key === "w" && direction !== "DOWN") direction = "UP";
    else if (key === "s" && direction !== "UP") direction = "DOWN";
    else if (key === "a" && direction !== "RIGHT") direction = "LEFT";
    else if (key === "d" && direction !== "LEFT") direction = "RIGHT";
}

function draw() {
    ctx.fillStyle = "#000";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < snake.length; i++) {
        ctx.fillStyle = i === 0 ? "#0F0" : "#FFF";
        ctx.fillRect(snake[i].x, snake[i].y, box, box);
    }

    ctx.fillStyle = "red";
    ctx.fillRect(food.x, food.y, box, box);

    let snakeX = snake[0].x;
    let snakeY = snake[0].y;

    if (direction === "UP") snakeY -= box;
    if (direction === "DOWN") snakeY += box;
    if (direction === "LEFT") snakeX -= box;
    if (direction === "RIGHT") snakeX += box;

    if (snakeX === food.x && snakeY === food.y) {
        food = {
            x: Math.floor(Math.random() * 20) * box,
            y: Math.floor(Math.random() * 20) * box,
        };
        score += 10; // Increment score
        document.getElementById("score").textContent = `Score: ${score}`; // Update score display
    } else {
        snake.pop();
    }

    const newHead = { x: snakeX, y: snakeY };

    if (
        snakeX < 0 ||
        snakeY < 0 ||
        snakeX >= canvas.width ||
        snakeY >= canvas.height ||
        collision(newHead, snake)
    ) {
        clearInterval(game);
        gameOverMessage.classList.remove("hidden");
    }

    snake.unshift(newHead);
}
function collision(head, array) {
    return array.some((segment) => head.x === segment.x && head.y === segment.y);
}

// Start the game
initializeGame();
