'use strict'
{

const clock = document.getElementById('clock');
const btn = document.getElementById('btn');

// 時間表示
function clockRunner () {
    let time = moment().format('L h:mm:ss');
    clock.innerHTML = time;
    setTimeout(clockRunner, 1000);
}

window.onload = clockRunner();
}