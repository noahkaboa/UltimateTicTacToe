const playerDiv = document.getElementById("player");
const miniSquares = document.querySelectorAll('.mini-square');
const utnText = document.getElementById("utn");
const utnButton = document.getElementById("utn-button");
const moveList = document.getElementById("move-list");
let toMove = "X";
let moveCounter = 0;

playerDiv.innerHTML = "X to move";
utnText.innerHTML = "81 X -1 -1"

// Reset game on reload
window.onload = function() {
    $.ajax({
        url: '/reset',
        type: 'POST',
        async: false,
        success: function(data) {
            console.log("Game reset");
        }
    })
}


miniSquares.forEach(miniSquare => {
  miniSquare.addEventListener('click', () => {
    let [ bigRow, bigCol, smallRow, smallCol ] = miniSquare.id.split("-");
    b = {
        "data": {
            "big_row": bigRow,
            "big_col": bigCol,
            "small_row": smallRow,
            "small_col": smallCol
        }
    }
    var return_data
    $.ajax({
        url: '/play',
        type: 'POST',
        async: false,
        data: JSON.stringify(b),
        success: function(data) {
            return_data = data;
        }
    })
    return_data = JSON.parse(return_data)
    console.log(return_data)
    if (return_data['success']) {
        moveCounter++;
        toMove = toMove === "X" ? "O" : "X";
        miniSquare.innerHTML = return_data['player'];
        miniSquare.classList.add(return_data['player'].toLowerCase());
        if (return_data['wins'] && return_data['wins'] != "Tie"){
            let big_win = document.createElement("div");
            big_win.innerHTML = return_data['player'].toUpperCase();
            big_win.classList.add(return_data['player'].toLowerCase()=="x" ? "x-win" : "o-win");
            const squares = miniSquare.parentElement.children;
            for (const child of squares) {
                child.classList.add("win-blur");
            }
            miniSquare.parentElement.appendChild(big_win);
            
        }
        if (return_data['wins'] == "Tie"){
            let big_win = document.createElement("div");
            const squares = miniSquare.parentElement.children;
            for (const child of squares) {
                child.classList.add("win-blur");
            }
            miniSquare.parentElement.appendChild(big_win);
        }

        // Update HTML
        playerDiv.innerHTML = (return_data['player'].toUpperCase() === "X" ? "O" : "X") + " to move";
        utnText.innerHTML = return_data['utn'];

        let newMove = document.createElement("tr");
        newMove.innerHTML = `<th scope='row'>${moveCounter}</th><td>${return_data['player']}</td></th><td>${bigRow}-${bigCol}-${smallRow}-${smallCol}</td>`;
        moveList.appendChild(newMove);

        for (const move of return_data['valid_moves']) {
            let [ bigRow, bigCol, smallRow, smallCol, possibility ] = move;
            const miniSquare = document.getElementById(`${bigRow}-${bigCol}-${smallRow}-${smallCol}`);
            miniSquare.classList.remove("possible");
            possibility === "possible" && miniSquare.classList.add("possible", toMove.toLowerCase());
        }

        if (return_data["game_over"] === "Tie") {
            alert("It was a tie! GG!")
        }
        if (return_data["game_over"] && return_data["game_over"] != "Tie") {
            alert(`${return_data["game_over"]} won! Congratulations!`)
            miniSquares.forEach(miniSquare => {
                // miniSquare.
            })
        }

    }
  });
  miniSquare.addEventListener('mouseover', () => {
    if ([...miniSquare.classList].includes("possible")) {
        miniSquare.classList.remove("x", "o");
        miniSquare.innerHTML = toMove.toUpperCase();
        miniSquare.classList.add(toMove.toLowerCase());
    }
  });
  miniSquare.addEventListener('mouseout', () => {
    if ([...miniSquare.classList].includes("possible")) {
        miniSquare.innerHTML = "";
        miniSquare.classList.remove("x", "o");
    }
  });
});

utnButton.onclick=async() => {
    var return_data
    console.log(utnText.value)
    $.ajax({
        url: '/set-utn',
        type: 'POST',
        async: false,
        data: {
            utn: utnText.value
        },
        success: function(data) {
            return_data = data;
        }
    })
    return_data = JSON.parse(return_data)
    console.log("Upload Data!")
    console.log(return_data)
    
    miniSquares.forEach(miniSquare => {
        miniSquare.classList.remove("possible");
    });
    for (const move of return_data['valid_moves']) {
        let [ bigRow, bigCol, smallRow, smallCol, possibility ] = move;
        const miniSquare = document.getElementById(`${bigRow}-${bigCol}-${smallRow}-${smallCol}`);
        miniSquare.classList.remove("x", "o", "possible", "win-blur");
        miniSquare.innerHTML = "";
        possibility === "possible" && miniSquare.classList.add("possible", toMove.toLowerCase());
        miniSquare.parentElement.classList.remove("win-blur");
        const win = miniSquare.parentElement.querySelector(".x-win, .o-win");
        win && win.remove();
    }

    expandedUTN = return_data['expanded_utn'].slice(0, 80);

    for (let i = 0; i < 3; i++){
        for (let j = 0; j < 3; j++){
            for (let k = 0; k < 3; k++){
                for (let l = 0; l < 3; l++){
                    const miniSquare = document.getElementById(`${i}-${j}-${k}-${l}`);
                    miniSquare.classList.remove("x", "o");
                    miniSquare.innerHTML = expandedUTN[i+j+k+l] == "_" ? "" : return_data['expanded_utn'][i+j+k+l];
                }
            }
        }
    }

    toMove = return_data['player'].toUpperCase();
    playerDiv.innerHTML = toMove + " to move";
}