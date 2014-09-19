/*jslint browser: true*/
/*global $, Mustache*/

(function () {
    "use strict";

    function fuzzyMatch(pattern, text) {
        var pi = 0, ti = 0;
        while (pi < pattern.length && ti < text.length) {
            if (pattern.charAt(pi) === text.charAt(ti)) {
                pi += 1;
            }
            ti += 1;
        }
        if (pi === pattern.length) {
            return true;
        }
        return false;
    }

    function openDropDown() {
        if (!$("#top-input").hasClass("open")) {
            $(".topic-dropdown").dropdown("toggle");
        }
    }

    function TopicPopupView() {
        var self = this;
        self.template = $('#topic-list-template').html();
        self.selectedTemplate =
            $('#topic-selected-template').html();
        self.view = {};
        self.topics = {};

        self.click_unpicked = function (event) {
            var id = self.topics[$(this).attr("data-id")].id;
            $(this).hide();
            $(this).addClass('picked');
            $(".selected-topics").find("#topic" + id).show();
            event.stopPropagation();
        };

        self.click_picked = function (event) {
            var id = self.topics[$(this).attr("data-id")].id;
            $(this).hide();
            $(".topic-suggestions").find("#topic" + id)
                .show().removeClass('picked');
            event.stopPropagation();
        };

        self.render = function () {
            $('#topic-field').after(
                Mustache.render(self.template, self.view)
            );
            $('.selected-topics').append(
                Mustache.render(self.selectedTemplate,
                    {topics: self.view.topics.reverse()})
            );
        };

        self.selectedTopics = function () {
            var topics = [];
            $(".topic-suggestions .picked").each(function () {
                var id = self.topics[$(this).attr("data-id")].id;
                topics.push(id);
            });
            return topics;
        };

        self.getTopics = function () {
            function handleResponse(response) {
                var i, topics = response;

                self.view = {
                    topics: topics
                };

                for (i = 0; i < topics.length; i += 1) {
                    self.topics[topics[i].id] = topics[i];
                }

                self.render();
                $(".topic-suggestions")
                    .find(".topic-suggestion")
                    .click(self.click_unpicked);
                $(".selected-topics")
                    .find(".topic-suggestion")
                    .click(self.click_picked);
            }

            $.get('api/topics', handleResponse);
        };

        self.filterList = function () {
            var visibleCount = 0,
                string = $(this).val().toLowerCase();
            $(".topic-suggestions .topic-suggestion").each(
                function () {
                    var text = $(this).html().toLowerCase();
                    if (!$(this).hasClass('picked')) {
                        if (fuzzyMatch(string, text)) {
                            $(this).show();
                            visibleCount += 1;
                        } else {
                            $(this).hide();
                        }
                    }
                }
            );
            if (visibleCount === 0) {
                $("#no-topics-text").show();
            } else {
                $("#no-topics-text").hide();
            }
        };

        // register event handlers
        $("#topic-field").click(self.filterList);
        $("#topic-field").keyup(self.filterList);

        // initialise data and render
        self.getTopics();
    }

    $(document).ready(function () {
        var page = 0,
            payload = {},
            loadComplete = false,
            topicPopupView = new TopicPopupView();
        Mustache.tags = ["[[", "]]"];

        function handlePageResponse(page, pageCount) {
            $("#load-button").text("Load More");
            $("#search-button").text("Search");
            if (page === pageCount) {
                loadComplete = true;
                $("#load-button").hide();
            } else {
                $("#load-button").show();
            }
        }

        function startSearch() {
            page = 1;
            loadComplete = false;
            $("#search-button").text("Searching...");
        }

        function startLoadingNotes() {
            $("#load-button").show();
            $("#load-button").text("Loading...");
        }

        function nextPage() {
            if (loadComplete) {
                return false;
            }
            startLoadingNotes();
            page += 1;
            payload.page = page;
            $.get('search', payload,
                function (response) {
                    $("#content").append(response.html);
                    handlePageResponse(response.page,
                        response.page_count);
                });
        }

        function search() {
            startSearch();
            startLoadingNotes();
            payload = {"string": $("#search-field").val(),
                "topics": topicPopupView.selectedTopics().join(" "),
                "page": page,
                "min_show": $("#show-from").val(),
                "max_show": $("#show-to").val()};

            $.get('search', payload,
                function (response) {
                    $("#content").html("");
                    $("#content").append(response.html);
                    handlePageResponse(response.page,
                        response.page_count);
                });
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

        $("#topic-field").click(function (e) {
            e.stopPropagation();
            openDropDown();
        });

        $("#topic-field").focusin(function (e) {
            e.stopPropagation();
            openDropDown();
        });

        $("#search-field").keypress(function (e) {
            if (e.which === 13) {
                search();
            }
        });

        $("#load-button").click(function () {
            nextPage();
        });

        $(window).scroll(function () {
            if ($(window).scrollTop() ===
                    $(document).height() - $(window).height()
                    && page > 0) {
                nextPage();
            }
        });
    });
}());
