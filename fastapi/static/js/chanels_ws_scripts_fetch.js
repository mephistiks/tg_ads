async function get_chanels(){
    //тута запрос и заполнение массива loC(здесь cond везде будет const) а ещё удали хуйню в начале chanels_ws_scripts.js
    render_chanels_ws();
}

async function send_save_changes(data_to_send){
    console.log(data_to_send);
    //здесь отправка данных на сервер
}