$(document).ready(function (){
// declare a parent, sq_one, and sq_two variables from the start
var parent;
var sq_one;
var sq_two;
var block_nullify = false;

function nullify() {
    if (!block_nullify) {
        sq_one = null;
        sq_two = null;
    }
    block_nullify = false;
}

// whenever a square is clicked execute the code
$('.light_square, .dark_square').on("click", function() {
if (parent != undefined && parent.attr("class")=="light_square"){
    parent.css("background-color","WhiteSmoke");
    $(".dot").remove();
} else if (parent != undefined && parent.attr("class")=="dark_square") {
    parent.css("background-color","#966136");
    $(".dot").remove();
}
parent = null;

// get the current square of the item clicked
var cur_square = $(this).attr("id").slice(6,11);

// check if there is a piece at the current square, else empty square clicked
if (document.getElementById("piece" + cur_square)) {
    var piece = document.getElementById("piece" + cur_square);
    var p_col = piece.getAttribute('data-type');
    if (sq_one) {
        if (document.getElementById("piece"+sq_one).getAttribute('data-type') == p_col) {
            sq_one = cur_square;
            parent = $(this);
            get_moves(sq_one, parent);
        } else {
            sq_two = cur_square;
            parent = $(this);
            move_piece(sq_one, sq_two, parent);
            nullify();
        }
    } else {
        sq_one = cur_square;
        parent = $(this);
        get_moves(sq_one, parent);
    }
} else {
    // if sq_one is set, and an empty square is clicked, try to move the piece to the square
    if (sq_one) {
        sq_two = $(this).attr("id").slice(6,11);
        // execute the function to move the piece to the square
        move_piece(sq_one, sq_two, parent);
        nullify();
    }
}

// function to execute when getting the possible moves for a piece
function get_moves(sq_one, parent) {
    parent.css("background-color", "Gold");
    $.ajax({
        contentType: 'application/json;charset=UTF-8',
        type:'POST',
        url:"/moves",
        data:JSON.stringify({'sq_one':sq_one}),
        success: function(response) {
            for (x in response) {
                var id = "square("+response[x]+")";
                document.getElementById(id).innerHTML += ("<span class=\"dot\"></span>");
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            nullify();
            alert('Wrong colour piece selected')
        }
    });
};

// function to execute when moving a piece from square one to square two
function move_piece(sq_one, sq_two, parent) {
    var piece = document.getElementById("piece"+sq_one);
    var src = piece.src;
    if (src.search('pawn') != -1 && (sq_two.slice(3,4) == 8 || sq_two.slice(3,4) == 1)) {
        if (src.search('white') != -1) {
            block_nullify = true;
            $('#wModal').modal('show');
        } else if (src.search('black') != -1) {
            block_nullify = true;
            $('#bModal').modal('show');
        }
    } else {
        $.ajax({
        contentType: 'application/json;charset=UTF-8',
        type:'POST',
        url:"/execute",
        data:JSON.stringify({'sq_one':sq_one, 'sq_two': sq_two}),
        success: function(response) {
            if (!response.error) {
                if (response.castle != null) {
                    var r_one = response.castle[0];
                    var r_two = response.castle[1];
                    var square = document.getElementById("square"+r_two.slice(0,3)+r_two.slice(4,6));
                    var rook = document.getElementById("piece"+r_one.slice(0,3)+r_one.slice(4,6));
                    rook.id = "piece"+r_two.slice(0,3)+r_two.slice(4,6);
                    square.append(rook);
                }
                if (document.getElementById("piece"+sq_two)) {
                    document.getElementById("piece"+sq_two).remove();
                }
                var piece = document.getElementById("piece"+sq_one);
                piece.id = "piece("+sq_two.slice(1,4)+")";
                document.getElementById("square"+sq_two).append(piece);
                for (x in response.empty) {
                    var id = "piece" + response.empty[x].slice(0,3) + response.empty[x].slice(4,6);
                    if (document.getElementById(id)) {
                        document.getElementById(id).remove();
                    }
                }
                if (response.outcome) {
                    setTimeout(function () {
                    $("#"+response.outcome+"Modal").modal('show');
                    }, 500);
                }
            } else {
                alert(response.error);
            }
        }
        });
    }
};
});

// handling promotions
$('.promotion-piece').on("click", function () {
var promotion = $(this).attr('data-type');
var src = $(this).attr('data-img');
$.ajax({
        contentType: 'application/json;charset=UTF-8',
        type:'POST',
        url:"/promote",
        data:JSON.stringify({'sq_one':sq_one, 'sq_two': sq_two, 'promotion':promotion}),
        success: function(response) {
            if (!response) {
                if (document.getElementById("piece"+sq_two)) {
                    document.getElementById("piece"+sq_two).remove()
                }
                var piece = document.getElementById("piece"+sq_one);
                piece.id = "piece("+sq_two.slice(1,4)+")";
                piece.src = src
                document.getElementById("square"+sq_two).append(piece)
                nullify();
                $('.modal').modal('hide')
            } else {
                alert(response)
            }

        }
    });
});
});
