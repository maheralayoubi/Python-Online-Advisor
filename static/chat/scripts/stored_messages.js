$(function () {
    let $chat_window = $("#chat-window");
    let chatClient;
    let channelId = window.location.pathname.split("/")[2];

    function addMessage(message, author){
        let $message = $('<span class"text-message">').text(message);
        let $user = $('<span class="name-sender">').text(author);

        let $container = $('<div class="conatiner-message">');
        let $messagecontainer = $('<div class="not-me">');
        $messagecontainer.append($message);
        $container.append($user);
        $container.append($messagecontainer);

        $chat_window.append($container);

        $chat_window.animate({ scrollTop: $(document).height() }, "slow");
        return false;
    }
    $.getJSON(
        "/token",
        function (data) {
            username = data.username;
            console.log(username);
            Twilio.Chat.Client.create(data.token).then(Client => {
                chatClient = Client;

                chatClient.getChannelByUniqueName(channelId).then(function(channel){
                    if(channel.state.status === 'joined'){
                        channel.getMessages().then(function(messages){
                            const length = messages.items.length;
                            console.log(length);
                            for(var i=0; i<length; i++){
                                const messageObj = messages.items[i];
                                var author = messageObj.author;
                                var message = messageObj.body;
                                addMessage(message, author);
                                console.log(message);
                                console.log(author);
                            }
                        })
                    }

                    else{
                        channel.join().then(function(cjannel){
                            channel.getMessages().then(function(messages){
                                const length = messages.items.length;
                                for(var i=0; i<length; i++){
                                    const messageObj = messages.items[i];
    
                                    var message = messageObj.body;
                                    console.log(message);
                                }
                            })
                        })
                    }
                }).catch(function(){
                    console.log("No channel has been found");
                    let $msg = $('<span class="NOTE">') .text("表示するメッセージはありません");
                    $chat_window.append($msg);
                })
            })

        }
    )
})