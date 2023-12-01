import csv

from django.http import HttpResponse
from django.shortcuts import render
from data.models import List, Event, Participant, Pairing, Player


def raw_list(request, list_id):
    list = List.objects.get(id=list_id)
    return HttpResponse(list.raw_list.replace("\n", "<br>"))


def export_pairings_as_csv(request):
    pairings = Pairing.objects.filter(
        event__start_date__range=["2023-07-15", "2023-12-31"], event__rounds__in=[3, 5]
    ).order_by("event__name", "-event__start_date", "round", "id")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="pairings.csv"'

    writer = csv.writer(response)
    writer.writerow(
        [
            "pairing_id",
            "round",
            "player1_name",
            "player2_name",
            "player1_result",
            "player2_result",
            "player1_score",
            "player2_score",
            "event_name",
            "event_date",
            "event_end_date",
            "season",
            "player1_faction",
            "player1_subfaction",
            "player2_faction",
            "player2_subfaction",
            "player1_list_url",
            "player2_list_url",
        ]
    )

    for pairing in pairings:
        player1_name = (
            f"{pairing.player1.player.source_json['firstName']} {pairing.player1.player.source_json['lastName']}"
            if pairing.player1
            else ""
        )
        player2_name = (
            f"{pairing.player2.player.source_json['firstName']} {pairing.player2.player.source_json['lastName']}"
            if pairing.player2
            else ""
        )
        player1_list_faction = (
            pairing.player1_list.faction if pairing.player1_list else ""
        )
        player1_list_subfaction = (
            pairing.player1_list.subfaction if pairing.player1_list else ""
        )
        player2_list_faction = (
            pairing.player2_list.faction if pairing.player2_list else ""
        )
        player2_list_subfaction = (
            pairing.player2_list.subfaction if pairing.player2_list else ""
        )

        writer.writerow(
            [
                pairing.id,
                pairing.round,
                player1_name,
                player2_name,
                pairing.player1_result,
                pairing.player2_result,
                pairing.player1_score,
                pairing.player2_score,
                pairing.event.name,
                pairing.event.start_date,
                pairing.event.end_date,
                "2023",
                player1_list_faction,
                player1_list_subfaction,
                player2_list_faction,
                player2_list_subfaction,
                pairing.player1_list.raw_list if pairing.player1_list else "",
                pairing.player2_list.raw_list if pairing.player2_list else "",
            ]
        )

    return response
