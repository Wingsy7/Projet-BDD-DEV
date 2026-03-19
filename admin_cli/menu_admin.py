import json
from typing import Any

from client_api import ClientAPI


client = ClientAPI()


def prompt(message: str) -> str:
    return input(f"{message} : ").strip()


def prompt_int(message: str, allow_empty: bool = False) -> int | None:
    while True:
        value = prompt(message)
        if allow_empty and value == "":
            return None
        try:
            return int(value)
        except ValueError:
            print("Merci de saisir un nombre entier.")


def prompt_float(message: str, allow_empty: bool = False) -> float | None:
    while True:
        value = prompt(message)
        if allow_empty and value == "":
            return None
        try:
            return float(value)
        except ValueError:
            print("Merci de saisir un nombre.")


def prompt_bool(message: str, allow_empty: bool = False) -> bool | None:
    while True:
        value = prompt(f"{message} (o/n)").lower()
        if allow_empty and value == "":
            return None
        if value in {"o", "oui", "y", "yes"}:
            return True
        if value in {"n", "non", "no"}:
            return False
        print("Reponse attendue : o ou n.")


def show(data: Any) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=True))


def list_endpoint(path: str, params: dict | None = None) -> None:
    show(client.request("GET", path, params=params))


def print_title(title: str) -> None:
    print()
    print(f"--- {title} ---")


def preview_eleves() -> None:
    print_title("Eleves")
    for eleve in client.request("GET", "/admin/eleves"):
        print(
            f"{eleve['id']} - {eleve['nom']} | age {eleve['age']} | "
            f"promo {eleve['promotion']['nom']} | email {eleve['email']}"
        )


def preview_profs() -> None:
    print_title("Profs")
    for prof in client.request("GET", "/prof"):
        print(f"{prof['id']} - {prof['nom']} | age {prof['age']} | {prof['email']}")


def preview_promotions() -> None:
    print_title("Promotions")
    for promotion in client.request("GET", "/promotion"):
        print(
            f"{promotion['id']} - {promotion['nom']} | annee {promotion['annee']} | "
            f"specialite {promotion['specialite_nom']}"
        )


def preview_cours() -> None:
    print_title("Cours")
    for cours in client.request("GET", "/cours"):
        specialite = cours["specialite_nom"] or "Aucune"
        print(f"{cours['id']} - {cours['nom']} | niveau {cours['niveau']} | specialite {specialite}")


def preview_notes() -> None:
    print_title("Notes")
    for note in client.request("GET", "/note"):
        print(
            f"{note['id']} - {note['eleve_nom']} | {note['cours_nom']} | "
            f"{note['valeur']} | prof {note['prof_nom']}"
        )


def preview_instances() -> None:
    print_title("Instances de cours")
    for instance in client.request("GET", "/instances"):
        print(
            f"{instance['id']} - {instance['cours_nom']} | prof {instance['prof_nom']} | "
            f"{instance['date_cours']}"
        )


def preview_clubs() -> None:
    print_title("Clubs")
    for club in client.request("GET", "/clubs"):
        print(
            f"{club['id']} - {club['nom']} | {club['categorie']} | "
            f"budget {club['budget_annuel']} | membres {club['nombre_membres']}"
        )


def preview_club_inscriptions() -> None:
    print_title("Inscriptions club")
    for inscription in client.request("GET", "/club-inscriptions"):
        print(
            f"{inscription['id']} - club {inscription['club_nom']} | eleve {inscription['eleve_nom']} | "
            f"role {inscription['role_membre']} | date {inscription['date_inscription']}"
        )


def create_eleve() -> None:
    preview_promotions()
    payload = {
        "nom": prompt("Nom"),
        "email": prompt("Email"),
        "age": prompt_int("Age"),
        "promotion_id": prompt_int("Promotion id"),
    }
    show(client.request("POST", "/eleve", json_data=payload))


def update_eleve() -> None:
    preview_eleves()
    preview_promotions()
    eleve_id = prompt_int("Eleve id")
    payload = {
        "nom": prompt("Nouveau nom (laisser vide pour ignorer)") or None,
        "email": prompt("Nouvel email (laisser vide pour ignorer)") or None,
        "age": prompt_int("Nouvel age (laisser vide pour ignorer)", allow_empty=True),
        "promotion_id": prompt_int("Nouvelle promotion id (laisser vide pour ignorer)", allow_empty=True),
    }
    show(client.request("PUT", f"/eleve/{eleve_id}", json_data=payload))


def delete_eleve() -> None:
    preview_eleves()
    eleve_id = prompt_int("Eleve id")
    show(client.request("DELETE", f"/eleve/{eleve_id}"))


def create_prof() -> None:
    payload = {
        "nom": prompt("Nom"),
        "email": prompt("Email"),
        "age": prompt_int("Age"),
    }
    show(client.request("POST", "/prof", json_data=payload))


def update_prof() -> None:
    preview_profs()
    prof_id = prompt_int("Prof id")
    payload = {
        "nom": prompt("Nouveau nom (laisser vide pour ignorer)") or None,
        "email": prompt("Nouvel email (laisser vide pour ignorer)") or None,
        "age": prompt_int("Nouvel age (laisser vide pour ignorer)", allow_empty=True),
    }
    show(client.request("PUT", f"/prof/{prof_id}", json_data=payload))


def delete_prof() -> None:
    preview_profs()
    prof_id = prompt_int("Prof id")
    show(client.request("DELETE", f"/prof/{prof_id}"))


def create_note() -> None:
    preview_eleves()
    preview_cours()
    preview_profs()
    payload = {
        "eleve_id": prompt_int("Eleve id"),
        "cours_id": prompt_int("Cours id"),
        "prof_id": prompt_int("Prof id (laisser vide si absent)", allow_empty=True),
        "valeur": prompt_float("Valeur"),
        "commentaire": prompt("Commentaire (optionnel)") or None,
    }
    show(client.request("POST", "/note", json_data=payload))


def update_note() -> None:
    preview_notes()
    preview_eleves()
    preview_cours()
    preview_profs()
    note_id = prompt_int("Note id")
    payload = {
        "eleve_id": prompt_int("Eleve id (laisser vide pour ignorer)", allow_empty=True),
        "cours_id": prompt_int("Cours id (laisser vide pour ignorer)", allow_empty=True),
        "prof_id": prompt_int("Prof id (laisser vide pour ignorer)", allow_empty=True),
        "valeur": prompt_float("Valeur (laisser vide pour ignorer)", allow_empty=True),
        "commentaire": prompt("Commentaire (laisser vide pour ignorer)") or None,
    }
    show(client.request("PUT", f"/note/{note_id}", json_data=payload))


def update_dossier() -> None:
    preview_eleves()
    eleve_id = prompt_int("Eleve id")
    payload = {
        "infos": prompt("Infos (laisser vide pour ignorer)") or None,
        "avertissement_travail": prompt_bool("Avertissement travail", allow_empty=True),
        "avertissement_comportement": prompt_bool("Avertissement comportement", allow_empty=True),
    }
    show(client.request("PUT", f"/dossier/{eleve_id}", json_data=payload))


def create_instance() -> None:
    preview_cours()
    preview_profs()
    payload = {
        "cours_id": prompt_int("Cours id"),
        "prof_id": prompt_int("Prof id"),
        "date_cours": prompt("Date cours (YYYY-MM-DD HH:MM:SS)"),
    }
    show(client.request("POST", "/instances", json_data=payload))


def update_instance() -> None:
    preview_instances()
    preview_cours()
    preview_profs()
    instance_id = prompt_int("Instance id")
    payload = {
        "cours_id": prompt_int("Cours id (laisser vide pour ignorer)", allow_empty=True),
        "prof_id": prompt_int("Prof id (laisser vide pour ignorer)", allow_empty=True),
        "date_cours": prompt("Date cours (laisser vide pour ignorer)") or None,
    }
    show(client.request("PUT", f"/instances/{instance_id}", json_data=payload))


def delete_instance() -> None:
    preview_instances()
    instance_id = prompt_int("Instance id")
    show(client.request("DELETE", f"/instances/{instance_id}"))


def create_club() -> None:
    preview_profs()
    payload = {
        "nom": prompt("Nom"),
        "categorie": prompt("Categorie"),
        "budget_annuel": prompt_float("Budget annuel"),
        "responsable_prof_id": prompt_int("Prof responsable id (laisser vide si absent)", allow_empty=True),
    }
    show(client.request("POST", "/clubs", json_data=payload))


def update_club() -> None:
    preview_clubs()
    preview_profs()
    club_id = prompt_int("Club id")
    payload = {
        "nom": prompt("Nom (laisser vide pour ignorer)") or None,
        "categorie": prompt("Categorie (laisser vide pour ignorer)") or None,
        "budget_annuel": prompt_float("Budget annuel (laisser vide pour ignorer)", allow_empty=True),
        "responsable_prof_id": prompt_int("Prof responsable id (laisser vide pour ignorer)", allow_empty=True),
    }
    show(client.request("PUT", f"/clubs/{club_id}", json_data=payload))


def delete_club() -> None:
    preview_clubs()
    club_id = prompt_int("Club id")
    show(client.request("DELETE", f"/clubs/{club_id}"))


def create_club_inscription() -> None:
    preview_clubs()
    preview_eleves()
    payload = {
        "club_id": prompt_int("Club id"),
        "eleve_id": prompt_int("Eleve id"),
        "role_membre": prompt("Role"),
        "date_inscription": prompt("Date inscription (YYYY-MM-DD)"),
    }
    show(client.request("POST", "/club-inscriptions", json_data=payload))


def update_club_inscription() -> None:
    preview_club_inscriptions()
    preview_clubs()
    preview_eleves()
    inscription_id = prompt_int("Inscription id")
    payload = {
        "club_id": prompt_int("Club id (laisser vide pour ignorer)", allow_empty=True),
        "eleve_id": prompt_int("Eleve id (laisser vide pour ignorer)", allow_empty=True),
        "role_membre": prompt("Role (laisser vide pour ignorer)") or None,
        "date_inscription": prompt("Date inscription (laisser vide pour ignorer)") or None,
    }
    show(client.request("PUT", f"/club-inscriptions/{inscription_id}", json_data=payload))


def delete_club_inscription() -> None:
    preview_club_inscriptions()
    inscription_id = prompt_int("Inscription id")
    show(client.request("DELETE", f"/club-inscriptions/{inscription_id}"))


def menu_read() -> None:
    print("1. Liste eleves")
    print("2. Eleve par id")
    print("3. Eleves avertis")
    print("4. Eleves bonne_notes")
    print("5. Notes d'un eleve")
    print("6. Notes groupees")
    print("7. Profs severes")
    print("8. Dossiers")
    print("9. Instances")
    print("10. Clubs")
    print("11. Membres d'un club")
    print("12. Clubs d'un eleve")
    print("13. Heures d'absence d'un eleve")
    choice = prompt("Choix lecture")

    if choice == "1":
        list_endpoint("/eleve")
    elif choice == "2":
        preview_eleves()
        list_endpoint(f"/eleve/{prompt_int('Eleve id')}")
    elif choice == "3":
        list_endpoint("/eleve/avertis")
    elif choice == "4":
        list_endpoint("/eleve/bonne_notes")
    elif choice == "5":
        preview_eleves()
        list_endpoint(f"/notes/{prompt_int('Eleve id')}")
    elif choice == "6":
        list_endpoint("/note", params={"par": prompt("Par (eleve/prof/cours/promotion)")})
    elif choice == "7":
        list_endpoint("/prof/severe")
    elif choice == "8":
        list_endpoint("/dossier")
    elif choice == "9":
        list_endpoint("/instances")
    elif choice == "10":
        list_endpoint("/clubs")
    elif choice == "11":
        preview_clubs()
        list_endpoint(f"/clubs/{prompt_int('Club id')}/membres")
    elif choice == "12":
        preview_eleves()
        list_endpoint(f"/eleve/{prompt_int('Eleve id')}/clubs")
    elif choice == "13":
        preview_eleves()
        list_endpoint(f"/eleve/{prompt_int('Eleve id')}/absence")


def main() -> None:
    actions = {
        "1": preview_eleves,
        "2": create_eleve,
        "3": update_eleve,
        "4": delete_eleve,
        "5": preview_profs,
        "6": create_prof,
        "7": update_prof,
        "8": delete_prof,
        "9": preview_notes,
        "10": create_note,
        "11": update_note,
        "12": update_dossier,
        "13": preview_instances,
        "14": create_instance,
        "15": update_instance,
        "16": delete_instance,
        "17": preview_clubs,
        "18": create_club,
        "19": update_club,
        "20": delete_club,
        "21": preview_club_inscriptions,
        "22": create_club_inscription,
        "23": update_club_inscription,
        "24": delete_club_inscription,
        "25": menu_read,
    }

    while True:
        print()
        print("=== Menu admin de l'ecole ===")
        print("1. Lire eleves (admin)")
        print("2. Creer eleve")
        print("3. Modifier eleve")
        print("4. Supprimer eleve")
        print("5. Lire profs")
        print("6. Creer prof")
        print("7. Modifier prof")
        print("8. Supprimer prof")
        print("9. Lire notes")
        print("10. Creer note")
        print("11. Modifier note")
        print("12. Modifier dossier")
        print("13. Lire instances")
        print("14. Creer instance")
        print("15. Modifier instance")
        print("16. Supprimer instance")
        print("17. Lire clubs")
        print("18. Creer club")
        print("19. Modifier club")
        print("20. Supprimer club")
        print("21. Lire inscriptions club")
        print("22. Creer inscription club")
        print("23. Modifier inscription club")
        print("24. Supprimer inscription club")
        print("25. Voir les routes du sujet")
        print("0. Quitter")

        choice = prompt("Choix")
        if choice == "0":
            break

        action = actions.get(choice)
        if not action:
            print("Choix invalide.")
            continue

        try:
            action()
        except Exception as exc:
            print(f"Erreur : {exc}")


if __name__ == "__main__":
    main()
