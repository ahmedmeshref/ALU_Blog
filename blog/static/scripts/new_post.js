// add new post form
document.getElementById("new_post").onsubmit = async function add_post(e) {
    e.preventDefault();
    const title = document.getElementById("title");
    const title_val = title.value;
    const description = document.getElementById("description");
    const description_val = description.value;
    let invalid_title = document.getElementById("invalid_title");
    let invalid_description = document.getElementById("invalid_description");
    let success = true;
    if (title_val.length > 50 || title_val.length < 3) {
        title.className = "form-control is-invalid";
        invalid_title.innerHTML = "title should be between 3 to 50 characters long";
        success = false;
    }
    if (description_val.length > 500 || description_val.length < 10) {
        description.className = "form-control is-invalid";
        invalid_description.innerHTML = "description should be between 10 to 500 characters long";
        success = false;
    }
    if (success) {
        try {
            let response = await fetch("/new_post", {
                                method: "POST",
                                body: JSON.stringify({
                                    'title': title_val,
                                    'description': description_val
                                }),
                                headers: {
                                    'Content-type': 'application/json'
                                }
                            })
            let res_val = await response.json();
            write_post(res_val);
            title.value= null;
            description.value= null;
        } catch (e) {
            console.log(e)
        }
    } else {
        console.log("Error in the title and/or description")
    }
    return;
}


function write_post(res_val) {
    document.getElementById("add_new_posts").innerHTML = `
        <article class="media content-section post_container" id='${res_val["id"]}'>
          <!-- write it as a link, can reach from everywhere, Links, How to make async for other users -->
          <img src='../profile_pics/${res_val["profile_image"]}'
               alt="user_image" class="rounded-circle article-img mt-2">
          <div class="media-body">
              <div class="container article-metadata mb-3">
                  <div class="row mt-1">
                    <div class="col-sm">
                       <a class="mr-2" href='http://127.0.0.1:5000/profile/${res_val["author_id"]}'>
                            ${res_val["username"]}
                       </a>
                       <small class="text-muted">
                            1 seconds ago
                      </small>
                    </div>
                    <div class=".col-sm-">
                        <div class="container">
                          <button class="btn btn-outline-primary border-0 mb-1 mt-0 p-0 font-weight-bold"
                                  data-toggle="dropdown" style="width: 25px">≡</button>
                            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton"> 
                                <a class="btn btn-primary dropdown-item" 
                                href='http://127.0.0.1:5000/post/${res_val["id"]}/update'>
                                    Edit
                                </a>
                                <button class="btn btn-danger dropdown-item" type="submit" onclick="delete_post(${res_val["id"]})">
                                  Delete
                                </button>
                            </div>
                        </div>
                    </div>
                  </div>
              </div>
            <h2>
                <a class="article-title" href='http://127.0.0.1:5000/post/${res_val["id"]}'>
                    ${res_val["title"]}
                </a>
            </h2>
            <p class="article-content text-dark">${res_val["description"]}</p>
          </div>
        </article>`
}

