/*jslint browser: true*/
/*global $*/

(function () {
    "use strict";

    $(document).ready(function () {
        function search() {
            $.get(
                'search',
                {"string": $("#search-field").val()},
                function (response) {
                    $("#content").html("");
                    $("#content").append(response);
                }
            );
        }

        $("#search-button").click(search);
        $("#search-field").keypress(function (e) {
            if (e.which === 13) {
                search();
            }
        });
    });
}());
