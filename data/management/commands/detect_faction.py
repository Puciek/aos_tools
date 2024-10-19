import json
import re

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import DataError
from django.db.models import Q, F

from data.models import *

failed_factions = {}


def ask_chat_gpt(prompt):
    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 100,
        "temperature": 0.7,
        "model": "gpt-4o-mini",
        "response_format": {"type": "json_object"},
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
    }

    success = False
    while success is False:
        try:
            response = requests.post(
                url, data=json.dumps(payload), headers=headers, timeout=10
            )
            success = True
        except requests.exceptions.Timeout:
            pass
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data}")
        return data["choices"][0]["message"]["content"].strip()
    else:
        raise ValueError(
            f"Request failed with status code {response.status_code} and {response.text}"
        )


def regexp_army_details_aos(text):
    faction_match = re.search(r"(Faction|Allegiance): (.+)", text)
    subfaction_match = re.search(
        r"(Subfaction|Glade|Stormhost|Mawtribe|Lodge|Legion|Constellation|Slaughterhost|Slaughterhosts|Tribe|Temple|Warclan|Host of Chaos|Enclave|Army Type|Lineage|Procession|City|Grand Court|Great Nation|Greatfray|Sky Port|Change Coven|Glade|Host|Option): ([\w+ \-\_]*)",
        text,
    )
    grand_strategy_match = re.search(r"Grand Strategy: ([\w+ \-\_]*)", text)

    if faction_match:
        faction = faction_match.group(2).strip()
    else:
        raise ValueError("Faction not detected in the input text.")

    if faction == "Nurgle":
        faction = "Maggotkin of Nurgle"
    elif faction == "Khorne":
        faction = "Blades of Khorne"
    elif faction == "Slaanesh":
        faction = "Hedonites of Slaanesh"
    elif faction == "Tzeentch":
        faction = "Disciples of Tzeentch"
    elif "Soulblight Gravelords" in faction:
        faction = "Soulblight Gravelords"

    if faction not in aos_factions:
        raise ValueError(f"Faction {faction} not recognized.")

    if subfaction_match:
        subfaction = subfaction_match.group(2).strip()
    else:
        raise ValueError("Subfaction not detected in the input text.")

    if grand_strategy_match:
        grant_strategy = grand_strategy_match.group(1).strip()
    else:
        grant_strategy = None

    return {
        "faction": faction,
        "subfaction": subfaction,
        "grand_strategy": grant_strategy,
    }


def extract_faction_details_for_aos(army_list_id: int):
    army_list = List.objects.get(id=army_list_id)
    list_text = army_list.raw_list
    prompt = f"""
    For given list of Age of Sigmar please fill in the following fields and return it as json document: {{"faction": string,"subfaction": string,}}
    
    Return only the json document, with no wrapper, markings or other commentary. If there are multiple lists, only process the first one, never return more than 1 set of requested data. Remove any text from it that's not directly the subfaction or faction.

    Valid list of factions: aos_factions = [
        "Stormcast Eternals",
        "Daughters of Khaine",
        "Fyreslayers",
        "Idoneth Deepkin",
        "Kharadron Overlords",
        "Lumineth Realm-lords",
        "Sylvaneth",
        "Seraphon",
        "Cities of Sigmar",
        "Slaves to Darkness",
        "Blades of Khorne",
        "Disciples of Tzeentch",
        "Hedonites of Slaanesh",
        "Maggotkin of Nurgle",
        "Skaven",
        "Beasts of Chaos",
        "Legion of Azgorh",
        "Flesh-eater Courts",
        "Nighthaunt",
        "Ossiarch Bonereapers",
        "Soulblight Gravelords",
        "Orruk Warclans",
        "Gloomspite Gitz",
        "Sons of Behemat",
        "Ogor Mawtribes",
    ]
    
    Valid list of subfactions: aos_subfactions = [
        "Fortress-City Defenders",
        "Collegiate Arcane Expedition",
        "Dawnbringer Crusade",
        "Ironweld Guild Army",
        "Scáthcoven",
        "Shadow Patrol",
        "Cauldron Guard",
        "Slaughter Troupe",
        "Scales of Vulcatrix",
        "Forge Brethren",
        "Warrior Kinband",
        "Lords of the Lodge",
        "Akhelian Beastmasters",
        "Soul-raid Ambushers",
        "Isharann Council",
        "Namarti Corps",
        "Endrineers Guild Expeditionary Force",
        "Iron Sky Attack Squadron",
        "Grundcorps Wing",
        "Aether-runners",
        "Vanari Battlehost",
        "Alarith Temple",
        "Scinari Council",
        "Hurakan Temple",
        "Thunderhead Host",
        "Lightning Echelon",
        "Vanguard Wing",
        "Sentinels of the Bleak Citadels",
        "Eternal Starhost",
        "Shadowstrike Starhost",
        "Sunclaw Starhost",
        "Thunderquake Starhost",
        "Lords of the Clan",
        "Outcasts",
        "Free Spirits",
        "Forest Folk",
        "Death Battle formations",
        "Cannibal Court",
        "Ghoul Patrol",
        "Lords of the Manor",
        "Royal Menagerie",
        "Vanishing Phantasms",
        "Hunters of the Accursed",
        "Death Stalkers",
        "Procession of Death",
        "Mortisan Council",
        "Mortek Phalanx",
        "Kavalos Lance",
        "Mortek Ballistari",
        "Legion of Shyish",
        "Deathstench Drove",
        "Bacchanal of Blood",
        "Deathmarch",
        "Marauding Brayherd",
        "Hungering Warherd",
        "Almighty Beastherd",
        "Thunderscorn Stormherd",
        "Depraved Carnival",
        "Epicurean Revellers",
        "Seeker Cavalcade",
        "Supreme Sybarites",
        "Khornate Legion",
        "Brass Stampede",
        "Murder Host",
        "Bloodbound Warhorde",
        "Tallyband of Nurgle",
        "Plague Cyst",
        "Nurgle’s Menagerie",
        "Affliction Cyst",
        "Despoilers",
        "Darkoath Horde",
        "Godsworn Warband",
        "Legion of Chaos",
        "Claw-Horde",
        "Fleshmeld Menargerie",
        "Virulent Procession",
        "Warpog Convocation",
        "Arcanite Cabal",
        "Tzaangor Coven",
        "Change Host",
        "Wyrdflame Host",
        "Kunnin' Rukk",
        "Snaga Rukk",
        "Brutal Rukk",
        "Kop Rukk",
        "Squigalanch",
        "Moonclan Skrap",
        "Troggherd",
        "Spiderfang Stalktribe",
        "Prophets of the Gulping God",
        "Heralds of the Everwinter",
        "Beast Handlers",
        "Blackpowder Fanatics",
        "Ironfist",
        "Weirdfist",
        "Ironjawz Brawl",
        "Grunta Stampede",
        "Kruleboyz Klaw",
        "Middul Finga",
        "Light Finga",
        "Trophy Finga",
        "Taker Tribe",
        "Breaker Tribe",
        "Stomper Tribe",
        "Boss Tribe",
    ]


    Ignore how the faction in the list is written, just match it to the closest faction in the
    above and return that faction if there is a match (typos and shorthand are expected). If the faction is not in the list, return "False", if the subfaction is not in the list of subfactions, return "False".

    list:

                {list_text}
                """
    try:
        details = regexp_army_details_aos(list_text)
        faction = details["faction"]
        if "\t" in faction:
            faction = faction.split("\t")[0]
        if " - " in faction:
            faction = faction.split(" - ")[0]
        subfaction = details["subfaction"]
        grand_strategy = details["grand_strategy"]
        army_list.faction = faction
        army_list.subfaction = subfaction
        army_list.grand_strategy = grand_strategy
        army_list.save()
        print(
            f"Detected faction: {faction} and subfaction: {subfaction} for {army_list.source_id} using regex"
        )
        army_list.regexp_parsed = True
        army_list.save()
        return True
    except (ValueError, DataError) as e:
        print(
            f"Failed to detect faction for {army_list.source_id} error: {e} using regex"
        )
    response = ask_chat_gpt(prompt)
    try:
        payload = json.loads(response.replace("```", "").replace("json", ""))
    except json.decoder.JSONDecodeError as e:
        print(f"Failed to decode json for {army_list.source_id} error: {e}")
        army_list.gpt_parsed = True
        army_list.gpt_parse_error = e
        return False
    try:
        if payload["faction"] not in aos_factions:
            raise ValueError(f"Faction {payload['faction']} not recognized.")
        army_list.faction = payload["faction"]
        if payload["subfaction"] not in aos_subfactions:
            raise ValueError(f"Subfaction {payload['subfaction']} not recognized.")
        army_list.subfaction = payload["subfaction"]
        army_list.manifestation_lores = payload.get("manifestation_lores", None)
        army_list.prayer_lores = payload.get("prayer_lores", None)
        army_list.spell_lores = payload.get("spell_lores", None)
        if army_list.faction == "":
            army_list.faction = None
        if army_list.subfaction == "":
            army_list.subfaction = None
        if "grand_strategy" in payload:
            army_list.grand_strategy = payload["grand_strategy"]
    except KeyError as e:
        print(
            f"Failed to detect faction for {army_list.source_id} error: {e} using gpt"
        )
    try:
        army_list.save()
        army_list.gpt_parsed = True
        army_list.save()
    except DataError as e:
        print(f"Failed to save faction for {army_list.source_id} error: {e}")
        army_list.gpt_parsed = True
        army_list.gpt_parse_error = e
        army_list.save()
    print(
        f"Detected faction: {army_list.faction} and subfaction: {army_list.subfaction} for {army_list.source_id} using gpt"
    )
    return True


def extract_faction_details_for_40k(id):
    army_list = List.objects.get(id=id)
    list_text = army_list.raw_list
    list_text = list_text.replace("’", "'")
    faction_in_text = next(
        (faction for faction in w40k_factions if faction.lower() in list_text.lower()),
        None,
    )
    if not faction_in_text:
        if "Adeptas Sororitas".lower() in list_text.lower():
            faction_in_text = "Adepta Sororitas"
        elif "Chaos Demons".lower() in list_text.lower():
            faction_in_text = "Chaos Daemons"
        elif "Termaguants".lower() in list_text.lower():
            faction_in_text = "Tyranids"
        elif "IG" in list_text:
            faction_in_text = "Astra Militarum"
        elif "Genestealer Cult".lower() in list_text.lower():
            faction_in_text = "Genestealer Cults"
        else:
            faction_in_text = next(
                (
                    faction
                    for faction in w40k_marines
                    if faction.lower() in list_text.lower()
                ),
                None,
            )
            if faction_in_text:
                faction_in_text = "Space Marines"
    if not faction_in_text:
        print(
            f"Failed to detect faction for {army_list.source_id} using text, assigning from user selection"
        )
        if "armyName" in army_list.source_json:
            selected_army = army_list.source_json["armyName"]
            if selected_army in w40k_factions:
                faction_in_text = selected_army
            elif selected_army in w40k_marines:
                faction_in_text = "Space Marines"
            elif selected_army in w40k_chaos_space_marines:
                faction_in_text = "Chaos Space Marines"
            elif selected_army in w40k_dark_angel:
                faction_in_text = "Dark Angels"
            elif "Astra Militarum".lower() == selected_army.lower():
                faction_in_text = "Astra Militarum"
            elif "GeneStealer Cult".lower() == selected_army.lower():
                faction_in_text = "Genestealer Cults"
            else:
                if selected_army not in failed_factions:
                    failed_factions[selected_army] = 1
                else:
                    failed_factions[selected_army] += 1
                faction_in_text = None
    if faction_in_text:
        army_list.faction = faction_in_text
        army_list.save()
        print(
            f"Detected faction: {faction_in_text} for {army_list.source_id} using text"
        )
        return True
    else:
        print(f"Failed to detect faction for {army_list.source_id} using text")


class Command(BaseCommand):
    help = "Detect Faction and Subfaction for downloaded lists"

    def handle(self, *args, **options):
        army_lists = (
            List.objects.exclude(Q(raw_list=""))
            .filter(Q(faction__isnull=True))
            .annotate(event_date=F("participant__event__start_date"))
            .annotate(game_type=F("participant__event__game_type"))
            .filter(game_type__in=[AOS])
            .filter(event_date__gte="2024-07-01")
            .exclude(gpt_parsed=True)
            .filter(~Q(raw_list="") | ~Q(raw_list__isnull=True))
        )
        self.stdout.write(f"Detecting for {army_lists.count()} lists")
        for army_list in army_lists:
            if army_list.game_type == AOS:
                extract_faction_details_for_aos(army_list.id)
            elif army_list.game_type == W40K:
                extract_faction_details_for_40k(army_list.id)
        self.stdout.write(f"Failed factions: {failed_factions}")
