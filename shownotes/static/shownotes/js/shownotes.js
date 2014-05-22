/*jslint browser: true*/
/*global $, Mustache*/

(function () {
    "use strict";

    function TopicPopupView() {
        var self = this;
        self.template = $('#topic-list-template').html();
        self.selectedTemplate = $('#topic-selected-template').html();
        self.view = {};
        self.topics = {};

        self.click_unpicked = function () {
            var text = $(this).html(),
                topic = self.topics[text],
                id = topic.id;
            // topic.on = false;
            $(this).hide();
            $(".selected-topics").find("#topic" + id).toggle();
            console.log($(".selected-topics").find("#topic" + id).length);
        };

        self.click_picked = function () {
            var text = $(this).html(),
                topic = self.topics[text],
                id = topic.id;
            // topic.on = true;
            $(this).hide();
            $(".topic-suggestions").find("#topic" + id).toggle();
        };

        self.render = function () {
            $('#topic-field').after(
                Mustache.render(self.template, self.view)
            );
            $('.selected-topics').append(
                Mustache.render(self.selectedTemplate, self.view)
            );
        };

        self.getTopics = function () {
            var i,
                topics = [
                    {text: "topic1", on: true, id: 1},
                    {text: "topic2", on: true, id: 2},
                    {text: "topic3", on: true, id: 3},
                    {text: "topic4", on: true, id: 4},
                    {text: "topic5", on: true, id: 5}];
            //TODO: do ajax, fake it for now
            self.view = {
                topics: topics
            };

            for (i = 0; i < topics.length; i += 1) {
                self.topics[topics[i].text] = topics[i];
            }
            // self.topics.push.apply(topics);

            // attach event handlers to topic objects
            self.render();
            $(".topic-suggestions").find(".topic-suggestion")
                .click(self.click_unpicked);
            $(".selected-topics").find(".topic-suggestion")
                .click(self.click_picked);
        };

        self.pick = function () {
            return null;
        };

        self.unpick = function () {
            return null;
        };

        // register event handlers

        // initialise data and render
        self.getTopics();
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
