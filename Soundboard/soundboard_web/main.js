async function main() {
    $.getJSON('./config.json', data => {
        document.title = data.application.title;

        build_song_cards(document.getElementById("music-card"), "music", data.music.songs);
        build_song_cards(document.getElementById("sound-effects-card"), "sound_effects", data.sound_effects.songs);
    })

    load_background();

    await new Promise(r => setTimeout(r, 500));
    document.getElementsByClassName("loading-screen")[0].remove();
}
function build_song_cards(bot_card, bot_identifier, songs) {
    const content = bot_card.querySelector(".card-content");
    const dropdown_content = bot_card.querySelector(".dropdown-content");

    Object.keys(songs).forEach(cat => {
        add_songs_to_dropdown(cat, songs, bot_identifier, dropdown_content, content).click();
    });
}

function add_songs_to_dropdown(songs_key, songs, bot_identifier, dropdown_content, card_content) {
    let el = document.getElementById("dropdown-song-template").cloneNode(true);
    el.id = "";
    el.classList.add("dropdown-item")
    el.querySelector(".dropdown-item-label").innerHTML = songs_key;
    el.querySelector(".button").onclick = () => {
        const song_card = card_content.querySelector(`#${get_songs_card_id(songs_key)}`);
        if(song_card === null) {
            add_songs_to_board(songs_key, songs, bot_identifier, card_content);
            el.querySelector(".dropdown-item-icon").innerHTML = "visibility_off";
        } else {
            remove_songs_from_board(song_card);
            el.querySelector(".dropdown-item-icon").innerHTML = "visibility";
        }
    }

    dropdown_content.appendChild(el)
    
    return el.querySelector(".button");
};

function get_songs_card_id(songs_key) {
    return songs_key.replace(' ', '_').toLowerCase();
}

function add_songs_to_board(songs_key, songs, bot_identifier, content) {
    let song_card = document.getElementById("song-card-template").cloneNode(true);
    song_card.id = get_songs_card_id(songs_key);
    song_card.hidden = false;
    song_card.querySelector(".card-header-title").innerHTML = songs_key;
    song_card.querySelector(".card-header-icon").onclick = () => remove_songs_from_board(song_card);

    Object.keys(songs[songs_key]).forEach(song => {
        let btn = document.createElement("button");
        btn.className = "button"
        btn.innerHTML = song;
        btn.onclick = () => {
            eel.play_song(songs[songs_key][song], bot_identifier);
        };

        song_card.querySelector(".card-content").appendChild(btn);
    })

    content.appendChild(song_card);
}

function remove_songs_from_board(song_card) {
    song_card.remove();
}

function toggle_dropdown(dropdown_id) {
    const dropdown = document.getElementById(dropdown_id);
    const icon = dropdown.querySelector(".material-icons");
    if(dropdown.classList.toggle("is-active")) {
        icon.innerHTML = "expand_less"
    } else {
        icon.innerHTML = "expand_more"
    }
}

function load_background() {
    const img = document.createElement("img");
    img.src = "media/background.jpg ";
    img.hidden = true;

    if (img.complete) {
        color_cards(img);
    } else {
        img.addEventListener('load', () => color_cards(img));
    }
}

function color_cards(img) {
    const colorThief = new ColorThief();
    let mainColor = colorThief.getColor(img);
    let palette = colorThief.getPalette(img);

    let backgroundColor = palette[0];
    let maxContrast = 0;
    for (const color of palette) {
        const contrast = get_contrast(mainColor, color)
        if (contrast > maxContrast) {
            maxContrast = contrast;
            backgroundColor = color
        }
    }

    const textColor = get_contrast(backgroundColor, [0, 0, 0]) >= 4.5 ? [0, 0, 0] : [255, 255, 255]

    for (const element of document.getElementsByClassName("card-header")) {
        element.style.backgroundColor = `rgb(${backgroundColor[0]}, ${backgroundColor[1]}, ${backgroundColor[2]})`;
        element.style.color = `rgb(${textColor[0]}, ${textColor[1]}, ${textColor[2]})`;
        element.querySelector(".card-header-title").style.color = `rgb(${textColor[0]}, ${textColor[1]}, ${textColor[2]})`;
    }
}

/*
Code snippet found there : https://stackoverflow.com/questions/9733288/how-to-programmatically-calculate-the-contrast-ratio-between-two-colors
*/
function luminance(r, g, b) {
    var a = [r, g, b].map(function (v) {
        v /= 255;
        return v <= 0.03928 ?
            v / 12.92 :
            Math.pow((v + 0.055) / 1.055, 2.4);
    });
    return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722;
}

function get_contrast(rgb1, rgb2) {
    var lum1 = luminance(rgb1[0], rgb1[1], rgb1[2]);
    var lum2 = luminance(rgb2[0], rgb2[1], rgb2[2]);
    var brightest = Math.max(lum1, lum2);
    var darkest = Math.min(lum1, lum2);
    return (brightest + 0.05) /
        (darkest + 0.05);
}
