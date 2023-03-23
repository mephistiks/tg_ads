async function get_p() {
    let r = await fetch('http://127.0.0.1:8000/api/posts', {
        method: "GET",
        headers: {
            'accept': 'application/json'
        }
    });
    //for (let i = 0; i<2; i++){
    //    console.log(r[i]);
    //}
    let q = await r.json();
    //console.log(r);
    console.log(q);
    //console.log(r.body);
    //console.log(await r.text());
    //console.log(r.body);
    //console.log(q);
    /*
    * for i in q:
    *   var posts = document.getElementById('posts')
        posts.appendChild(add_element(i))
    * */
    //var posts = document.getElementById('posts')
    //posts.appendChild(add_element())
    render_posts(q);
}

async function get_chanels(){
    //тута запрос и заполнение массива loC(здесь cond везде будет const) а ещё удали хуйню в начале list_posts.js
}

async function send_save_changes(data_to_send){
    console.log(data_to_send);
    //здесь отправка данных на сервер
}