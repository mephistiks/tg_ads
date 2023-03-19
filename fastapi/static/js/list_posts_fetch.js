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
    //тута запрос и заполнение массива loC
}

async function save_changes(){
    
}