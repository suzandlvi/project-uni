function insertParam(key, value) {
    key = encodeURIComponent(key);
    value = encodeURIComponent(value);

    // kvp looks like ['key1=value1', 'key2=value2', ...]
    var kvp = document.location.search.substr(1).split('&');
    let i = 0;

    for (; i < kvp.length; i++) {
        if (kvp[i].startsWith(key + '=')) {
            let pair = kvp[i].split('=');
            pair[1] = value;
            kvp[i] = pair.join('=');
            break;
        }
    }

    if (i >= kvp.length) {
        kvp[kvp.length] = [key, value].join('=');
    }

    // can return this or...
    let params = kvp.join('&');

    // reload page with new params
    document.location.search = params;
}

let checkBox = document.getElementById('available-checkbox')
checkBox.addEventListener('input', ev => {
    insertParam(ev.target.name, ev.target.checked)
})

function getUrlVars() {
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for (var i = 0; i < hashes.length; i++) {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}

let checkBoxValue = (getUrlVars()['available-checkbox'] === 'true')
checkBox.checked = checkBoxValue

function resetAllFilters() {
    window.history.replaceState(null, null, window.location.pathname);
    location.reload()
}

function submitSearch() {
    let form = document.querySelector('#search-form')
    form.submit()
}

function goToDetailPage(url) {
    location.href = url
}

/*salam*/