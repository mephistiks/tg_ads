function send_dt(){
    let date = document.getElementById("date").value;
    let time = document.getElementById("time").value;
    console.log(date);
    console.log(time);
}

async function render_preview(){
    //запрос
    let link_from_html = document.getElementById("tag_for_copy_to_js").innerHTML;
    let post_id = document.getElementById("post_id").innerHTML;
	let link_ = "";
	for(let i = 0, cntr = 0; i < link_from_html.length, cntr < 3; i++){
		if(link_from_html[i] == "/")
			cntr++;
		link_ += link_from_html[i];
	}
	let response = await fetch(link_ + "api/get_post/" + post_id, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json'
		}
	});
	let result = await response.json();
    console.log(result)
    let img = await fetch(link_ + "api/get_img/" + result["img_name"], {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json'
		}
	});
    //console.log()
    result["img"] = await img.json();
    let post = result;
    //let post = {
    //    "img": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAIAAAACUFjqAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAABDSURBVChTtcyxEQAwBIXhlEZQGtEWRlbKu5BjgOTv+I4lIutbcWNmjERU86kZkAdmVqvJqpo8HzS7ezKq1WRU+IgjNjQ7kDFj+9yaAAAAAElFTkSuQmCC",
    //    "post_name": "имя поста",
    //    "post_text": "<s>Вставьте сюда текст</s>\n<u>Вставьте сюда текст</u><b>Вставьте сюда текст</b>",
    //    "buttons": [
    //        [
    //            {"text": "текст1", "link": "https://google.com"},
    //            {"text": "текст2", "link": "https://google.com"}
    //        ],
    //        [
    //            {"text": "текст3", "link": "https://google.com"}
    //        ]
    //    ]
    //}
    document.getElementById('pr_pic').setAttribute('src', post["img"]);
    let text = post["post_text"];
    let ret_text = "";
    for(let i = 0; i < text.length; i++){
        if(text[i] == "\n"){
            ret_text += "<br>"
        }
        else{
            ret_text += text[i];
        }
    }
    document.getElementById('pr_txt').innerHTML = ret_text;
    el = document.getElementById('pr_btns');
    let content = '';
    let buttons_array = post["buttons"];
    for(let i = 0; i < buttons_array.length; i++){
        content += "<div class='buttons_str_pr'>";
        for(let j = 0; j < buttons_array[i].length; j++){
            content += "<a class='pr_link' href='" + buttons_array[i][j]["link"] + "' target='_blank'>";
            content += "<div class='button_pr'><p class='btn_pr_txt'>" + buttons_array[i][j]["text"] + "</p></div></a>";
        }
        content += "</div>";
    }
    el.innerHTML = content;
}