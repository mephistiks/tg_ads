async function post_post(){
	let pic_b64 = document.getElementById('pr_pic').src;
	let post_name = document.getElementById('post_name').value;
	let post_text = document.getElementById('txtar_inp').value;
	let post_buttons = new Array;
	for(let i = 0; i < buttons_array.length; i++){
		post_buttons.push(new Array);
		for(let j = 0; j < buttons_array[i].length; j++){
			post_buttons[i].push({"text": buttons_array[i][j].name, "link": buttons_array[i][j].link});
		}
	}
	let post_body = {
		"img": pic_b64,
		"post_name": post_name,
		"post_text": post_text,
		"buttons": post_buttons
	};
	///Добавь в кавычки ссылку на серв
	let link_from_html = document.getElementById("tag_for_copy_to_js").innerHTML;
	let link_ = "";
	for(let i = 0, cntr = 0; i < link_from_html.length, cntr < 3; i++){
		if(link_from_html[i] == "/")
			cntr++;
		link_ += link_from_html[i];
	}
	let response = await fetch(link_ + "api/create", {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(post_body)
	});
	let result = await response.json();

	var mydiv = document.getElementById("new_post");
	var aTag = document.createElement('a');

	aTag.setAttribute('href', link_ + "calendar/" + result)
	aTag.textContent = post_name;
	mydiv.appendChild(aTag)

}
