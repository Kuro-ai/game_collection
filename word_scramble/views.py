from django.shortcuts import render
from django.http import JsonResponse
import random
from django.contrib.auth.decorators import login_required

WORDS = [
    {"word": "python", "definition": "A high-level programming language."},
    {"word": "django", "definition": "A Python framework for web development."},
    {"word": "algorithm", "definition": "A step-by-step procedure to solve a problem."},
    {"word": "function", "definition": "A block of organized, reusable code."},
    {"word": "variable", "definition": "A symbol or name that holds a value."},
    {"word": "iteration", "definition": "The repetition of a process."},
    {"word": "recursion", "definition": "A function that calls itself."},
    {"word": "framework", "definition": "A platform for developing software applications."},
    {"word": "backend", "definition": "The server-side part of an application."},
    {"word": "frontend", "definition": "The client-side part of an application."},
    {"word": "database", "definition": "An organized collection of data."},
    {"word": "template", "definition": "A preset format used as a starting point for something."},
    {"word": "json", "definition": "A lightweight data-interchange format."},
    {"word": "html", "definition": "The standard markup language for documents on the web."},
    {"word": "css", "definition": "A language used to style an HTML document."},
    {"word": "javascript", "definition": "A high-level programming language used in web development."},
    {"word": "bootstrap", "definition": "A popular CSS framework for building responsive web pages."},
    {"word": "react", "definition": "A JavaScript library for building user interfaces."},
    {"word": "angular", "definition": "A TypeScript-based web application framework."},
    {"word": "node", "definition": "A JavaScript runtime built on Chrome's V8 engine."},
    {"word": "flask", "definition": "A lightweight Python web framework."},
    {"word": "array", "definition": "A collection of elements identified by index or key."},
    {"word": "stack", "definition": "A data structure following Last In, First Out (LIFO)."},
    {"word": "queue", "definition": "A data structure following First In, First Out (FIFO)."},
    {"word": "binary", "definition": "A number system using base 2."},
    {"word": "network", "definition": "A group of computers connected for communication."},
    {"word": "encryption", "definition": "The process of converting data into a secure format."},
    {"word": "server", "definition": "A computer or system that provides resources or services."},
    {"word": "client", "definition": "A device or application requesting resources from a server."},
    {"word": "software", "definition": "A set of instructions that tells a computer what to do."},
    {"word": "compiler", "definition": "A program that translates code into machine language."},
    {"word": "syntax", "definition": "The set of rules defining valid structure in a language."},
    {"word": "debugging", "definition": "The process of finding and fixing errors in code."},
    {"word": "testing", "definition": "The process of verifying software functionality."},
    {"word": "docker", "definition": "A tool designed to create, deploy, and run applications."},
    {"word": "kubernetes", "definition": "A system for automating deployment and management of containers."},
    {"word": "api", "definition": "A set of functions allowing interaction with software."},
    {"word": "git", "definition": "A distributed version control system."},
    {"word": "repository", "definition": "A storage location for software projects."},
    {"word": "commit", "definition": "A record of changes made to a repository."},
    {"word": "branch", "definition": "A separate line of development in a repository."},
    {"word": "merge", "definition": "Combining code from different branches in a repository."},
    {"word": "authentication", "definition": "The process of verifying identity."},
    {"word": "authorization", "definition": "The process of granting access to resources."},
    {"word": "session", "definition": "A way to persist user interaction across requests."},
    {"word": "cookie", "definition": "A small piece of data stored on the client side."},
    {"word": "hashing", "definition": "Transforming data into a fixed-length value."},
    {"word": "virtualization", "definition": "Creating virtual versions of physical resources."},
    {"word": "cloud", "definition": "Remote servers used for storage and computation."},
    {"word": "protocol", "definition": "A set of rules for data exchange over a network."},
    {"word": "port", "definition": "A communication endpoint in a computer network."},
    {"word": "firewall", "definition": "A security system that monitors and controls network traffic."},
    {"word": "proxy", "definition": "An intermediary server separating clients from the resources they access."},
    {"word": "cache", "definition": "A hardware or software component storing data for faster access."},
    {"word": "thread", "definition": "The smallest sequence of programmed instructions."},
    {"word": "process", "definition": "An instance of a program running on a computer."},
    {"word": "virtual", "definition": "Not physically existing but created by software."},
    {"word": "kernel", "definition": "The core part of an operating system."},
    {"word": "binary", "definition": "Data represented in base 2 numeral system."},
    {"word": "command", "definition": "An instruction to perform an operation in computing."},
    {"word": "interpreter", "definition": "A program that executes code line by line."},
    {"word": "loop", "definition": "A sequence of instructions repeated until a condition is met."},
    {"word": "script", "definition": "A program executed without the need for compilation."},
    {"word": "container", "definition": "An isolated environment for running applications."},
    {"word": "token", "definition": "A unit of value used in software or authentication systems."},
    {"word": "logic", "definition": "The process of reasoning or inference in programming."},
    {"word": "parsing", "definition": "Analyzing a string of symbols to understand its structure."},
    {"word": "regex", "definition": "A sequence of characters defining a search pattern."},
    {"word": "metadata", "definition": "Data providing information about other data."},
    {"word": "overflow", "definition": "When data exceeds the memory allocated for it."},
    {"word": "pointer", "definition": "A variable storing the memory address of another variable."},
    {"word": "operator", "definition": "A symbol performing an operation in programming."},
    {"word": "event", "definition": "An action recognized by software that triggers a response."},
    {"word": "iterator", "definition": "An object used to iterate through elements in a collection."},
    {"word": "pipeline", "definition": "A series of stages in data processing."},
    {"word": "lambda", "definition": "An anonymous function in programming."},
]

# Function to shuffle a word
def shuffle_word(word):
    scrambled = list(word)
    random.shuffle(scrambled)
    return ''.join(scrambled)

@login_required(login_url='/login/')
def game(request):
    # Shuffle the word list and pick a random word
    random.shuffle(WORDS)  # Shuffle the list
    selected_word = WORDS[0]  # Pick the first word after shuffling
    scrambled_word = shuffle_word(selected_word["word"])
    
    # Store the original word and definition in session
    request.session["original_word"] = selected_word["word"]
    request.session["definition"] = selected_word["definition"]
    request.session["lives"] = 3  # Initialize lives
    
    return render(request, "word_scramble/game.html", {
        "scrambled_word": scrambled_word,
        "lives": request.session["lives"],
    })

def check_answer(request):
    if request.method == "POST":
        user_answer = request.POST.get("answer", "").strip().lower()
        original_word = request.session.get("original_word", "")
        lives = request.session.get("lives", 0)
        is_correct = user_answer == original_word

        if not user_answer:  # Timer timeout case
            lives -= 1
            request.session["lives"] = lives
            return JsonResponse({
                "correct": False,
                "original_word": original_word,
                "lives": lives,
                "game_over": lives <= 0,
            })

        if not is_correct:
            lives -= 1
            request.session["lives"] = lives

        return JsonResponse({
            "correct": is_correct,
            "original_word": original_word,
            "lives": lives,
            "game_over": lives <= 0,
        })

    return JsonResponse({"error": "Invalid request"}, status=400)

def next_word(request):
    random.shuffle(WORDS)
    selected_word = WORDS[0]
    scrambled_word = shuffle_word(selected_word["word"])
    request.session["original_word"] = selected_word["word"]
    request.session["definition"] = selected_word["definition"]
    return JsonResponse({"scrambled_word": scrambled_word})

def show_hint(request):
    # Return the hint (definition) of the word
    definition = request.session.get("definition", "")
    return JsonResponse({"hint": definition})

def restart_game(request):
    # Reset the game session and redirect to the game page
    return JsonResponse({"restart": True})

