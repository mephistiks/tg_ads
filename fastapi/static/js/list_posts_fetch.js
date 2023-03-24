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