import json
import datetime
import math

from flask import Flask, render_template, request, redirect, flash, url_for

POINTS_PER_PLACES = 3


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


def create_app(config):

    app = Flask(__name__)
    app.secret_key = 'something_special'

    competitions = loadCompetitions()
    clubs = loadClubs()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/showSummary', methods=['POST'])
    def showSummary():
        try:
            club = [club for club in clubs if club['email'] == request.form['email']][0]  # noqa
        except IndexError:
            flash("Sorry, this email wasn't found.")
            return render_template(
                'index.html'
            )
        except Exception:
            flash("Something went wrong, please try again")
            return render_template(
                'index.html'
            )
        else:
            return render_template(
                'welcome.html',
                club=club,
                competitions=competitions,
                datetime=datetime
            )

    @app.route('/book/<competition>/<club>')
    def book(competition, club):
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]  # noqa
        club_points = int(foundClub['points'])
        max_places_from_comp = int(foundCompetition['numberOfPlaces'])
        max_places_from_points = math.floor(club_points / POINTS_PER_PLACES)

        if max_places_from_comp > 12 and max_places_from_points > 12:
            places = 12
        elif max_places_from_points <= max_places_from_comp:
            places = max_places_from_points
        elif max_places_from_points > max_places_from_comp:
            places = max_places_from_comp

        if foundClub and foundCompetition:
            return render_template(
                'booking.html',
                club=foundClub,
                competition=foundCompetition,
                places=places
            )
        else:
            flash("Something went wrong-please try again")
            return render_template(
                'welcome.html',
                club=club,
                competitions=competitions
            )

    @app.route('/purchasePlaces', methods=['POST'])
    def purchasePlaces():
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]  # noqa
        club = [c for c in clubs if c['name'] == request.form['club']][0]

        placesRequired = int(request.form['places'])
        competition['numberOfPlaces'] = int(
            competition['numberOfPlaces']
        ) - placesRequired

        club['points'] = int(club['points']) - placesRequired
        flash('Great-booking complete!')

        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions,
            datetime=datetime
        )

    @app.route('/pointsDisplay/<club>')
    def pointsDisplay(club):
        current_club = [c for c in clubs if c['name'] == club][0]
        return render_template(
            'board.html',
            clubs=clubs,
            current_club=current_club
        )

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    return app
