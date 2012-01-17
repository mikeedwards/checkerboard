var Checkerboard = Checkerboard || {};
Checkerboard.Map = function () {
    var map, timeline, eventSource, theme, bandInfos, base,
        markers = [],
        that = {
            load_data: function () {
                var username = $('#userSelect option:selected').attr("value"),
                    station = $('#stationSelect option:selected').attr("value"),
                    inquiry = $('#inquirySelect option:selected').attr("value"),
                    query = {},
                    i = 0;
                if (username !== '') {
                    query.username = username;
                }
                if (station !== '') {
                    query.station = station;
                }
                if (this !== $('#stationSelect')[0] && inquiry !== '') {
                    query.inquiry = inquiry;
                } else {
                    $('#inquirySelect').html('<option value="">--All--</option>');
                }
                $('#messageDisplay').html('<img src="/media/img/loadingAnimation.gif">');
                for (i; i < markers.length; i = i + 1) {
                    markers[i].setMap(null);
                }
                Dajaxice.checkerboard.spotter.request_points('Dajax.process', query);
            },
            initialize: function (base_url) {
                that.loadUI();
                that.loadMap();
                that.loadFilters();
                that.loadTimeline();
                var base = eventSource._getBaseURL(base_url);
            },
            loadUI: function () {
                $('#readDialog').dialog({
                    autoOpen: false,
                    height: 550,
                    width: 550,
                    modal: true,
                    title: "Observation",
                    buttons: {
                        'Blog this!': function () {
                            $('#formDialogTitle').val('');
                            $('#formDialogTags').val('');
                            $('#formDialog').dialog('open');
                            $(this).dialog('close');
                        },
                        Cancel: function () {
                            $(this).dialog('close');
                        }
                    },
                    close: function () {}
                });
                $('#formDialog').dialog({
                    autoOpen: false,
                    height: 550,
                    width: 550,
                    modal: true,
                    title: "Blog this!",
                    buttons: {
                        Done: function () {
                            that.submitBlogPost(this);
                        },
                        Cancel: function () {
                            $(this).dialog('close');
                        }
                    },
                    close: function () {}
                });
                $('#confirmDialog').dialog({
                    autoOpen: false,
                    height: 300,
                    width: 550,
                    modal: true,
                    title: "Thanks!",
                    buttons: {
                        Close: function () {
                            $(this).dialog('close');
                        }
                    },
                    close: function () {}
                });
                $('#read').button().click(function () {
                    $('#readDialog').dialog('open');
                });
            },

            submitBlogPost: function (widget) {
                if ($('#formDialogTitle').val() !== '') {
                    var body = $('#formDialogImageBody').html() + '\n' + $('#formDialogBody').val();
                    body = body.replace(/\n/g, '<br/>');
                    $.post("/checkerboard/upload/blog_post/",
                        {
                            title: $('#formDialogTitle').val(),
                            body: body,
                            tags: $('#formDialogTags').val()
                        },
                        function (data) {
                            base = $('#confirmDialogViewPost').attr("href");
                            $('#confirmDialogViewPost').attr("href", base + data.id);
                            $('#confirmDialog').dialog('open');
                        }
                        );
                    $(widget).dialog('close');
                } else {
                    $('#formDialogTitle').effect("highlight", {}, 3000);
                }
            },

            loadMap: function () {
                var latlng = new google.maps.LatLng(40.73, -73.97),
                    myOptions = {
                        zoom: 8,
                        center: latlng,
                        mapTypeId: google.maps.MapTypeId.ROADMAP
                    };
                map = new google.maps.Map(document.getElementById("map"), myOptions);
            },

            loadFilters: function () {
                $('#userSelect').change(that.load_data);
                $('#stationSelect').change(that.load_data);
                $('#inquirySelect').change(that.load_data);
            },

            loadTimeline: function () {
                var Timeline_ajax_url = "../js/timeline_ajax/simile-ajax-api.js",
                    Timeline_urlPrefix = '../js/timeline_js/';

                eventSource = new Timeline.DefaultEventSource(0);

                theme = Timeline.ClassicTheme.create();

                theme.event.tape.height = 8;
                theme.event.bubble.maxHeight = 240;
                theme.event.bubble.width = 480;
                theme.event.bubble.maxWidth = 600;
                theme.event.overviewTrack.tickHeight = 12;

                that.createBands(new Date());

                timeline = Timeline.create(document.getElementById("tl"), bandInfos, Timeline.HORIZONTAL);

                Timeline.OriginalEventPainter.prototype._showBubble = function (x, y, evt) {
                    that.displayReadDialog(evt);
                };
            },

            draw_points: function (data)
            {
                var center = data.center;
                var bounds = data.bounds;
                var events = data.events;
                var added = false;

                bounds = new google.maps.LatLngBounds(new google.maps.LatLng(bounds[3], bounds[0]), new google.maps.LatLng(bounds[1], bounds[2]));
                map.fitBounds(bounds);
                map.setCenter(new google.maps.LatLng(center.lat, center.lng));

                markers = Array(events.length);
                var windows = Array(events.length);

                var dateTimeFormat = ("dateTimeFormat" in data) ? data.dateTimeFormat : null;
                var parseDateTimeFunction = eventSource._events.getUnit().getParser(dateTimeFormat);
                var last = ("last" in data) ? parseDateTimeFunction(data.last): new Date();

                eventSource.clear();
    
                for (var e = 0; e < events.length; e = e + 1)
                {
                    var event = events[e];
                    // timeline loading
                    var start = parseDateTimeFunction(event.start);
                    var start_date_string = start.toDateString();
                    var evt = new Timeline.DefaultEventSource.Event(
                            {id: ("id" in event) ? event.id : undefined,
                                    start: parseDateTimeFunction(event.start),
                                    end: parseDateTimeFunction(event.end),
                                    latestStart: parseDateTimeFunction(event.latestStart),
                                    earliestEnd: parseDateTimeFunction(event.earliestEnd),
                                    instant: true,
                                    text: event.title,
                                    description: event.description,
                                    image: eventSource._resolveRelativeURL(event.image, base),
                                    link: eventSource._resolveRelativeURL(event.link, base),
                                    icon: eventSource._resolveRelativeURL(event.thumbnail, base),
                                    color: event.color,
                                    textColor: event.textColor,
                                    hoverText: event.hoverText,
                                    classname: event.classname,
                                    tapeImage: event.tapeImage,
                                    tapeRepeat: event.tapeRepeat,
                                    caption: event.caption,
                                    eventID: event.eventID,
                                    trackNum: event.trackNum});
    
                    evt._obj = event;
                    evt.getProperty = function (name) {
                        return this._obj[name];
                    };
    
                    eventSource._events.add(evt);
                    added = true;
    
                    // map loading
                    var thumbnail = event.thumbnail;
                    var position = new google.maps.LatLng(event.lat, event.lng);
                    var title = event.title;
                    var marker = new google.maps.Marker({icon: thumbnail, position: position, map: map, title: title});
                    marker.evt = evt;
                    var window = new google.maps.InfoWindow({position: position});
                    google.maps.event.addListener(marker, 'click', function () {
                        that.displayReadDialog(this.evt);
                    });
                    markers[e] = marker;
                }
    
                if (added) {
                    eventSource._fire("onAddMany", []);
                    that.createBands(last);
                    timeline = Timeline.create(document.getElementById("tl"), bandInfos, Timeline.HORIZONTAL);    
                }
    
    
            },
    
            createBands: function (d)
            {
                bandInfos = [
                    Timeline.createBandInfo({
                        width:          260, 
                        intervalUnit:   Timeline.DateTime.MINUTE,
                        multiple: 15, 
                        intervalPixels: 10,
                        eventSource:    eventSource,
                        date:           d,
                        theme:          theme,
                        eventPainter:   Timeline.OriginalEventPainter
                    }),
                    Timeline.createBandInfo({
                        width:          30, 
                        intervalUnit:   Timeline.DateTime.DAY, 
                        intervalPixels: 150,
                        overview:       true,
                        eventSource:    eventSource,
                        date:           d,
                        theme:          theme
                    }),
                    Timeline.createBandInfo({
                        width:          30, 
                        intervalUnit:   Timeline.DateTime.MONTH,
                        multiple: 1, 
                        intervalPixels: 300,
                        eventSource:    eventSource,
                        overview:       true,
                        date:           d,
                        theme:          theme
                    })
                ];
    
                bandInfos[1].syncWith = 0;
                bandInfos[1].highlight = true;
                bandInfos[2].syncWith = 0;
            },
    
            displayReadDialog: function (clickedEvent)
            {
                var author = clickedEvent.getProperty("author");
                var image = clickedEvent.getProperty("image");
                var caption = clickedEvent.getProperty("caption");
                if (caption === null || typeof(caption) === "undefined") {
                    caption = "";
                }
                var answers = clickedEvent.getProperty("answers");
                var text = clickedEvent.getProperty("text");
                var since = "observed " + clickedEvent.getProperty("since") + " ago...";
                var body = "";  
    
                $('#readDialogAuthor').html(author);
                $('#readDialogSince').html(since);
                $('#readDialogImage img').attr("src", image);
                $('#readDialogCaption').html(caption);
    
                $('#readDialogAnswers dl').html("");
                for (var a = 0; a < answers.length; a = a + 1)
                {
                    $('#readDialogAnswers dl').append("<dt>" + answers[a].question + "</dt>");
                    $('#readDialogAnswers dl').append("<dd>" + answers[a].answer + "</dd>");
                    body += answers[a].question + "\n";
                    body += answers[a].answer + "\n\n";
                }
    
                $('#readDialog').dialog('option', 'title', clickedEvent.getProperty("title"));
                $('#readDialog').dialog('open');
    
                var imageHTML = '<p><img src="' + image + '" mce_src="' + image + '" alt=""/></p>';
    
                $('#formDialogImageBody').html(imageHTML);
                $('#formDialogBody').val(
                        caption + '\n' + author + ' ' + since + '\n' + body + '\n'
                );
            }
        };
    return that;
}();
