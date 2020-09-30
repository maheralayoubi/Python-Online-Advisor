$(function () {
  let $messagesTable = $("#MessagesBody");
  let rows = document.getElementsByClassName("Messages");
  let chatClient;


  $.getJSON(
    "/token",
    function (data) {
      username = data.username;
      Twilio.Chat.Client.create(data.token).then(Client => {
        chatClient = Client;
        for (var i = 0; i < rows.length; i++) {
          let ids = rows[i].getElementsByClassName("lessonID");
          let lastMessageTime = rows[i].getElementsByClassName("time");
          let lastMessage = rows[i].getElementsByClassName("message");
          let lastmsg = lastMessage[0].getElementsByClassName("msg");
          
          chatClient.getChannelByUniqueName(ids[0].innerHTML).then(function (channel) {

            
            if (channel.state.status === 'joined') {
              channel.getMessages().then(function (messages) {
                const total = messages.items.length;

                if (total != 0) {
                  const messageObj = messages.items[total - 1];
                  var time = messageObj.timestamp;
                  var jsontime = JSON.stringify(time);
                  var json = JSON.parse(jsontime);

                  var date = new Date(json);
                  var formattedtime = date.getHours() + ":" + date.getMinutes();

                  var message = messageObj.body;
                  lastMessageTime[0].innerHTML = formattedtime;
                  lastmsg[0].innerHTML = message;
                }
              });
            }

            else {
              channel.join().then(function (channel) {
                channel.getMessages().then(function (messages) {
                  const total = messages.items.length;

                  if (total != 0) {
                    const messageObj = messages.items[total - 1];
                    var time = messageObj.timestamp;
                    var jsontime = JSON.stringify(time);
                    var json = JSON.parse(jsontime);

                    var date = new Date(json);
                    var formattedtime = date.getHours() + ":" + date.getMinutes();

                    var message = messageObj.body;
                    lastMessageTime[0].innerHTML = formattedtime;
                    lastMessage[0].innerHTML = message;
                  }
                });
              })
            }


          }).catch(function () {
            console.log("channel not found")
          });

        }
      });

    }
  )
})