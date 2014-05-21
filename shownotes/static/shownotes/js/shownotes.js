/*jslint browser: true*/
/*global $*/

(function () {
    "use strict";

    var sample_data = ["string", "test", "data", "string2"];

    function fuzzyMatcher(entries) {
        return function (q, cb) {
            var matches, regex;
            matches = [];
            regex = new RegExp(q, "i");

            /*jslint unparam: true*/
            $.each(entries, function (i, str) {
                if (regex.test(str)) {
                    matches.push({ value: str });
                }
            });

            cb(matches);
        };
    }

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

        $('.typeahead').typeahead({
            minLength: 3,
            highlight: true,
        }, {
            name: 'topic-dataset',
            source: fuzzyMatcher(sample_data)
        });

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
