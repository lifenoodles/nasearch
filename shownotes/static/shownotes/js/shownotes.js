(function () {
    "use strict"

    $(document).ready(function() {
        function search() {
            alert("lol no");
        }

        $("#search-button").click(search);
        $("#search-field").keypress(function (e) {
            if (e.which === 13) {
                search();
            }
        });
    });
}())
