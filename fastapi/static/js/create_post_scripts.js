function button_constr(button_name, button_link){
	return{
		name: button_name,
		link: button_link
	};
}

let buttons_array = new Array;

function txt_flow(){
	let text = document.getElementById('txtar_inp').value;
	let ret_text = "";
	for(let i = 0; i < text.length; i++){
		if(text[i] == "\n"){
			ret_text += "<br>"
		}
		else{
			ret_text += text[i];
		}
	}
	let txt_out = document.getElementById('pr_txt');
	txt_out.innerHTML = ret_text;
}

function te_buttons(tag){
	let text = document.getElementById('txtar_inp').value;
	if(tag == "a"){
		text += "<a href='Вставьте ссылку'>Вставьте текст</a>";
	}
	else{
		text += "<" + tag + ">Вставьте сюда текст</" + tag + ">";
	}
	document.getElementById('txtar_inp').value = text;
	txt_flow();
}

function buttons_ws_rendering(){
	let el = document.getElementById('ws_post_buttons');
	let content = "";
	for(let i = 0; i < buttons_array.length; i++){
		content += "<div class='buttons_str'><label>Строка " + String(i+1) + "</label>";
		content += "<input type='button' name='del_str' value='Удалить строку' id='DelStr" + String(i) + "' onclick='del_str(this.id)'>";
		for(let j = 0; j < buttons_array[i].length; j++){
			content += "<div class = 'button_creator'>";
			content += "<input type='text' name='txt' value='" + buttons_array[i][j].name + "' id='BtnName" + String(i) + String(j) + "' onchange='btn_flow(this.id)'>";
			content += "<input type='text' name='lnk' value='" + buttons_array[i][j].link + "' id='BtnLink" + String(i) + String(j) + "' onchange='btn_flow(this.id)'>";
			content += "<input type='button' name='del_btn' value = 'X' id='DelBtn" + String(i) + String(j) + "' onclick='del_btn(this.id)'></div>";
		}
		if(buttons_array[i].length < 3){
			content += "<input type='button' name='add_btn' value='+' id='AddBtn" + String(i) + "' onclick='add_btn(this.id)'></div>";
		}
	}
	content += "<input type='button' name='add_str' value='Добавить строку' onclick='add_btn_str()'>";
	el.innerHTML = content;

	el = document.getElementById('pr_btns');
	content = '';
	for(let i = 0; i < buttons_array.length; i++){
		content += "<div class='buttons_str_pr'>";
		for(let j = 0; j < buttons_array[i].length; j++){
			content += "<a class='pr_link' href='" + buttons_array[i][j].link + "' target='_blank'>";
			content += "<div class='button_pr'><p class='btn_pr_txt'>" + buttons_array[i][j].name + "</p></div></a>";
		}
		content += "</div>";
	}
	el.innerHTML = content;
}

function add_btn_str(){
	buttons_array.push(new Array(button_constr("текст", "ссылка")));
	buttons_ws_rendering();
}

function add_btn(id_str){
	let id_s = "";
	for(let i = 6; i < id_str.length; i++){
		id_s += id_str[i];
	}
	let id = Number(id_s);
	buttons_array[id].push(button_constr("текст", "ссылка"));
	buttons_ws_rendering();
}

function del_str(id_str){
	let id_s = "";
	for(let i = 6; i < id_str.length; i++){
		id_s += id_str[i];
	}
	let id = Number(id_s);
	buttons_array.splice(id, 1);
	buttons_ws_rendering();
}

function del_btn(id_btn){
	let id_s = "";
	for(let i = 6; i < id_btn.length - 1; i++){
		id_s += id_btn[i];
	}
	let str_n = Number(id_s);
	let btn_n = Number(id_btn[id_btn.length - 1]);
	buttons_array[str_n].splice(btn_n, 1);
	buttons_ws_rendering();
}

function btn_flow(id_btn){
	let el = document.getElementById(id_btn);
	let id_s = "";
	for(let i = 7; i < id_btn.length - 1; i++){
		id_s += id_btn[i];
	}
	let str_n = Number(id_s);
	let btn_n = Number(id_btn[id_btn.length - 1]);
	if(id_btn[3] == "N"){
		buttons_array[str_n][btn_n].name = el.value;
	}
	else{
		if((el.value.substring(0, 8) != "https://") && (el.value.substring(0, 7))){
			buttons_array[str_n][btn_n].link = "https://" + el.value;
		}
		else{
			buttons_array[str_n][btn_n].link = el.value;
		}
	}
	buttons_ws_rendering();
}

function pic_flow() {
	let preview = document.getElementById('pr_pic');
	let file = document.getElementById('picInput').files[0];
	let reader = new FileReader();
	reader.onloadend = function (){
		preview.src = reader.result;
	}
	if(file){
		reader.readAsDataURL(file);
	} 
	else{
		preview.src = "";
	}
}

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
	aTag.textContent = post_text;
	mydiv.appendChild(aTag)

	alert(result);
}