const test = ['random1', 'random2'];

console.log(test);
var getTodos = function(url, callback){
    const req = new XMLHttpRequest();

    req.addEventListener('readystatechange', function () {
        if(req.readyState === 4 && req.status === 200){
            const data = JSON.parse(req.responseText);
            callback(undefined, data);
        }
        else if(req.readyState === 4){
            
            callback('there has been an error', undefined);
        }
    });

    req.open('POST', url);  // Change to POST if your Flask route uses POST
    
    req.send();
};


var reroute_form = function(path, formdata){
    fetch(path, {
        method: 'POST',
        body: formdata
    })
    .then(response => {
        response.json()
    })
    .then(
        
        data_obj => {
        console.log(data_obj)

        const names1 = (Object.keys(data_obj));

        // data.forEach(element => {
        //   console.log(element)  
        // })
        const list1 = document.querySelector('ul');
        list1.innerHTML = '';

        names1.forEach( name => {
            
            const item = document.createElement('li');
            item.textContent = name;
            list1.appendChild(item);
            
        })
       
    })
    .catch(err => {
        console.log(err);
    })
};

document.getElementById('artist_form').addEventListener('submit', function(event){
    event.preventDefault();
    const formData = new FormData(event.target);

    reroute_form('http://127.0.0.1:5000/form_submit', formData);
    

});


document.getElementById('album_info').addEventListener('click', function(event) {
    console.log('clicked on album info');
    

});



