from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.forms import SearchForm, ContactForm
from app.utils import import_agents_from_csv
from bson import ObjectId
import os

@app.route('/')
def index():
    form = SearchForm()
    return render_template('index.html', form=form)

@app.route('/search', methods=['GET'])
def search():
    form = SearchForm(request.args)
    search_query = form.search_query.data
    results = []

    if search_query:
        results = db.agents.find({"$text": {"$search": search_query}})

    return render_template('index.html', form=form, results=results)

@app.route('/import_agents', methods=['GET', 'POST'])
def import_agents():
    form = SearchForm()  # Add form to pass it to the template
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = os.path.join('data', file.filename)
            file.save(file_path)
            import_agents_from_csv(file_path)
            flash('Agents imported successfully!', 'success')
            return redirect(url_for('index'))
    return render_template('import_agents.html', form=form)  # Pass form here too

@app.route('/contact/<agent_id>', methods=['GET', 'POST'])
def contact(agent_id):
    agent = db.agents.find_one({"_id": ObjectId(agent_id)})
    form = ContactForm()

    if request.method == 'POST' and form.validate():
        # Handle sending email or SMS to the agent
        flash('Message sent successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('contact.html', agent=agent, form=form)
