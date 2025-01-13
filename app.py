from flask import Flask, jsonify, request
from flask_cors import CORS
# from DataFetcher import DATAFETCHER

from data.utils.datafetcher import DataFetcher


app = Flask(__name__)
CORS(app)

# Initialize the data fetcher
data_fetcher = DataFetcher(job_class="All Technical Jobs")
# print(data_fetcher)

df = data_fetcher.get_dataframe(job_class="All Technical Jobs")

# Role options
options = ['All Technical Jobs']
options.extend(df.job_domain.unique().tolist())


@app.route('/api/role_options', methods=['GET'])
def get_role_options():
    return jsonify(options)


@app.route('/api/all_data', methods=['POST'])
def get_all_data():
    selected_role = request.json.get('role')  # Get the role from the POST request
    print(selected_role)
    try:
        # if selected_role == "All Technical Jobs":
        #     selected_role = None

        data_fetcher = DataFetcher(selected_role)

        # Education data
        education_data = dict(data_fetcher.get_education())
        
        # Language data
        language_data = data_fetcher.get_languages()
        language_list = [
            {"Category": category, "Value": value}
            for category, value in zip(language_data['Category'], language_data['Value'])
        ]
        
        # Package data
        package_data = data_fetcher.get_frameworks()
        package_list = [
            {"Category": category, "Value": value}
            for category, value in zip(package_data['Category'], package_data['Value'])
        ]
        
        # Total jobs
        total_jobs = len(data_fetcher.get_dataframe(selected_role))
        
        # Combine all data into one JSON response
        combined_data = {
            "education_data": education_data,
            "language_data": language_list,
            "package_data": package_list,
            "total_jobs": total_jobs
        }
        
        return jsonify(combined_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
