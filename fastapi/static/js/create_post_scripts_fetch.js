async function send_post_post(post_body){
    let host = document.location.origin
    let lnk = document.location.pathname
	let response = await fetch(host + "api/create", {
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