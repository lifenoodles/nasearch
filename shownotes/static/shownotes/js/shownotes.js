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

        $("#content").on("click", ".shownote-heading-div",
            function () {
                $(this).next().toggle(200);
            });
        $("#content").on("mouseenter", ".shownote-heading-div",
            function () {
                $(this).removeClass("bg-info");
                $(this).addClass("bg-primary");
            });
        $("#content").on("mouseleave", ".shownote-heading-div",
            function () {
                $(this).removeClass("bg-primary");
                $(this).addClass("bg-info");
            });
        $("#search-button").click(search);
        $("#search-field").keypress(function (e) {
            if (e.which === 13) {
                search();
            }
        });
    });
}());
