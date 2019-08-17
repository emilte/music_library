# imports
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core import management
from songs.models import *
import json
import datetime
import os
from halo import *
# End: imports -----------------------------------------------------------------


songs = {
    #'Title': {'artist': 'xxx', 'bpm': xxx, 'tags': ['name'], 'spotify_URL': 'xxx', 'spotify_URI': 'xxx'},
    'Maniac': {'artist': 'Michael Sembello', 'bpm': 80, 'tags': ['repetetiv', 'gåtur'], 'spotify_URL': 'https://open.spotify.com/track/1xPSDf8z4dH46gkvlLtvDO?si=-uU2X3vLRoOcGV9MjTvfVw', 'spotify_URI': 'spotify:track:1xPSDf8z4dH46gkvlLtvDO'},
    'King of The Road': {'artist': 'Roger Miller', 'bpm': 61, 'tags': ['breaks'], 'spotify_URL': 'https://open.spotify.com/track/2fxZpmpqDNKVRC2zYbdT6e?si=X1iEeLtxRIWeqw70VHsv8A', 'spotify_URI': 'spotify:track:2fxZpmpqDNKVRC2zYbdT6e'},
    'Crazy Little Thing Called Love': {'artist': 'Queen', 'bpm': 77, 'tags': ['breaks'],'spotify_URL': 'https://open.spotify.com/track/68Xvr6rd9xrVqJItrmn7o4?si=XxyYeSpNSW-8py5teYeimw', 'spotify_URI': 'spotify:track:68Xvr6rd9xrVqJItrmn7o4'},
    'Fine Brown Frame': {'artist': 'Dianne Reeves, Lou Rawls', 'bpm': 64, 'tags': ['twist'], 'spotify_URL': 'https://open.spotify.com/track/529bZN7XbpbDog5xQqC3wA?si=P8P6ie7qTPOdW6Noq8Baew', 'spotify_URI': 'spotify:track:529bZN7XbpbDog5xQqC3wA'},
    'Sultans Of Swing': {'artist': 'Dire Straits', 'bpm': 74, 'tags': [], 'spotify_URL': 'https://open.spotify.com/track/6AUYnTv5LXbWm2oHxN3QAw?si=2t00RGfBQyaETWY2JvUhUA', 'spotify_URI': 'spotify:track:6AUYnTv5LXbWm2oHxN3QAw'},
    'Vem vet': {'artist': 'Lisa Ekdahl', 'bpm': 63, 'tags': ['breaks', 'koselig'], 'spotify_URL': 'https://open.spotify.com/track/05n1T8JesqkZPIzWu7k7uF?si=tJB_zaZkQv28gwW1RlvIPA', 'spotify_URI': 'spotify:track:05n1T8JesqkZPIzWu7k7uF'},
    'Benen i kors': {'artist': 'Lisa Ekdahl', 'bpm': 70, 'tags': ['breaks', 'styling', 'koselig'], 'spotify_URL': 'https://open.spotify.com/track/2IwHUPvJEvFJoSSLsMRe7k?si=A7VBnIXbQN-k15EMzcE0JQ', 'spotify_URI': 'spotify:track:2IwHUPvJEvFJoSSLsMRe7k'},
    "I'm A Believer": {'artist': 'The Monkees', 'bpm': 80, 'tags': ['breaks'], 'spotify_URL': 'https://open.spotify.com/track/5RKZ9zCtLjBLTea7qkSFqr?si=y7DLxcB5QfCTk5tn-BcA3Q', 'spotify_URI': 'spotify:track:5RKZ9zCtLjBLTea7qkSFqr'},
    'Sixteen Tons': {'artist': 'Tennessee Ernie Ford', 'bpm': 72, 'tags': ['breaks'], 'spotify_URL': 'https://open.spotify.com/track/6Bqq92HMn3Cf9wkr9XXTew?si=gfJNu1AOQBWsb75yh9ZQTw', 'spotify_URI': 'spotify:track:6Bqq92HMn3Cf9wkr9XXTew'},
    'Wake Me Up Before You Go-Go': {'artist': 'Wham!', 'bpm': 81, 'tags': ['hopp'], 'spotify_URL': 'https://open.spotify.com/track/6ZEAXknmx2mrO3KgcDNpFI?si=JbbcAIxjSQOZaBwbBKzeZA', 'spotify_URI': 'spotify:track:6ZEAXknmx2mrO3KgcDNpFI'},
    'Stiches': {'artist': 'Shawn Mendes', 'bpm': 75, 'tags': ['pop', 'koselig'], 'spotify_URL': 'https://open.spotify.com/track/1WP1r7fuvRqZRnUaTi2I1Q?si=qKD5ChgNQ6mE381Swkb1ow', 'spotify_URI': 'spotify:track:1WP1r7fuvRqZRnUaTi2I1Q'},
    'Dance With Me Tonight': {'artist': 'Olly Murs', 'bpm': 82, 'tags': ['styling'], 'spotify_URL': 'https://open.spotify.com/track/1FSWSs9CL01RCYxXtm08Rf?si=o1_IT5usR5mA8xDzHZ51vA', 'spotify_URI': 'spotify:track:1FSWSs9CL01RCYxXtm08Rf'},
    'You Can Never Tell': {'artist': 'Chuck Berry', 'bpm': 79, 'tags': [], 'spotify_URL': 'https://open.spotify.com/track/7xcFTtcCiyRvqLLq8s61WF?si=Z189u2qYT2OyysAkh_19cA', 'spotify_URI': 'spotify:track:7xcFTtcCiyRvqLLq8s61WF'},
    'Candyman': {'artist': 'Christina Aguilera', 'bpm': 86, 'tags': ['pop', 'høy energi', 'styling'], 'spotify_URL': 'https://open.spotify.com/track/5lUTzPuiloBHm1qEaJcJfF?si=zISTO-jFTqO0aKY-JXvm_w', 'spotify_URI': 'spotify:track:5lUTzPuiloBHm1qEaJcJfF'},
    "I'd Rather Dance With You": {'artist': 'Kings of Convenience', 'bpm': 71, 'tags': ['koselig'], 'spotify_URL': 'https://open.spotify.com/track/1ZcxNiJtXf4pHMcNjwn3Rc?si=YaaSd09AQEm51A3RzleVJg', 'spotify_URI': 'spotify:track:1ZcxNiJtXf4pHMcNjwn3Rc'},
    'Footloose': {'artist': 'Kenny Loggins', 'bpm': 87, 'tags': ['hopp'], 'spotify_URL': 'https://open.spotify.com/track/4YR6Dextuoc3I8nJ0XgzKI?si=_yTVV8PXTmC_fNeYsazsYg', 'spotify_URI': 'spotify:track:4YR6Dextuoc3I8nJ0XgzKI'},
    'Dear Future Husband': {'artist': 'Meghan Trainor', 'bpm': 80, 'tags': ['styling', 'twist', 'pop'], 'spotify_URL': 'https://open.spotify.com/track/3cU2wBxuV6nFiuf6PJZNlC?si=JC4gfxhFSB-x7YVl-Pg-1A', 'spotify_URI': 'spotify:track:3cU2wBxuV6nFiuf6PJZNlC'},
    'There She Goes': {'artist': "The La's", 'bpm': 62, 'tags': ['lav energi', 'koselig', 'rollebytte'], 'spotify_URL': 'https://open.spotify.com/track/4c6vZqYHFur11FbWATIJ9P?si=Dd0QXn_STO2tJlD2T0ds-g', 'spotify_URI': 'spotify:track:4c6vZqYHFur11FbWATIJ9P'},
    "Come On, Let's Go": {'artist': 'Dion', 'bpm': 77, 'tags': ['breaks'], 'spotify_URL': 'https://open.spotify.com/track/4OmNaLOHfudiXxcWOsXPt1?si=sqKeInBvTcy29Uyf5ZQFuw', 'spotify_URI': 'spotify:track:4OmNaLOHfudiXxcWOsXPt1'},
    'All American': {'artist': 'Nick Carter', 'bpm': 63, 'tags': ['pop'], 'spotify_URL': 'https://open.spotify.com/track/3AOlEh1oZX6iFd2qnzfs0v?si=avIjwS1JSbC5kHe8GS_Q4A', 'spotify_URI': 'spotify:track:3AOlEh1oZX6iFd2qnzfs0v'},
    'Sway': {'artist': 'Michael Bublé', 'bpm': 63, 'tags': ['breaks', 'styling', 'spin'], 'spotify_URL': 'https://open.spotify.com/track/2ajUl8lBLAXOXNpG4NEPMz?si=KrnHG4TQR2SHjqqBvv7EOw', 'spotify_URI': 'spotify:track:2ajUl8lBLAXOXNpG4NEPMz'},
    "I'm So Excited": {'artist': 'The Pointer Sisters', 'bpm': 92, 'tags': ['hopp'], 'spotify_URL': 'https://open.spotify.com/track/2u8MGAiS2hBVE7GZzTZLQI?si=tp_E2gctT1-9nwtrO7Csvg', 'spotify_URI': 'spotify:track:2u8MGAiS2hBVE7GZzTZLQI'},
    'Bongo Bong': {'artist': 'Robbie Williams', 'bpm': 75, 'tags': ['vanskelig takt'], 'spotify_URL': 'https://open.spotify.com/track/0NlT1OFrZVQ3ZJUzZljPgr?si=boAbLTCZT22mhQBstDhBjQ', 'spotify_URI': 'spotify:track:2u8MGAiS2hBVE7GZzTZLQI'},
    'Let It Roll Again': {'artist': 'Big Bad Voodoo Daddy', 'bpm': 65, 'tags': [], 'spotify_URL': 'https://open.spotify.com/track/6u6kTDvYPifO052iuNHmBU?si=ecR2cxMRTuec6oOgBhd3DQ', 'spotify_URI': 'spotify:track:6u6kTDvYPifO052iuNHmBU'},
    "That Don't Impress Me Much": {'artist': 'Shania Twain', 'bpm': 63, 'tags': ['høy energi', 'pop'], 'spotify_URL': 'https://open.spotify.com/track/3acriFyHOVFW8heimUC0IW?si=aFFLsnklTSek5sCCM9lxwg', 'spotify_URI': 'spotify:track:3acriFyHOVFW8heimUC0IW'},
    'Shut Up and Dance': {'artist': 'WALK THE MOON', 'bpm': 64, 'tags': ['pop'], 'spotify_URL': 'https://open.spotify.com/track/4kbj5MwxO1bq9wjT5g9HaA?si=_zdM1FLtQEWPfieInC9HaA', 'spotify_URI': 'spotify:track:4kbj5MwxO1bq9wjT5g9HaA'},
    'Cake By The Ocean': {'artist': 'DNCE', 'bpm': 60, 'tags': [], 'spotify_URL': 'https://open.spotify.com/track/7L5jgZtAyfiU7elB8DIqCx?si=-AUTWyw0SQu6_FA4bss3Lg', 'spotify_URI': 'spotify:track:7L5jgZtAyfiU7elB8DIqCx'},
    'Toxic': {'artist': 'Britney Spears', 'bpm': 72, 'tags': ['dukketur', 'pop'], 'spotify_URL': 'https://open.spotify.com/track/2cPJpyurXxJAZHFNSFcWCr?si=c7yLZsr0QB66z8XYIax5Dw', 'spotify_URI': 'spotify:track:2cPJpyurXxJAZHFNSFcWCr'},
    "I'm Gonna Be (500 Miles)": {'artist': 'The Proclaimers', 'bpm': 66, 'tags': ['gåtur'], 'spotify_URL': 'https://open.spotify.com/track/66S14BkJDxgkYxLl5DCqOz?si=wIXCWSxOR3aERGN3ppyp0Q', 'spotify_URI': 'spotify:track:66S14BkJDxgkYxLl5DCqOz'},
    'Get My Name': {'artist': 'Mark Ballas', 'bpm': 61, 'tags': ['styling'], 'spotify_URL': 'https://open.spotify.com/track/5tfJjJ5MbahIA5TDV7DJk5?si=wYgKcljoRBaNJIQ_IiHlyw', 'spotify_URI': 'spotify:track:5tfJjJ5MbahIA5TDV7DJk5'},
    'Little Bitty Pretty One': {'artist': 'Billy Gilman', 'bpm': 87, 'tags': [], 'spotify_URL': 'https://open.spotify.com/track/5V9ezTbv9LhSpgDcGph2n3?si=eqcIWcuaQ6eNX7HI0nwCjw', 'spotify_URI': 'spotify:track:5V9ezTbv9LhSpgDcGph2n3'},
    'Blue Moon': {'artist': 'The Marcels', 'bpm': 64, 'tags': ['vanskelig takt'], 'spotify_URL': 'https://open.spotify.com/track/39hE7MMHFjYsqv7zwhR6LD?si=_QCFt48BTbidy-k0xEZG4Q', 'spotify_URI': 'spotify:track:39hE7MMHFjYsqv7zwhR6LD'},
    "It's About That Walk": {'artist': 'Prince', 'bpm': 65, 'tags': ['styling', 'breaks', 'gåtur'], 'spotify_URL': 'https://open.spotify.com/track/1pI0UV8zAolSGiAJljPKJe?si=SyHMqeoaRaqfzgLlEGmaBg', 'spotify_URI': 'spotify:track:1pI0UV8zAolSGiAJljPKJe'},
    "Don't Stop The Music": {'artist': 'Rihanna', 'bpm': 61, 'tags': ['pop'], 'spotify_URL': 'https://open.spotify.com/track/0ByMNEPAPpOR5H69DVrTNy?si=-eubGEcpTKW41y9d0-RRsQ', 'spotify_URI': 'spotify:track:0ByMNEPAPpOR5H69DVrTNy'},
    'Katchi': {'artist': 'Ofenbach, Nick Waterhouse', 'bpm': 63, 'tags': [], 'spotify_URL': 'https://open.spotify.com/track/2NF8A7C6tICScdRaZ0BrEe?si=xhumYqc1RJeKPUuWXaWuzQ', 'spotify_URI': 'spotify:track:2NF8A7C6tICScdRaZ0BrEe'},
    'Elektrisk': {'artist': 'Marcus & Martinus, Katastrofe', 'bpm': 64, 'tags': ['styling', 'pop', 'høy energi'], 'spotify_URL': 'https://open.spotify.com/track/2q83iIfEGIk8kyrdT4uYOG?si=MoSh5HqpRseMkf3Ri3to6A', 'spotify_URI': 'spotify:track:2q83iIfEGIk8kyrdT4uYOG'},
    "Haven't Met You Yet": {'artist': 'Michael Bublé', 'bpm': 61, 'tags': ['koselig'], 'spotify_URL': 'https://open.spotify.com/track/4iMdiQO0YJwEkWf8eI2wff?si=ASedfnRxTquGdmywTq7vkg', 'spotify_URI': 'spotify:track:4iMdiQO0YJwEkWf8eI2wff'},
    "Ex's & Oh's": {'artist': 'Elle King', 'bpm': 70, 'tags': [], 'spotify_URL': 'https://open.spotify.com/track/70eDxAyAraNTiD6lx2ZEnH?si=dGsBwkPSSS-hTTkVviWAJw', 'spotify_URI': 'spotify:track:70eDxAyAraNTiD6lx2ZEnH'},
    'Super Freak': {'artist': 'Rick James', 'bpm': 66, 'tags': ['høy energi'], 'spotify_URL': 'https://open.spotify.com/track/55OjNE2lCUX19YsiwjmtYX?si=GEUKjUj_TgqGUdL6lGujkw', 'spotify_URI': 'spotify:track:55OjNE2lCUX19YsiwjmtYX'},
    'Girls': {'artist': 'Marcus & Martinus, Madcon', 'bpm': 59, 'tags': ['høy energi', 'pop'], 'spotify_URL': 'https://open.spotify.com/track/4Y8s3kA6vx4y51T79sNVOs?si=cQAL7vfTS8m0fAyks3zG8g', 'spotify_URI': 'spotify:track:4Y8s3kA6vx4y51T79sNVOs'},
    'Light It Up': {'artist': 'Marcus & Martinus, Samantha J', 'bpm': 64, 'tags': ['pop', 'høy energi'], 'spotify_URL': 'https://open.spotify.com/track/6trXE7m15i4OFFxzApXSzQ?si=jFXTolBRT1Olq4ZjllR6Hw', 'spotify_URI': 'spotify:track:6trXE7m15i4OFFxzApXSzQ'},
    'Doctor Jones': {'artist': 'Aqua', 'bpm': 70, 'tags': ['pop'], 'spotify_URL': 'https://open.spotify.com/track/6EBDmMZBQkWrj7jWlGhFU1?si=EeBFbgneQBOjtJoTQPqhjw', 'spotify_URI': 'spotify:track:6EBDmMZBQkWrj7jWlGhFU1'},
    'Drømmedame': {'artist': 'Trang Fødsel', 'bpm': 61, 'tags': ['spin'], 'spotify_URL': 'https://open.spotify.com/track/0jXg3CVnHrd2m7U8bNdDdH?si=rUBmApuqRVe4i9F28RgydA', 'spotify_URI': 'spotify:track:0jXg3CVnHrd2m7U8bNdDdH'},
    'I kjempeform': {'artist': 'Ole Ivars', 'bpm': 84, 'tags': ['breaks'], 'spotify_URL': 'https://open.spotify.com/track/59UHxS8ougjFTNKRpdNvCL?si=caQaoAtzSpe44N_3l0w1lA', 'spotify_URI': 'spotify:track:59UHxS8ougjFTNKRpdNvCL'},
    'Big Time Operator': {'artist': 'Big Bad Voodoo Daddy', 'bpm': 84, 'tags': ['styling'], 'spotify_URL': 'https://open.spotify.com/track/4G59PDOr2U13ztLwIpiH5W?si=tDWXkoqYQOac17Udj0KGmw', 'spotify_URI': 'spotify:track:4G59PDOr2U13ztLwIpiH5W'},
    'Everything': {'artist': 'Michael Bublé', 'bpm': 61, 'tags': ['koselig'], 'spotify_URL': 'https://open.spotify.com/track/4T6HLdP6OcAtqC6tGnQelG?si=Dv0wrEoDT0GrQyqg8Zu1aA', 'spotify_URI': 'spotify:track:4T6HLdP6OcAtqC6tGnQelG'},
    'Baby Likes To Rock It': {'artist': 'The Tractors', 'bpm': 80, 'tags': [], 'spotify_URL': 'https://open.spotify.com/track/2kQtKFkPMdL5Jf7xk4T9SI?si=w_tlq_jKQ2yWe-67AB7kjg', 'spotify_URI': 'spotify:track:2kQtKFkPMdL5Jf7xk4T9SI'},
    'You Make My Dreams': {'artist': 'Darys Hall, John Oates', 'bpm': 83, 'tags': [], 'spotify_URL': 'https://open.spotify.com/track/4o6BgsqLIBViaGVbx5rbRk?si=A-SbAfobSFawD1n5qISRIw', 'spotify_URI': 'spotify:track:4o6BgsqLIBViaGVbx5rbRk'},
    'A Letter To You': {'artist': "Shakin' Stevens", 'bpm': 68, 'tags': [], 'spotify_URL': 'https://open.spotify.com/track/1DpHd44nRoTFljl7mYbc7J?si=FuHGeH7rTEyIuSjg816Idw', 'spotify_URI': 'spotify:track:1DpHd44nRoTFljl7mYbc7J'},
    'Three Cool Cats': {'artist': 'Jump4joy', 'bpm': 71, 'tags': ['breaks'], 'spotify_URL': 'https://open.spotify.com/track/1GS487k2zxOfqYMy65j6Uh?si=ws9Vj4fTSz-9qAyCFVOvVQ', 'spotify_URI': 'spotify:track:1GS487k2zxOfqYMy65j6Uh'},
    'Jailhouse Rock': {'artist': 'Elvis Presley', 'bpm': 83, 'tags': [], 'spotify_URL': 'https://open.spotify.com/track/4gphxUgq0JSFv2BCLhNDiE?si=D4yn4HS_RQCakhsYHKjx3A', 'spotify_URI': 'spotify:track:4gphxUgq0JSFv2BCLhNDiE'},
    'The Boy Does Nothing': {'artist': 'Alesha Dixon', 'bpm': 87, 'tags': [], 'spotify_URL': 'https://open.spotify.com/track/522GGnq0ZikjsxbiKFLy3D?si=hTzenwCORVa1sM7CiyDMJA', 'spotify_URI': 'spotify:track:522GGnq0ZikjsxbiKFLy3D'},
    'All Shook Up': {'artist': 'Elvis Presley', 'bpm': 75, 'tags': ['breaks'], 'spotify_URL': 'https://open.spotify.com/track/5ueyLj6e6oVaTY0KQ6yLaA?si=99rq0jEvTCKAYdKn4njGiQ', 'spotify_URI': 'spotify:track:5ueyLj6e6oVaTY0KQ6yLaA'},
    'La det swinge': {'artist': 'Bobbysocks', 'bpm': 69, 'tags': ['høy energi'], 'spotify_URL': 'https://open.spotify.com/track/0LmEzNrxk0lecRm8X58jiC?si=A1Yws1c2TdSZ_6bDCOuCNg', 'spotify_URI': 'spotify:track:0LmEzNrxk0lecRm8X58jiC'},
    'Just One Dance': {'artist': 'Caro Emerald', 'bpm': 55, 'tags': [], 'spotify_URL': 'https://open.spotify.com/track/2HSEXxOWGrmkUDa1ftt6iQ?si=-MshVb_DQl2hm1dSrbh8jw', 'spotify_URI': 'spotify:track:2HSEXxOWGrmkUDa1ftt6iQ'},
    'Boom Boom Goes My Heart': {'artist': 'Alex Swings Oscar Sings!', 'bpm': 65, 'tags': [], 'spotify_URL': 'https://open.spotify.com/track/5mgFHE4QZ8hdZwl5A5pR0h?si=1WZnqzcKReWb4VHZHUJQ_A', 'spotify_URI': 'spotify:track:5mgFHE4QZ8hdZwl5A5pR0h'},
    'Hip To Be Square': {'artist': 'Huey Lewis & The News', 'bpm': 70, 'tags': [], 'spotify_URL': 'https://open.spotify.com/track/648BMGrt98kUbLo24A4vgj?si=HmyMmfb0SnWTY_E-j564Eg', 'spotify_URI': 'spotify:track:648BMGrt98kUbLo24A4vgj'},
    "Danny's All-Star Joint": {'artist': 'Rickie Lee Jones', 'bpm': 72, 'tags': [], 'spotify_URL': 'https://open.spotify.com/track/0NQDBfriyjeCoSq8TJ2Nrr?si=CgufYvsrQtSXF-0I4KfuJg', 'spotify_URI': 'spotify:track:0NQDBfriyjeCoSq8TJ2Nrr'},
    'Last Friday Night (T.G.I.F)': {'artist': 'Katy Perry', 'bpm': 63, 'tags': ['pop'], 'spotify_URL': 'https://open.spotify.com/track/3oHNJECGN3bBoGXejlw2b1?si=ZThWh-UvQN2COq3p4_030A', 'spotify_URI': 'spotify:track:3oHNJECGN3bBoGXejlw2b1'},
    'Part Of Me': {'artist': 'Katy Perry', 'bpm': 65, 'tags': ['pop', 'koselig'], 'spotify_URL': 'https://open.spotify.com/track/1nZzRJbFvCEct3uzu04ZoL?si=anUemSD1TXi4vhtzmdt7vg', 'spotify_URI': 'spotify:track:1nZzRJbFvCEct3uzu04ZoL'},
    "C'est Toi": {'artist': 'Dany Brilliant, Claude Wagner', 'bpm': 64, 'tags': [], 'spotify_URL': 'https://open.spotify.com/track/6IgTNSwnShmQMNZQ476tSx?si=yEqjd0g1SlCVbqAP7L34HA', 'spotify_URI': 'spotify:track:6IgTNSwnShmQMNZQ476tSx'},
    "You've Got a Friend in Me": {'artist': 'Randy Newman', 'bpm': 58, 'tags': [], 'spotify_URL': 'https://open.spotify.com/track/4dzWhN1AsIsg8b5QS1z9G4?si=gI-FPFVcSxOFgxezZeK1FA', 'spotify_URI': 'spotify:track:4dzWhN1AsIsg8b5QS1z9G4'},
    'Grease': {'artist': 'Frankie Valli', 'bpm': 55, 'tags': [], 'spotify_URL': 'https://open.spotify.com/track/1KnckjAZIi2mE9EdBLTJmX?si=-NA3-csVQp61QLJVz7Wa0w', 'spotify_URI': 'spotify:track:1KnckjAZIi2mE9EdBLTJmX'},
    'Budapest': {'artist': 'George Ezra', 'bpm': 64, 'tags': ['koselig'], 'spotify_URL': 'https://open.spotify.com/track/7GJClzimvMSghjcrKxuf1M?si=lztnh-fuQn2dvBe5o4SEmA', 'spotify_URI': 'spotify:track:7GJClzimvMSghjcrKxuf1M'},
    "Ain't No Mountain High Enough": {'artist': 'Marvin Gaye, Tammi Terrell', 'bpm': 65, 'tags': [], 'spotify_URL': 'https://open.spotify.com/track/2H3ZUSE54pST4ubRd5FzFR?si=B28s_WNfTUuA8m9hPKPe_g', 'spotify_URI': 'spotify:track:2H3ZUSE54pST4ubRd5FzFR'},
    'New Shoes': {'artist': 'Paolo Nutini', 'bpm': 75, 'tags': ['lav energi'], 'spotify_URL': 'https://open.spotify.com/track/265Anh9hGoozFigjUVLUeD?si=D_r9I0iMRMCsQSxTzQRLLw', 'spotify_URI': 'spotify:track:265Anh9hGoozFigjUVLUeD'},
    'Do Wah Diddy Diddy': {'artist': 'Manfred Mann', 'bpm': 63, 'tags': [], 'spotify_URL': 'https://open.spotify.com/track/4y50Di3Klx36lvldnnd1vL?si=3YgrRtTORlahLpN6aiRDfw', 'spotify_URI': 'spotify:track:4y50Di3Klx36lvldnnd1vL'},
    'Big Spender': {'artist': 'Shirley Bassey', 'bpm': 63, 'tags': ['vanskelig takt'], 'spotify_URL': 'https://open.spotify.com/track/0sfHo5YX7ZBm40FlEVivDG?si=exSk91yuQpS-hWXjNIce2w', 'spotify_URI': 'spotify:track:0sfHo5YX7ZBm40FlEVivDG'},
    'Summer Sunshine': {'artist': 'The Corrs', 'bpm': 61, 'tags': ['koselig'], 'spotify_URL': 'https://open.spotify.com/track/3e1QuucYG7rI1yS4glKNbk?si=_OpnDWAOQfuy-hW_-f6Anw', 'spotify_URI': 'spotify:track:3e1QuucYG7rI1yS4glKNbk'},
    "Don't Stop 'Til You Get Enough'": {'artist': 'Michael Jackson', 'bpm': 60, 'tags': [], 'spotify_URL': 'https://open.spotify.com/track/6AZZzlQD1FThgAcWIgu3g1?si=vHbcWIgzRT6zQiaCmR2JyQ', 'spotify_URI': 'spotify:track:6AZZzlQD1FThgAcWIgu3g1'},
    'Bills': {'artist': 'LunchMoney Lewis', 'bpm': 63, 'tags': ['høy energi'], 'spotify_URL': 'https://open.spotify.com/track/10znXCse0n6fZQWKWzqOop?si=YCz3QL6gQ-yWzv7hApH_ag', 'spotify_URI': 'spotify:track:10znXCse0n6fZQWKWzqOop'},
    'Tonight Tonight': {'artist': 'Hot Chelle Rae', 'bpm': 50, 'tags': ['høy energi'], 'spotify_URL': 'https://open.spotify.com/track/2i0AUcEnsDm3dsqLrFWUCq?si=93lp_2iYQJGo1D9QRu9eYw', 'spotify_URI': 'spotify:track:2i0AUcEnsDm3dsqLrFWUCq'},
    '9 to 5': {'artist': 'Dolly Parton', 'bpm': 53, 'tags': [], 'spotify_URL': 'https://open.spotify.com/track/4w3tQBXhn5345eUXDGBWZG?si=AGpZciDPSn-0DqOZRJvXtg', 'spotify_URI': 'spotify:track:4w3tQBXhn5345eUXDGBWZG'},
    'Call Me Maybe': {'artist': 'Carly Rae Jepsen', 'bpm': 60, 'tags': ['styling', 'koselig', 'spin'], 'spotify_URL': 'https://open.spotify.com/track/20I6sIOMTCkB6w7ryavxtO?si=4pEFRqVSTwKvJ3s04U_usg', 'spotify_URI': 'spotify:track:20I6sIOMTCkB6w7ryavxtO'},
    'September': {'artist': 'Earth, Wind & Fire', 'bpm': 63, 'tags': ['koselig'], 'spotify_URL': 'https://open.spotify.com/track/7Cuk8jsPPoNYQWXK9XRFvG?si=BrpvgEMZQd6J5mHYf7hr4A', 'spotify_URI': 'spotify:track:7Cuk8jsPPoNYQWXK9XRFvG'},
    'Rock Steady': {'artist': 'Ole Børud', 'bpm': 69, 'tags': [], 'spotify_URL': 'https://open.spotify.com/track/5WCAW8xyyGevUxlUiFBvxL?si=BKWjlj-CRVC30pfuHEK1vg', 'spotify_URI': 'spotify:track:5WCAW8xyyGevUxlUiFBvxL'},
    'Summertime Blues': {'artist': 'Dion', 'bpm': 77, 'tags': [], 'spotify_URL': 'https://open.spotify.com/track/75PlQtrs8lKbY2Lh64LsNc?si=tPJEDkDuT2imIOT-xyh40A', 'spotify_URI': 'spotify:track:75PlQtrs8lKbY2Lh64LsNc'},
    'En jävel på kärlek': {'artist': 'Glenmark Eriksson Strömsedt', 'bpm': 78, 'tags': [], 'spotify_URL': 'https://open.spotify.com/track/6sDc7xKVYe28DdASxT4FxR?si=4V6hte_CR_yS9QqjeVIC3g', 'spotify_URI': 'spotify:track:6sDc7xKVYe28DdASxT4FxR'},
    'Be My Baby Tonight': {'artist': 'John Michael Montgomery', 'bpm': 78, 'tags': ['country'], 'spotify_URL': 'https://open.spotify.com/track/674B5e1tIUKZkXUPIJayss?si=KvKZt9GYS5C9DbVw7VmjQg', 'spotify_URI': 'spotify:track:674B5e1tIUKZkXUPIJayss'},
    'Unbelievable': {'artist': 'Diamond Rio', 'bpm': 78, 'tags': ['country'], 'spotify_URL': 'https://open.spotify.com/track/2zNuaa0jBttcqSeURO6Odt?si=FHesNgKcQVyjKCahVQdyXA', 'spotify_URI': 'spotify:track:2zNuaa0jBttcqSeURO6Odt'},
    'Greased Lightning': {'artist': 'John Travolta', 'bpm': 80, 'tags': ['høy energi'], 'spotify_URL': 'https://open.spotify.com/track/4S9RHp3Ge0xepqcixPQ6Fc?si=TpFbo8dTQHGMCUB-lei-QA', 'spotify_URI': 'spotify:track:4S9RHp3Ge0xepqcixPQ6Fc'},
    'Bienvenue dans ma vie': {'artist': 'Nikki Yanofsky', 'bpm': 72, 'tags': ['koselig'], 'spotify_URL': 'https://open.spotify.com/track/0K4sxJf1SSnoGPmEWjGDnA?si=Q3sghi9ESJ2bNB2sgqlbdg', 'spotify_URI': 'spotify:track:0K4sxJf1SSnoGPmEWjGDnA'},
    'Solitude City': {'artist': 'Les Forbans', 'bpm': 60, 'tags': [], 'spotify_URL': 'https://open.spotify.com/track/4pNetJzdTdjSN5hXUmhpZ3?si=naJM8zGESLSiDvr0gtQwRg', 'spotify_URI': 'spotify:track:4pNetJzdTdjSN5hXUmhpZ3'},
    #'Title': {'artist': 'xxx', 'bpm': xxx, 'tags': ['name'], 'spotify_URL': 'xxx', 'spotify_URI': 'xxx'},

}


class Command(BaseCommand):

    def delete_songs(self):
        Song.objects.all().delete()

    def create_songs(self):
        global songs
        spinner = Halo("Creating songs")
        spinner.start()
        for tittel, info in songs.items():
            s = Song.objects.create(
                tittel = tittel,
                artist = info['artist'],
                bpm = info['bpm'],
                spotify = info['spotify_URL'],
                URI = info['spotify_URI'],
            )

            for navn in info['tags']:
                t, created = SongTag.objects.get_or_create(navn=navn)
                s.tags.add(t)
        spinner.succeed()

    def handle(self, *args, **options):
        self.delete_songs()
        self.create_songs()
        # End of handle
