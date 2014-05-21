/*jslint browser: true*/
/*global $, Mustache*/

(function () {
    "use strict";

    function TopicPopupView() {
        this.template = $('#topic-list-template').html();

        this.render = function (view) {
            var rendered = Mustache.render(this.template, view);
            $('#topic-field').after(rendered);
        };

        this.getTopics = function () {
            //TODO: do ajax, fake it for now
            var view = {
                topics: ["topic1", "topic2", "topic3"]
            };
            this.render(view);
        };

        this.filter = function () {
            return null;
        };

        // register event handlers

        // initialise data and render
        this.getTopics();
    }

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
        Mustache.tags = ["[[", "]]"];
        var topicPopupView = new TopicPopupView();

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
