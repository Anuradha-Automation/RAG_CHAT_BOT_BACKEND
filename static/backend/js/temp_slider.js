$(function() {
    var valMap = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0];

    $("#slider").slider({
            max: valMap.length - 1,
            slide: function(event, ui) {
                $("#temperature").val(valMap[ui.value]);
                var fieldNameElement = document.getElementById('radiusAmount');
                fieldNameElement.innerHTML = "Temperature ("+valMap[ui.value]+")";
            }
        })
        .each(function() {

            var opt = $(this).data().uiSlider.options;
            var vals = opt.max - opt.min;
            var arrayLength = valMap.length;
            for (var i = 0; i < arrayLength; i++) {
                var el = $('<label>' + (valMap[i]) + '</label>').css('left', (i / vals * 100) + '%');
                $("#slider").append(el);
            }
        });
let numb = document.getElementById("slider").childNodes[0].style.left = $("#temperature").val()*100+"%";
});


