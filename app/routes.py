from flask import render_template, request, redirect, url_for, flash, make_response
from app import app, db
from app.forms import SearchForm, ContactForm, ImportForm, SaveSearchForm, YouTubeSearchForm
from app.utils import import_agents_from_csv
from app.serpapi_utils import search_google_local, search_youtube
from bson import ObjectId
import os
import csv
import io

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        search_query = form.search_query.data
        return redirect(url_for('search', query=search_query))
    return render_template('index.html', form=form)

@app.route('/search')
def search():
    query = request.args.get('search_query', '')
    search_results = []
    if query:
        search_results = list(db.agents.find({"$text": {"$search": query}}))
    return render_template('search_results.html', query=query, search_results=search_results)

@app.route('/contact/<agent_id>', methods=['GET', 'POST'])
def contact(agent_id):
    agent = db.agents.find_one({"_id": ObjectId(agent_id)})
    form = ContactForm()
    if form.validate_on_submit():
        # Implement email/text sending logic here
        flash('Message sent successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('contact.html', agent=agent, form=form)

@app.route('/import_agents', methods=['GET', 'POST'])
def import_agents():
    form = ImportForm()
    if form.validate_on_submit():
        file = form.csv_file.data
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        import_agents_from_csv(file_path)
        flash('Agents imported successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('import_agents.html', form=form)

@app.route('/serpapi_search_page', methods=['GET'])
def serpapi_search_page():
    return render_template('serpapi_search.html', search_results=[])

@app.route('/serpapi_search', methods=['GET'])
def serpapi_search():
    query = request.args.get('query', '')
    country = request.args.get('country', 'United States')
    state = request.args.get('state', '')
    city = request.args.get('city', '')

    location_parts = [city, state, country]
    location = ", ".join([part for part in location_parts if part]).strip(', ')
    search_results = search_google_local(query, location)

    return render_template('serpapi_search.html', query=query, search_results=search_results)

@app.route('/export_google_search', methods=['GET'])
def export_google_search():
    query = request.args.get('query', '')
    country = request.args.get('country', 'United States')
    state = request.args.get('state', '')
    city = request.args.get('city', '')

    location_parts = [city, state, country]
    location = ", ".join([part for part in location_parts if part]).strip(', ')
    search_results = search_google_local(query, location)

    # Create CSV
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Title', 'Address', 'Phone', 'Website', 'Type', 'Rating', 'Reviews'])
    for result in search_results:
        cw.writerow([result['title'], result['address'], result['phone'], result['website'], result['type'], result['rating'], result['reviews']])

    response = make_response(si.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=google_search_results.csv'
    response.headers["Content-type"] = "text/csv"
    return response

@app.route('/youtube_search_page', methods=['GET'])
def youtube_search_page():
    form = YouTubeSearchForm()
    return render_template('youtube_search.html', form=form, search_results=[])

@app.route('/youtube_search', methods=['GET'])
def youtube_search():
    query = request.args.get('query', '')
    search_results = search_youtube(query)
    return render_template('youtube_search.html', query=query, search_results=search_results)

@app.route('/export_youtube_search', methods=['GET'])
def export_youtube_search():
    query = request.args.get('query', '')
    search_results = search_youtube(query)

    # Create CSV
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Title', 'Link', 'Snippet', 'Thumbnail'])
    for result in search_results:
        cw.writerow([result['title'], result['link'], result['snippet'], result['thumbnail']])

    response = make_response(si.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=youtube_search_results.csv'
    response.headers["Content-type"] = "text/csv"
    return response
