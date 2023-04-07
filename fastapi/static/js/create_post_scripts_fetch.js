async function send_media(file){
	let host = document.location.origin;
	let response = await fetch(host + "/api/v2/upload", {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			"file": file
		})
	});
	let result = await response.text();
	return result;
}

async function send_post_post(post_body){
    let host = document.location.origin;
	let response = await fetch(host + "/api/create", {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(post_body)
	});
	let result = await response.json();

	var mydiv = document.getElementById("new_post");

	mydiv.innerHTML = "<a href = " + host + "/calendar/" + result + "> "+post_body["post_name"]+"</a>";

}