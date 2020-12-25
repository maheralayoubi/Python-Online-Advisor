$(function () {
    let $chatwindow = $("#chat-window");
    let $chatwindow1 = $("#chat-window1");
    let username;
    let chatClient;
    let channelName;
    let roomChannel;
    var rooms;
    

    function printMessage(fromUser, message) {
        // if the user is me
        let $message = $('<span class="text-message">').text(message);
        if (fromUser === username) {
            let $messageBox = $('<div class="me">');
            $messageBox.append($message);
            $chatwindow.append($messageBox);
            $chatwindow1.append($messageBox);
            $chatwindow.animate({ scrollTop: $(document).height() }, "slow");
            return false;
        }
        else {
            let $container = $('<div class="conatiner-message">');
            let $sender = $('<span class="name-sender">').text(fromUser);
            let $notMe = $('<div class="not-me">');
            $notMe.append($message);
            $container.append($sender).append($notMe);
            $chatwindow.append($container);
            $chatwindow1.append($container);
            $chatwindow.animate({ scrollTop: $(document).height() }, "slow");
            return false;
        }


    }


    $.getJSON(
        "/token",
        function (data) {
            username = data.username;
            Twilio.Chat.Client.create(data.token).then(client => {
                rooms = document.getElementsByClassName("chatroom");
                chatClient = client;
                
                var timediv;
                for (var i = 0; i < rooms.length; i++) {
                    let anchor = rooms[i].getElementsByClassName("rooms-anchor");
                    let lessonid = anchor[0].getElementsByClassName("id");
                    chatClient.getChannelByUniqueName(lessonid[0].innerHTML).then(function (channel) {

                        //getting time pf last msg
                        channel.getMessages().then(function (messages) {
                            const leng = messages.items.length;
                            var lastmsg = messages.items[leng - 1];
                            var lastmsgTime = lastmsg.timestamp;
                            var jsontime = JSON.stringify(lastmsgTime);
                            var json = JSON.parse(jsontime);
                            var date = new Date(json);
                            dictime = date.getHours() + ":" + date.getMinutes();
                            timediv = document.getElementById(lessonid[0].innerHTML);
                            timediv.innerHTML = dictime;
                        }).catch(function () {
                            console.log("somethig went wrong");
                        });
                    }).catch(function () {
                        console.log("chat hasn't been created yet!")
                    });
                }
                var channels = chatClient.getSubscribedChannels();
                var less;
                for (var i = 0; i < rooms.length; i++) {
                    let anchor = rooms[i].getElementsByClassName("rooms-anchor");
                    let lessonid = anchor[0].getElementsByClassName("id");
                    rooms[i].onclick = function (e) {
                        e.preventDefault();
                        less = lessonid[0].innerHTML;
                        channels.then(JoinChannel(channels, less));
                    }
                }

            });
        }
    )
    function setupChannel(name) {
        if (roomChannel.state.status === 'joined') {
            $chatwindow.html(" ");
            $chatwindow1.html(" ");
            console.log("you have already joined this channel");
            roomChannel.getMessages(25).then(processPage);
        }
        else {
            console.log("First time joinning");
            roomChannel
                .join()
                .then(function (channel) {
                    channel.getMessages(25).then(processPage);
                })
        }

        roomChannel.on("messageAdded", function (message) {
            printMessage(message.author, message.body);
            // send_email(message.author)
        });
    }

    function processPage(page) {
        page.items.forEach(message => {
            printMessage(message.author, message.body);
        });
        if (page.hasNextPage) {
            page.nextPage().then(processPage);
        } else {
            console.log("Done loading messages");

        }
    }
    function JoinChannel(channels, name) {
        channelName = name;
        chatClient
            .getChannelByUniqueName(channelName)
            .then(function (channel) {
                roomChannel = channel;
                setupChannel(channelName);
            })
            .catch(function () {
                console.log('new channel has created');
                chatClient
                    .createChannel({
                        uniqueName: channelName,
                        friendlyName: `${channelName} Chat Channel`
                    })
                    .then(function (channel) {
                        roomChannel = channel;
                        setupChannel(channelName);
                    })
            });
    }
        let $form = $("#message-form");
    let $input = $("#message-input");
    $form.on("submit", function (e) {
        e.preventDefault();
        if (roomChannel && $input.val().trim().length > 0) {
            roomChannel.sendMessage($input.val());
            console.log($input.val());
            $input.val("");
        }
    });

});





// function getCookie(name) {
//     var cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         var cookies = document.cookie.split(';');
//         for (var i = 0; i < cookies.length; i++) {
//             var cookie = cookies[i].trim();

//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
// var csrftoken = getCookie('csrftoken');

// function send_email(author) {
//     var url = 'send_email_for_chat/';

//     fetch(url, {
//         method: 'POST',
//         headers: {
//             'Content-type': 'application/json',
//             'X-CSRFToken': csrftoken,
//         },
//         body: JSON.stringify({ 'author': author })
//     })

// }


