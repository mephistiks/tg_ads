function render_posts(q){
    let posts = document.getElementById('posts');
    for(let i = 0; i < q.length; i++){
        console.log(q[i]);

        posts.innerHTML += "<a href='calendar/"+ q[i][Object.keys(q[i])[0]] + "'><div class='post_in_list'><p>" + q[i][Object.keys(q[i])[1]] + "</p></div></a>";
        ///posts.innerHTML += "<p>" + q[i][Object.keys(q[i])[0]]  + "</p>";
    }
}

function renders(){
    get_chanels(); //это короче теперь отсылает к файлу chanels_ws_scripts_fetch.js, так что эту строчку надо будет удалить
    get_p();
}