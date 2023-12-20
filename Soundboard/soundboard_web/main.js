async function main() {
    $.getJSON('./config.json', data => {
        document.title = data.application.title;

        build_sound_cards(document.getElementById("music-card"), "music", data.music.sounds);
        build_sound_cards(document.getElementById("sound-effects-card"), "sound_effects", data.sound_effects.sounds);
    })

    load_background();

    await new Promise(r => setTimeout(r, 500));
    document.getElementsByClassName("loading-screen")[0].remove();
}
function build_sound_cards(bot_card, bot_identifier, sounds) {
    const content = bot_card.querySelector(".card-content");
    const dropdown_content = bot_card.querySelector(".dropdown-content");

    Object.keys(sounds).forEach(cat => {
        add_sounds_to_dropdown(cat, sounds, bot_identifier, dropdown_content, content).click();
    });
}

function add_sounds_to_dropdown(sounds_key, sounds, bot_identifier, dropdown_content, card_content) {
    let el = document.getElementById("dropdown-sound-template").cloneNode(true);
    el.id = "";
    el.classList.add("dropdown-item")
    el.querySelector(".dropdown-item-label").innerHTML = sounds_key;
    el.querySelector(".button").onclick = () => {
        const sound_card = card_content.querySelector(`#${get_sounds_card_id(sounds_key)}`);
        if(sound_card === null) {
            add_sounds_to_board(sounds_key, sounds, bot_identifier, card_content);
            el.querySelector(".dropdown-item-icon").innerHTML = "visibility_off";
        } else {
            remove_sounds_from_board(sound_card);
            el.querySelector(".dropdown-item-icon").innerHTML = "visibility";
        }
    }

    dropdown_content.appendChild(el)
    
    return el.querySelector(".button");
};

function get_sounds_card_id(sounds_key) {
    return sounds_key.replace(' ', '_').toLowerCase();
}

function add_sounds_to_board(sounds_key, sounds, bot_identifier, content) {
    let sound_card = document.getElementById("sound-card-template").cloneNode(true);
    sound_card.id = get_sounds_card_id(sounds_key);
    sound_card.hidden = false;
    sound_card.querySelector(".card-header-title").innerHTML = sounds_key;
    sound_card.querySelector(".card-header-icon").onclick = () => remove_sounds_from_board(sound_card);

    Object.keys(sounds[sounds_key]).forEach(sound => {
        let btn = document.createElement("button");
        btn.className = "button"
        btn.innerHTML = sound;
        btn.onclick = () => {
            eel.play_sound(sounds[sounds_key][sound], bot_identifier);
        };

        sound_card.querySelector(".card-content").appendChild(btn);
    })

    content.appendChild(sound_card);
}

function remove_sounds_from_board(sound_card) {
    sound_card.remove();
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
