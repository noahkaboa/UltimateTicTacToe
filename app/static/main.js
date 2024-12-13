miniSquares = document.querySelectorAll('.mini-square');


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
    console.log(return_data["success"])
    if (return_data['success']) {
        miniSquare.innerHTML = return_data['player'];
        miniSquare.classList.add(return_data['player'].toLowerCase());
        if (return_data['winner'] != null) {
            alert(return_data['winner'] + " wins!");
        }
    }
  });
});