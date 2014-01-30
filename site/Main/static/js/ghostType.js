(function( $ ){
    $.fn.ghostType = function(callback) {

        return this.each(function() {

            var $this = $(this);
            var str = $this.text();
            $this.empty().show();
            str = str.split("");
            str.push("_");

            // increase the delay to ghostType slower
            var delay = 100;

            $.each(str, function (i, val) {
                if (val == "^") {
                    // Do nothing. This will add to the delay.
                }
                else if(val=="!"){
                    $this.append('</br>');
                }
                else {
                    // if(i==str.length-1){
                    //     $this.append('<span>' + val + '</span>');
                    //     $this.children("span").hide().fadeIn(100,function(){
                    //         callback();
                    //     }).delay(delay * i);
                    // }
                    $this.append('<span>' + val + '</span>');
                    $this.children("span").hide().fadeIn(100).delay(delay * i);

                }
            });
            $this.children("span:last").css("textDecoration", "blink");

        });

    };
})( jQuery );