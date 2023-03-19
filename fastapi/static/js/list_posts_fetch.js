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
    let posts = document.getElementById('posts');
    for(let i = 0; i < q.length; i++){
        console.log(q[i]);

        posts.innerHTML += "<a href='calendar/"+ q[i][Object.keys(q[i])[0]] + "'><div class='post_in_list'><p>" + q[i][Object.keys(q[i])[1]] + "</p></div></a>";
        ///posts.innerHTML += "<p>" + q[i][Object.keys(q[i])[0]]  + "</p>";
    }
}

async function get_chanels(){
    //тута запрос и заполнение массива loC(здесь cond везде будет const) а ещё удали хуйню в начале list_posts.js
}

async function save_changes(){
    let delete_array = new Array;
    let modify_array = new Array;
    let add_array = new Array;
    for(let i = 0; i < loC.length; i++){
        if(loC[i]["cond"] == "delete")
            delete_array.push(loC[i]["_id"]);
        else if(loC[i]["cond"] == "modify")
            modify_array.push({"_id": loC[i]["_id"], "name": loC[i]["name"], "tg_id": loC[i]["tg_id"], "ref": loC[i]["ref"]});
        else if(loC[i]["cond"] == "add")
            add_array.push({"_id": loC[i]["_id"], "name": loC[i]["name"], "tg_id": loC[i]["tg_id"], "ref": loC[i]["ref"]});
    }
    let data_to_send = {
        "delete": delete_array,
        "modify": modify_array,
        "add": add_array
    };
    console.log(data_to_send);
    //здесь отправка данных на сервер
}