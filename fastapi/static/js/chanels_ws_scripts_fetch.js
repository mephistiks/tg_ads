async function get_chanels(){
    //тута запрос и заполнение массива loC(здесь cond везде будет const) а ещё удали хуйню в начале chanels_ws_scripts.js
    let response = await fetch(host + "/api/send_post/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data_to_send)
    });
    render_chanels_ws();
}

async function send_save_changes(data_to_send){
    console.log(data_to_send);
    //здесь отправка данных на сервер
}