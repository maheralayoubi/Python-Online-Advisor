// var ti = document.getElementsByClassName("timelesson");
// var lessonhour;
// var lessonMinute;
// var lhourparse;
// var lminuteparse;

// //cuntdown modal
// var beforestartsession = setInterval(function () {
//     for (var i = 0; i < ti.length; i++) {
//         lessonhour = ti[i].innerHTML.slice(13, 16);
//         lessonMinute = ti[i].innerHTML.slice(17, 20);
//         lhourparse = parseInt(lessonhour, 10);
//         lminuteparse = parseInt(lessonMinute, 10);
//         console.log(lminuteparse);

//         var h = lhourparse;
//         var m = lminuteparse;

//         //current time
//         var today = new Date();
//         var hour = today.getHours();
//         console.log(hour);
//         var minute = today.getMinutes();
//         var seconds = today.getSeconds();
//         if (hour == h && minute == m) {
//             $("#myModal").modal("show");
//             // startsession.disabled = true;
//             clearInterval(beforestartsession);
//             if (seconds > 0) {
//                 var sec = 60 - seconds;
//                 countdown(sec);
//             }
//             else if (seconds == 0) {
//                 countdown(60);
//             }

//         }

//     }
//     //lesson time

// }, 1000);

// //rating modal
// var ratingmodal = setInterval(function () {
//     //ending time lesson
//     for (var i = 0; i < ti.length; i++) {
//         lessonhour = ti[i].innerHTML.slice(13, 16);
//         lessonMinute = ti[i].innerHTML.slice(17, 20);
//         lhourparse = parseInt(lessonhour, 10);
//         lminuteparse = parseInt(lessonMinute, 10);


//         var h = lhourparse+1;
//         var min = lminuteparse;
//         var today = new Date();
//         var hour = today.getHours();
//         var minute = today.getMinutes();
//         if (h == hour && min == minute) {
//             $('#rating').modal('show');
//             $('#myModal').modal('hide');

//         }
//     }
// }, 1000);


// function countdown(sec) {
//     var timer = document.getElementById("timer");
//     var counter = 0;
//     var timeleft = sec;
//     var time = convertSeconds(timeleft - counter);
//     timer.innerHTML = convertSeconds(timeleft - counter);
//     var internal = setInterval(function () {
//         counter++;
//         timer.innerHTML = convertSeconds(timeleft - counter);
//         if (counter === timeleft) {
//             clearInterval(internal);
//         }
//     }, 1000);
// }

// function convertSeconds(s) {
//     var min = Math.floor(s / 60);
//     var sec = s % 60;
//     var minformat;
//     var secformat;
//     if (min < 10) {
//         minformat = ("0" + min).slice(-2);
//     }
//     else {
//         minformat = min;
//     }
//     if (sec < 10) {
//         secformat = ("0" + sec).slice(-2);
//     }
//     else {
//         secformat = sec;
//     }
//     return minformat + ":" + secformat;
// }

