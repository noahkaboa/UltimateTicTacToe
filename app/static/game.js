miniSquares = document.querySelectorAll('.mini-square');
toMove = "X";

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
        toMove = toMove === "X" ? "O" : "X";
        miniSquare.innerHTML = return_data['player'];
        miniSquare.classList.add(return_data['player'].toLowerCase());
        if (return_data['winner'] != null) {
            alert(return_data['winner'] + " wins!");
        }
        if (return_data['wins']){
            let big_win = document.createElement("div");
            big_win.innerHTML = return_data['player'].toUpperCase();
            big_win.classList.add(return_data['player'].toLowerCase()=="x" ? "x-win" : "o-win");
            const squares = miniSquare.parentElement.children;
            console.log(squares);
            for (const child of squares) {
                console.log(child);
                child.classList.add("win-blur");
            }
            miniSquare.parentElement.appendChild(big_win);
        }

        for (const move of return_data['valid_moves']) {
            let [ bigRow, bigCol, smallRow, smallCol, possibility ] = move;
            const miniSquare = document.getElementById(`${bigRow}-${bigCol}-${smallRow}-${smallCol}`);
            miniSquare.classList.remove("possible");
            possibility === "possible" && miniSquare.classList.add("possible", toMove.toLowerCase());
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