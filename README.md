# DISCORD TTRPG SOUNDBOARD & BOTS
A soundboard to manage music and ambience (from local storage or youtbe) during your discord TTRPG sessions. I have built this tool for my very own purpose so it is a bit shaky but I decided to share it if it can help someone. I know that some built-in or online solutions exist for this but sometimes nothing match exactly your needs so you have to get your hands dirty. You can use this tool as you want, copy it, fork it do as you want. If you do some improvments do no hesitate to share it whith me to ensure everybody can enjoy it. 

## General overview
The tool consists of 2 Discord music bots and a soundboard displayed in a web view. The soundboard allow you to control the music played by the bots throught the interface.

![The soundboard](https://github.com/AurelienDellac/discord-ttrpg-soundboard/assets/33094417/c114ffbe-a0fa-43b5-b62d-e13f9e368f43)


## Installation and configuration
### Technical aspects
The tool consists of 2 Discord music bots and a soundboard displayed in a web view. The soundboard allow you to control the music played by the bots throught the interface. The bots cannot be controlled throught the discord chat except for joining and leaving a voice channel. The idea is to have two bots to manage simulteanously music/ambience and the sound effects. But you can use the two bots in the way you want even just one if you prefer (just kick the other one from the vocal).

The bots are hosted with python and a Lavalink server (version 3.7.8).

### Download

### Bots configuration

### Environment configuration

### Launching

## Use
The tool consists of 2 Discord music bots and a soundboard displayed in a web view. The soundboard allow you to control the music played by the bots throught the interface. The bots cannot be controlled throught the discord chat except for joining and leaving a voice channel.

The idea is to have two bots to manage simulteanously music/ambience and the sound effects. But you can use the two bots in the way you want even just one if you prefer (just kick the other one from the vocal).

When you launch the tool (a combination of batch, jar and python script) it opens a Windows console and a webview. You can minimize the console you will probably have no use for it. The webview contain the soundboard.

![The tool console](https://github.com/AurelienDellac/discord-ttrpg-soundboard/assets/33094417/df596735-2349-4ba0-982f-d1efec75f9db)
![The soundboard](https://github.com/AurelienDellac/discord-ttrpg-soundboard/assets/33094417/c114ffbe-a0fa-43b5-b62d-e13f9e368f43)

The soundboard consists in two main sections corresponding to each bot and the sounds are dispatched in differents sub categories. You can chose which sound each bot plays by clicking on a sound button. The sounds can come from local storage files or youtube links as explain in [the customization section](#customization). Each bot have a a list of commands at the bottom of its body :
- Pause
- Resume
- Stop
- Reset volume to default
- Lower volume
- Increase volume
- Switch on repeat one mode
- Switch off repet one mode

![Bot commands on the soundboard](https://github.com/AurelienDellac/discord-ttrpg-soundboard/assets/33094417/873a97e5-f251-4331-9ecc-6b075ac372c2)

## Customization
### Managing sounds and categories
The sounds are managed through a `config.json` file located in Soundboard/soundboard_web/. There should be a `config.example.json` to start with that you can rename `config.json`. In this file you have two main sections which are `music` and `sound_effects` and each have an inner section named `sounds`. Do not change this labels if you don't want to affect the code. For each bot you have to define at least one category to put the sounds in but you can add as many categories as you want. You will just have to test how it displays to ensure a good utilisation.

To add a sound you have to precise its name (what display on the soundboard button) and its value. The value can be either :
- a local file by precising the tag `{sound_folder}` before the file name and extension. See [environment configuration](#environment-configuration) to configure the local store folder.
- a youtube link by precising the tag `{youtube}` before the video link.


There is an example of my `config.json` file for a Lord of the Rings session using either local files and youtube videos :
```json
"music" : {
    "sounds" : {
        "The Shire" : {
            "Day"                 : "{sound_folder}the-shire.mp3",
            "Night"               : "{sound_folder}the-shire-night.mp3",
            "Northern moors"      : "{sound_folder}windy-nature.mp3",
            "Inn"                 : "{sound_folder}the-shire-tavern.mp3",
            "Suspense"            : "{sound_folder}suspense.mp3"
        },
        "Other ambiences" : {
            "Waiting ambience (the witcher)"    : "{youtube}https://www.youtube.com/watch?v=zAAVbFToD10",
            "Waiting ambience (LOTR)"           : "{youtube}https://www.youtube.com/watch?v=IxQ6sBDoylQ",
            "Fight"                             : "{sound_folder}fight-low-level.mp3"
        }
    }
},
"sound_effects" : {
    "sounds" : {
        "Scenario effects" : {
            "Door knocking"            : "{sound_folder}se-door-knocking.mp3",
            "Dogs"                     : "{sound_folder}se-dogs-angry.mp3",
            "River"                    : "{sound_folder}river.mp3",
            "A Elbereth Gilthoniel"    : "{sound_folder}elbereth-gilthoniel.mp3"
        },
        "General effect" : {
            "Men/Women yelling"     : "{sound_folder}se-men-yelling.mp3",
            "Arrow"                 : "{sound_folder}se-arrow-wood.mp3",
            "Sword on shield"       : "{sound_folder}se-sword-wood.mp3",
            "Sword wound"           : "{sound_folder}se-sword-bloody.mp3",
            "Bloody sword wound"    : "{sound_folder}se-sword-very-bloody.mp3"
        }
    }
}
```


