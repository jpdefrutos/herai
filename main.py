from flask import Flask, render_template, request, send_from_directory
import yaml
from yaml.loader import SafeLoader
from werkzeug.utils import secure_filename
import tempfile
import os
import subprocess as sp


app = Flask("SINTEF MIA Catalogue")
APP_DICT = dict()


@app.route("/")
def main():
    ctx = load_catalogue()
    for app in ctx['apps']:
        APP_DICT[app['name']] = app
    return render_template("catalogue.jinja2", title="Catalogue", **ctx)   # By default, Flask expects your templates in a templates/ directory


@app.route("/application/<string:app_name>/<string:template>")
def application(app_name, template):
    # return render_template("{}.jinja2".format(app_name.lower()), **{'app_name': app_name.capitalize()})
    return process(app_name, template)


@app.route("/")
def update_processing_UI():
    render_template("processing.jinja2", title="Processing")


@app.route("/")
def downloader(dir_name, name):
    return send_from_directory(dir_name, name)


@app.route("/process/<string:app_name>/<string:template>", methods=["GET", "POST"])
def process(app_name, template):
    template_parameters = {
        'show_spin': str(False),
        'download_dir': '',
        'download_file_name': '',
        'app_name': app_name
    }   # These are the parameters if the request.method == 'GET', i.e., when the user first opens the app

    if request.method == "POST":
        # update UI that it is processing
        # update_processing_UI()

        # create temporary directory - will automatically delete when exiting context manager
        with tempfile.TemporaryDirectory() as dir_name:
            template_parameters['show_spin'] = str(True)
            template_parameters['download_dir'] = dir_name
            template_parameters['download_file_name'] = "prediction-livermask.nii"
            # upload
            f = request.files["file"]
            curr_path = os.path.join(dir_name, secure_filename(f.filename))
            f.save(curr_path)

            # process
            sp.check_call(["livermask", "--input", curr_path, "--output", os.path.join(dir_name, "prediction"), "--verbose"])

            # download result
            # downloader(dir_name, "prediction-livermask.nii")
            # NOTE: This has to be returned, otherwise, the result is NOT downloaded!
            return send_from_directory(dir_name, "prediction-livermask.nii")

            # return "Processing finished successfully!"
    return render_template(template+".jinja2", title="Processing", **template_parameters)

@app.route("/download/<string:dir_name>/<string:file_name>")
def download_results(dir_name, file_name):
    return send_from_directory(dir_name, file_name)

"""
# @app.route("/process/<string:app_name>", methods=['GET', 'POST'])
@app.route("/upload")
def process(app_name):
    if request.method == 'POST':
        f = request.files["the_file"]
        f.save("./{secure_filename(file.filename)")
        # Forward the uploaded data to the corresponding service
        # APP_DICT[app_name].
"""


def load_catalogue(catalogue_configuration_file: str='resources/catalogue.yaml') -> dict:
    catalogue_file = yaml.load(open(catalogue_configuration_file, 'r'), Loader=SafeLoader)
    return catalogue_file


if __name__ == '__main__':
    app.run(debug=True)
