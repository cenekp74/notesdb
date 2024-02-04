var disableanim = false
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
function topnav_drop() {
    var topnav = document.getElementById("topnav");
    var topnav_links = document.getElementById("topnav-links");
    var icon = document.getElementById("icon");
    icon.className = "fa fa-xmark"
    if (topnav.className === "topnav") {
        topnav.className += " responsive";
        disableanim = false;
        animateHeight(0, topnav_links.scrollHeight, topnav_links)
        sleep(320).then(() => {topnav_links.style.height = "auto";});
    } else {
        var icon = document.getElementById("icon");
        icon.className = "fa fa-bars"
        disableanim = true
        topnav_links.style.height = "auto";
        topnav.className = "topnav";
        sleep(320).then(() => {disableanim=false;});
    }
}
function hide_topnav() {
    var topnav = document.getElementById("topnav");
    var topnav_links = document.getElementById("topnav-links");
    var icon = document.getElementById("icon");
    var accountDropdown = document.getElementsByClassName("account-dropdown-content")[0];
    if (accountDropdown) {
        accountDropdown.classList.remove('dropped')
    }
    icon.className = "fa fa-bars"
    disableanim = true
    topnav_links.style.height = "auto";
    topnav.className = "topnav";
    sleep(320).then(() => {disableanim=false;});
}
function animateHeight(start, target, element) {
    var duration = 300;
    var startTime = null;

    function step(timestamp) {
        if (!startTime) startTime = timestamp;
        var progress = timestamp - startTime;
        var percentage = Math.min(progress / duration, 1);

        element.style.height = start + (target - start) * percentage + 'px';

        if (progress < duration) {
            if (disableanim) {
                element.style.height = "auto";
                return;
            }
            requestAnimationFrame(step);
        }
    }
    requestAnimationFrame(step);
}

function setParentDisplayNone(element) {
    element.parentNode.style.display = 'none';
}

function toggleAccountDropdown() {
    element = document.getElementsByClassName('account-dropdown-content')[0];
    element.classList.toggle('dropped');
}

const setTheme = theme => document.documentElement.className = theme;

function getCookie(name) {
    let cookie = {};
    document.cookie.split(';').forEach(function(el) {
      let split = el.split('=');
      cookie[split[0].trim()] = split.slice(1).join("=");
    })
    return cookie[name];
}

function setThemeFromCookie() {
    theme = getCookie('theme')
    if (!theme) {
        setTheme('dark')
        setThemeCookie('dark')
    }
    setTheme(theme)
}

function setThemeCookie(theme) {
    const existingThemeCookie = document.cookie.split('; ').find(cookie => cookie.startsWith('theme='));
    if (existingThemeCookie) {
        document.cookie = document.cookie.replace(/theme=([^;]+)/, `theme=${theme}`);
    } else {
        const cookieString = `theme=${theme}`;
        document.cookie = document.cookie ? `${document.cookie}; ${cookieString}` : cookieString;
    }
}

function changeTheme() {
    checkboxEle = document.querySelector('.theme-checkbox')
    if (checkboxEle.checked) {
        theme = 'dark'
    }
    else {
        theme = 'light'
    }
    setThemeCookie(theme)
    setThemeFromCookie()
}

if (document.querySelector('.theme-checkbox')) {
    if (getCookie('theme') == 'light') {
        document.querySelector('.theme-checkbox').checked = false;
    } else {
        document.querySelector('.theme-checkbox').checked = true;
    }
}

setThemeFromCookie()