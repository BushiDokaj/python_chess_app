$(document).ready(function(){
var parent;
var sq_one;
var sq_two;
$("img.piece").click(function(){
if (parent != undefined && parent.attr("class")=="light_square"){
    parent.css("background-color","WhiteSmoke")
    $(".dot").remove()
} else if (parent != undefined && parent.attr("class")=="dark_square") {
    parent.css("background-color","Sienna")
    $(".dot").remove()
}
parent = $(this).parent();
sq_one = $(this).attr("id").slice(5,10);
parent.css("background-color", "Gold");
$.ajax({
    contentType: 'application/json;charset=UTF-8',
    type:'POST',
    url:"/moves",
    data:JSON.stringify({'sq_one':sq_one}),
    success: function(response) {
        for (x in response) {
            var id = "square("+response[x]+")"
            document.getElementById(id).innerHTML += ("<span class=\"dot\"></span>")
        }
    }
    });
});
$('.light_square, .dark_square').click(function() {
sq_two = $(this).attr("id").slice(6,11);
if (sq_one && sq_two!=sq_one){
    if (parent != undefined && parent.attr("class")=="light_square"){
            parent.css("background-color","WhiteSmoke");
            $(".dot").remove();
    } else if (parent != undefined && parent.attr("class")=="dark_square") {
        parent.css("background-color","Sienna");
        $(".dot").remove();
    }
    var piece = document.getElementById("piece"+sq_one);
    var src = piece.src
    if (src.search('pawn') != -1 && (sq_two.slice(3,4) == 8 || sq_two.slice(3,4) == 1)) {
        if (src.search('white') != -1) {
            $('#wModal').modal('show');
        } else if (src.search('black') != -1) {
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
                    var r_one = response.castle[0]
                    var r_two = response.castle[1]
                    var square = document.getElementById("square"+r_two.slice(0,3)+r_two.slice(4,6));
                    var rook = document.getElementById("piece"+r_one.slice(0,3)+r_one.slice(4,6));
                    rook.id = "piece"+r_two.slice(0,3)+r_two.slice(4,6);
                    square.append(rook);
                }
                if (document.getElementById("piece"+sq_two)) {
                    document.getElementById("piece"+sq_two).remove()
                }
                var piece = document.getElementById("piece"+sq_one);
                piece.id = "piece("+sq_two.slice(1,4)+")";
                document.getElementById("square"+sq_two).append(piece)
                for (x in response.empty) {
                    var id = "piece" + response.empty[x].slice(0,3) + response.empty[x].slice(4,6);
                    if (document.getElementById(id)) {
                        document.getElementById(id).remove();
                    }
                }
                sq_one = null
            } else {
                sq_one = null
                alert(response.error)
            }
        }
        });
    }
}
});
$('.promotion-piece').click(function () {
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
            } else {
                alert(response)
            }

        }
});
});
});