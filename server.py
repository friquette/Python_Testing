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

        if foundClub and foundCompetition:
            return render_template(
                'booking.html',
                club=foundClub,
                competition=foundCompetition
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

        if placesRequired > 12:
            flash("You can't purchase more than 12 places for a competition")
            return render_template(
                'booking.html',
                club=club,
                competition=competition
            )
        elif (placesRequired * POINTS_PER_PLACES) > int(club['points']):
            flash("You don't have enough points")
            return render_template(
                'booking.html',
                club=club,
                competition=competition
            )
        elif placesRequired > int(competition['numberOfPlaces']):
            flash("Not enough places available in this competition")
            return render_template(
                'booking.html',
                club=club,
                competition=competition
            )

        competition['numberOfPlaces'] = str(
            int(competition['numberOfPlaces']) - placesRequired
        )

        club['points'] = str(
            int(club['points']) - (placesRequired * POINTS_PER_PLACES)
        )

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
